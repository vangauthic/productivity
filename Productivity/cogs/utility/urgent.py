import discord
import aiosqlite

from discord import app_commands
from discord.ext import commands

class urgent(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="urgent", description="Create a new urgent goal in the to-do list!")
    @commands.has_permissions(administrator=True)
    @app_commands.describe(role="The team required for the goal")
    @app_commands.describe(title="The title of the goal")
    @app_commands.describe(description="The description of the goal")
    async def urgent(self, interaction: discord.Interaction, role: discord.Role, title: str, description: str):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM urgentToDo WHERE title=?', (title.upper(),))

            if await cursor.fetchone() is None:
                await db.execute('INSERT INTO urgentToDo (role, roleID, title, description) VALUES (?,?,?,?)', (role.name, role.id, title.upper(), description))
                await db.commit()
                embed = discord.Embed(title=f"Created New Urgent Goal", 
                                      description=f"\n\nYou have succesfully created the goal: **{title.upper()}** assigned to {role.mention}",
                                      color=discord.Color.orange())
            else:
                embed = discord.Embed(title=f"Urgent Goal Already Exists", 
                                      description=f"\n\nA goal with the name **{title.upper()}** already exists! Please choose a new title.",
                                      color=discord.Color.red())
                
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(urgent(bot))