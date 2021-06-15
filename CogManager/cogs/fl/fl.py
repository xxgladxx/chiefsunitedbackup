import discord
from redbot.core import commands
import asyncio
import clashroyale
import re
from urllib.parse import unquote

class FL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        self.CRregex = re.compile(r"<?(https?:\/\/)?(www\.)?(link\.clashroyale\.com\/invite\/friend)\b([-a-zA-Z0-9/]*)>?")

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
        name = str(name)
        for emote in self.bot.emojis:
            if emote.name == name.replace(" ", "").replace("-", "").replace(".", ""):
                return '<:{}:{}>'.format(emote.name, emote.id)
        return ''


    @commands.Cog.listener()
    async def on_message_without_command(self, message):
 
      if self.CRregex.search(message.content) is not None:

        ftag = message.content.index('=') +1
        fand = message.content.index('&') 
        profiletag = '#' + message.content[ftag:fand] 
        url1 = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content)
        url = str(url1)
        url = url.strip("['")
        url = url.strip("']")

                       

      try:            
        profiletag = str(profiletag)
      except clashroyale.NotFoundError:
        return await ctx.send("Invalid Tag. Please try again.")

      try:
        profiledata = await self.clash.get_player(profiletag)
      except clashroyale.RequestError:
        return await message.channel.send('Unable to reach CR servers')

      embed = discord.Embed(title="Click the link below to add as friend in Clash Royale!", color=discord.Colour.green())
      embed.set_author(name=profiledata.name + " (" + profiledata.tag + ")", icon_url=await self.constants.get_clan_image(profiledata))
      embed.set_thumbnail(url="https://imgur.com/C9rLoeh.jpg")
      embed.add_field(name="{}".format('<:frnd:830119277935067146>', url), value="{0}[**Link**]({1})".format('<:dot:831131197454286869>', url))
      embed.add_field(name="{}User".format(self.emoji("blueking")), value=message.author.mention, inline=True)
      embed.add_field(name="Trophies", value="{} {}".format(self.emoji("ltrophy"), profiledata.trophies), inline=False)
      embed.add_field(name="Level", value="{}{}".format(self.emoji("exp"), profiledata.expLevel), inline=True)      
      if profiledata.clan is not None:
        embed.add_field(name="Clan {}".format(profiledata.role.capitalize()), value="{}{} ".format(self.emoji("cws"), profiledata.clan.name), inline=True)
      
      embed.set_image(url="https://media.discordapp.net/attachments/760484066381398026/830034046813601823/legend_logo-trans.png?width=150&height=100")
      embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
    
      await message.delete()
      await message.channel.send(embed=embed)


    #@commands.Cog.listener()
    #async def on_message_without_command(self, message):
      #try:
    
        #if '<@698376874186768384>' in str(message.content):
          #if message.author.id != 433195170343682048 or message.author.id != 520275271182712842:
            #await message.channel.send("{}, Glad.. might take longer than usual to respond.\nLots of homework :new_moon_with_face:".format(message.author))

      #except Exception as e:
        #await message.channel.send(e)






