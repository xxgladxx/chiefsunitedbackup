import discord
import re
import urllib.parse as urlparse
import clashroyale
from redbot.core import commands

creditIcon = "https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473"
credits = "Bot for Chiefs United!"


class friendlink(commands.Cog):
    """Automatically convert Clash Royale to beautiful embeds"""

    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants

    async def crtoken(self):
        # Clash Royale API config
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Make sure to have royaleapi ip added (128.128.128.128) Use !set api "
                  "clashroyale token,YOUR_TOKEN to set it")
        self.clash = clashroyale.official_api.Client(token=token['token'], is_async=True,
                                                     url="https://proxy.royaleapi.dev/v1")

    def emoji(self, name):
        """Emoji by name."""
        for emoji in self.bot.get_all_emojis():
            if emoji.name == name:
                return '<:{}:{}>'.format(emoji.name, emoji.id)
        return ''

    commands.Cog.listener()
    async def FL(self, message):


        if "https://link.clashroyale.com/invite/friend/" in message.content:
              ftag = message.content.index('=') + 1
              fand = message.content.index('&')
              profiletag = '#' + message.content[ftag:fand]
              try:
                  profiledata = await self.clash.get_player(profiletag)
              except clashroyale.RequestError:
                  return await ctx.send('Unable to reach CR servers')


              embed = discord.Embed(title='Click this link to add as friend in Clash Royale!', url=url[0], color=0x0080ff)
              embed.set_author(name=profiledata.name + " (" + profiledata.tag + ")", icon_url=await self.constants.get_clan_image(profiledata))
              embed.set_thumbnail(url="https://imgur.com/C9rLoeh.jpg")
              embed.add_field(name="User", value=message.author.mention, inline=True)
              embed.add_field(name="Trophies", value="{} {:,}".format(self.emoji(arenaFormat), profiledata.trophies), inline=True)
              embed.add_field(name="Level", value=self.emoji("level{}".format(profiledata.expLevel)), inline=True)
              if profiledata.clan is not None:
                  embed.add_field(name="Clan {}".format(profiledata.role.capitalize()),
                                  value="{} {}".format(self.emoji("clan"), profiledata.clan.name),
                                  inline=True)
              embed.set_footer(text=credits, icon_url=creditIcon)
              await self.bot.delete_message(message)
              await self.bot.send_message(message.channel, embed=embed)
