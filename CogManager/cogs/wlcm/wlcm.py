from redbot.core import commands
from redbot.core import checks
import discord

class WLCM(commands.Cog):
    """My custom cog"""
    def __init__(self, bot):
        self.bot = bot
        
        
  #  @commands.Cog.listener()
   # async def on_member_join(self, member : discord.Member) -> None:
        # send a message to welcome channel when a user joins server
    @commands.Cog.listener()
    async def on_member_join(self, member : discord.Member):
        channel = member.guild.get_channel(812319225267355768)
        embed = discord.Embed(color=discord.Colour.green(), description=f"\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2 \n \n Welcome to Chiefs Family! \n {member.mention} \n \n If your main purpose is to Chill and Kill, you are at the right place! \n\n \u27bc Founded on 29th September 2020, we aim for the best clashing experience in a friendly environment. We provide you a wonderful place to hang around with other chiefs. \n \n \u27bc Verify your CR account by doing: \n !save <tag> \n \n \u27bc If you wanna join our alliance, ping a <@&760377944043814942> or <@&760377941807988736> . \n \n \u27bc If you're facing any trouble, ping <@&760484038062112808> in this channel. \n \n Have Fun, \n Clash On! \n \n \u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2\u21e2")
        embed.set_author(name=f"\u2022 Entry Gate \u2022", icon_url="https://media.discordapp.net/attachments/754780357349605467/760477780978434058/image0.gif?width=475&height=475", url="https://discord.gg/WNrSEGVT")
        embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/wtqLXQjEmYQLdwmAUUo0gMMutN6MApAxnfHSqsMds7c/%3Fwidth%3D473%26height%3D473/https/media.discordapp.net/attachments/827982101507866726/829589928807497768/legend_logo-trans.png")
        embed.set_image(url="https://cdn.discordapp.com/emojis/554424099770728472.gif?v=1")
        embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
        await channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(roles=True, users=True))
        await member.send('Join us here : \n <https://link.clashroyale.com/en?clanInfo?id=YGGQR0CV>x')
        channel1 = member.guild.get_channel(830128135202799656)
        await channel1.send("<@&760377941807988736> <@&760377944043814942>, \n {} is waiting for you in <#812319225267355768>".format(member.mention), allowed_mentions=discord.AllowedMentions(roles=True, users=True))

   # @commands.command()
   # @checks.admin_or_permissions(manage_guild=True)
   # async def app(self, ctx, member : discord.Member = None):
    #    if member is None:
     #       member = ctx.author
      #  embed = discord.Embed(color=discord.Colour.blue(), description=f"Hey there {member.mention}!")
      #  embed.set_author(name="Chiefs United!", icon_url="https://media.discordapp.net/attachments/754780357349605467/760477780978434058/image0.gif?width=473&height=473")
      #  embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/598503254351020032.png?v=1")
       # embed.add_field(name=f"We're more than happy to have you approved as a Chief! \nPlease click the link below to join our clan.", value=f"<:star:827893695047139348> [\u2022\u2022\u2022\u2022\u2022](https://link.clashroyale.com/en?clanInfo?id=YGGQR0CV%27) <:star:827893695047139348>")
       # embed.set_image(url="https://images-ext-1.discordapp.net/external/wtqLXQjEmYQLdwmAUUo0gMMutN6MApAxnfHSqsMds7c/%3Fwidth%3D473%26height%3D473/https/media.discordapp.net/attachments/827982101507866726/829589928807497768/legend_logo-trans.png")
       # embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
       # await member.send(embed=embed, allowed_mentions=discord.AllowedMentions(roles=True, users=True))

