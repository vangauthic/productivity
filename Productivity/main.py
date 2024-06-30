import discord
import yaml
import sys
import aiosqlite
import datetime as DT
import asyncio

from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime
from checks import check_tables

with open('config.yml', 'r') as file:
    data = yaml.safe_load(file)

token = data["General"]["TOKEN"]
activity = data["General"]["ACTIVITY"].lower()
doing_activity = data["General"]["DOING_ACTIVITY"]
status = data["General"]["STATUS"].lower()
admin_guild_id = data["General"]["ADMIN_GUILD_ID"]

initial_extensions = [
                      'cogs.utility.addtolist',
                      'cogs.utility.urgent',
                      'cogs.utility.submit'
                      ]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if status == "online":
    _status = getattr(discord.Status, status)
elif status == "idle":
    _status = getattr(discord.Status, status)
elif status == "dnd":
    _status = getattr(discord.Status, status)
elif status == "invisible":
    _status = getattr(discord.Status, status)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Status: {bcolors.ENDC}{bcolors.OKCYAN}{status}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}online{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}idle{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}dnd{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}invisible{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 7
""")

if activity == "playing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Game(name=doing_activity)
elif activity == "watching":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.watching)
elif activity == "listening":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.listening)
elif activity == "competing":
    if doing_activity == "":
        sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Doing Activity: {bcolors.OKBLUE}It Must Be Set!
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 5
""")
    else:
        _activity = discord.Activity(name=doing_activity, type=discord.ActivityType.competing)
else:
    sys.exit(f"""
{bcolors.FAIL}{bcolors.BOLD}ERROR:{bcolors.ENDC}
{bcolors.FAIL}Invalid Activity: {bcolors.ENDC}{bcolors.OKCYAN}{activity}{bcolors.ENDC}
{bcolors.OKBLUE}Valid Options: {bcolors.ENDC}{bcolors.OKGREEN}{bcolors.UNDERLINE}playing{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}watching{bcolors.ENDC}{bcolors.OKGREEN}, {bcolors.UNDERLINE}competing{bcolors.ENDC}{bcolors.OKGREEN}, or {bcolors.UNDERLINE}listening{bcolors.ENDC}
{bcolors.OKGREEN}config.json {bcolors.OKCYAN}Line 4
""")

intents = discord.Intents.all()
class productivity(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix = '.',
            intents = intents,
            token = token,
            activity = _activity,
            status = _status
        )

    async def on_ready(self):
        print(f'{client.user} is connected!')

        print("Attempting to check local tables...")
        await check_tables()
        print("Checked!")

        print('Attempting to sync slash commands...')
        await self.tree.sync()
        await self.tree.sync(guild=discord.Object(id=admin_guild_id))
        print('Synced')

    async def setup_hook(self):
        for extension in initial_extensions:
            await self.load_extension(extension)
        teams.start()
        urgent.start()

client = productivity()

messageChannel = 0

#Send teams to-do list at noon CST every day
@tasks.loop(seconds = 5)
async def teams():
    await client.wait_until_ready()

    sent = False
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute('SELECT * from teamsToDo')
    goals = await cursor.fetchall()
    for goal in goals:
        roleID = goal[2]
        title = goal[3]
        description = goal[4]
        channel = client.get_channel(messageChannel)
        role = channel.guild.get_role(roleID)

        time = datetime.now()

        embed = discord.Embed(title=f"{title}", 
                            description=f"\n{role.mention}\n\n{description}",
                            color=discord.Color.green())

        if time.hour == 12 and time.minute == 00 and time.second < 6 and sent == False:
            await channel.send(content=role.mention, embed=embed)

#Send urgent to-do list at noon and midnight CST every day
@tasks.loop(seconds = 5)
async def urgent():
    await client.wait_until_ready()

    sent = False
    db = await aiosqlite.connect('database.db')
    cursor = await db.execute('SELECT * from urgentToDo')
    goals = await cursor.fetchall()
    for goal in goals:
        roleID = goal[2]
        title = goal[3]
        description = goal[4]
        channel = client.get_channel(messageChannel)
        role = channel.guild.get_role(roleID)

        time = datetime.now()

        embed = discord.Embed(title=f"{title}", 
                            description=f"\n{role.mention}\n\n{description}",
                            color=discord.Color.green())

        if time.hour == 12 and time.minute == 00 and time.second < 6 and sent == False:
            await channel.send(content=role.mention, embed=embed)

        if time.hour == 00 and time.minute == 00 and time.second < 6 and sent == False:
            await channel.send(content=role.mention, embed=embed)

client.run(token)