import discord
from redbot.core import commands

class GladIsBusy(commands.Cog):

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
      glad = '@Glad..'
        if  glad in message.content:
          if message.author.id != 433195170343682048 or message.author.id != 520275271182712842:
            await message.channel.send("{}, Glad.. might take longer than usual to respond.\nLots of homework :new_moon_with_face:".format(message.author))
