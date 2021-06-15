from redbot.core import commands
import discord

class Mycog(commands.Cog):
    """My custom cog"""

    @commands.command()
    async def dev(self, ctx):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("Hey" + ctx.author + ", the bot is developed by <@698376874186768384>!" )
