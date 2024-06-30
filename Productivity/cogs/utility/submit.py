import discord
import aiosqlite

from discord import app_commands
from discord.ext import commands

class submit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="submit", description="Create a new goal in the to-do list!")
    @app_commands.describe(goal="The title of the goal you would like to submit")
    async def submit(self, interaction: discord.Interaction, goal: str):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute('SELECT * FROM teamsToDo WHERE title=?', (goal.upper(),))

            if await cursor.fetchone() is None:
                urgent_cursor = await db.execute('SELECT * FROM urgentToDo WHERE title=?', (goal.upper(),))
                if await urgent_cursor.fetchone() is None:
                    embed = discord.Embed(title=f"Invalid Goal", 
                                        description=f"\n\nThe goal **{goal.upper()}** does not exist! Try submitting a different goal.",
                                        color=discord.Color.red())
                else:
                    await db.execute('DELETE FROM urgentToDo WHERE title=?', (goal.upper(),))
                    await db.commit()
                    embed = discord.Embed(title=f"Goal Submitted", 
                                          description=f"\n\nYou have successfully submitted the goal **{goal.upper()}**",
                                          color=discord.Color.green())
            else:
                await db.execute('DELETE FROM teamsToDo WHERE title=?', (goal.upper(),))
                await db.commit()
                embed = discord.Embed(title=f"Goal Submitted", 
                                      description=f"\n\nYou have successfully submitted the goal **{goal.upper()}**",
                                      color=discord.Color.green())
                
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(submit(bot))