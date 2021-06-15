#start
import discord
from redbot.core import commands

class Gen(commands.Cog):
     @commands.command()
     async def genop(self, ctx):
          member = ctx.author
          role = discord.utils.get(member, name="Gen OP")
          await discord.Member.add_roles(member, role)
          await ctx.send("Role has been added!")
