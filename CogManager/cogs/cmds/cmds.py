# Discord
import discord
import random
import asyncio

# Red
from redbot.core import commands
from redbot.core import checks

# Libs 
from random import choice as rnd

BaseCog = getattr(commands, "Cog", object)

__version__ = "2018.9.0"
__author__ = "Gladiator"

gifs = [
    "https://i.imgur.com/YTGnx49.gif",
    "https://i.imgur.com/U37wHs9.gif",
    "https://i.imgur.com/BU2IQym.gif",
    "https://i.imgur.com/yp6kqPI.gif",
    "https://i.imgur.com/uDyehIe.gif",
    "https://i.imgur.com/vG8Vuqp.gif",
    "https://i.imgur.com/z4uCLUt.gif",
    "https://i.imgur.com/ZIRC9f0.gif",
    "https://i.imgur.com/s8m4srp.gif",
    "https://i.imgur.com/LKvNxmo.gif",
    "https://i.imgur.com/j4W4GFt.gif",
    "https://i.imgur.com/75bX4A1.gif",
    "https://i.imgur.com/dSlfpe3.gif",
    "https://i.imgur.com/JjxaT8e.gif",
    "https://i.imgur.com/QWBlOaQ.gif",
    "https://i.imgur.com/5448px6.gif",
    "https://i.imgur.com/4WJRAGw.gif",
    "https://i.imgur.com/v1sSh5r.gif"
]

failmsgs = [
    "{author} is trying to pat non-existent entity ... and failed.",
    "{author}: *pats non-existent entity*. This bad boy can accept so many pats.",
    "To be honest, I don't know what's {author} been smoking, but sorry, you can't pat non-existent entity",
    "Oh come on, is it that hard to correctly use this command?",
    "You must pat valid and existing user. Try using @ mention, username or nickname.",
    "(╯°□°）╯︵ ┻━┻"
]

patmsgs = [
    "**{user}** got a pat from **{author}**",
    "**{author}** affectionately pat **{user}**",
    "Without hesitation, **{author}** pats **{user}** with love"
]


class PDA(BaseCog):
    """Public Display of Affection ~!"""

    def __init__(self, bot):
        self.gifs = gifs
        self.failmsgs = failmsgs
        self.version = __version__
        self.author = __author__

    @commands.command()
    @commands.cooldown(6, 60, commands.BucketType.user)
    async def pat(self, ctx, *, user: discord.Member=None):
        """Pat users."""
        author = ctx.author

        if not user:
            message = rnd(self.failmsgs)
            await ctx.send(message.format(author=author.name))
        else:
            message = rnd(patmsgs)
            pat = discord.Embed(description=message.format(user=user.name, author=author.name), color=discord.Color(0xffb6c1))
            pat.set_image(url=rnd(self.gifs))
            await ctx.send(embed=pat)

    @commands.command(name="pdaver", hidden=True)
    async def _pda_version(self, ctx):
        """Show PDA version"""
        ver = self.version
        await ctx.send("You are using PDA version {}".format(ver))
        
    @commands.command()
    async def hug(self, ctx, member: discord.Member):
        """Hug your senpai/waifu!"""
        author = ctx.author.mention
        mention = member.mention
        
        hug = "**{0} gave {1} a hug!**"
        
        choices = ['http://i.imgur.com/sW3RvRN.gif', 'http://i.imgur.com/gdE2w1x.gif', 'http://i.imgur.com/zpbtWVE.gif', 'http://i.imgur.com/ZQivdm1.gif', 'http://i.imgur.com/MWZUMNX.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour.blue())
        embed.set_image(url=image)

        await ctx.send(embed=embed)

    @commands.command()
    async def mongoop(self, ctx):
        """"""
        
        embed = discord.Embed(colour=discord.Colour.blue(), description="No doubt!")
        embed.set_author(name="Yeeet!")
        embed.set_image(url="https://cdn.discordapp.com/attachments/823464413910532109/828225135575302154/image0-removebg-preview.png")

        await ctx.send(embed=embed)
                        
    @commands.command()
    async def yerzop(self, ctx):
        """"""
        
        embed = discord.Embed(colour=discord.Colour.red(), description="No doubt!")
        embed.set_author(name="Woop Woop!")
        embed.set_image(url="https://media.discordapp.net/attachments/823464413910532109/830035332681433098/image0-removebg-preview.png")

        await ctx.send(embed=embed)

    @commands.command()
    async def daanop(self, ctx):
        """"""
        
        embed = discord.Embed(colour=discord.Colour.red(), description="Shhh:shushing_face:")
        embed.set_author(name="Mr.077!")
        embed.set_image(url="https://images-ext-1.discordapp.net/external/Fdhoqi1vHm7lG3OnxZhciPZTvANebp5S3dL7y05OA9w/%3Fv%3D1/https/cdn.discordapp.com/emojis/692943147273027665.gif")

        await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member):
        """slapping stuff"""
        author = ctx.author.mention
        mention = member.mention
        if member.id == 822419904992641044: 
                hug = "**Magic! {1} slapped {0} in return.**"
        else:
                hug = "**{0} slapped {1} pretty hard!**"
        
        choices = ['https://i.imgur.com/oOCq3Bt.gif', 'https://i.imgur.com/o2SJYUS.gif', 'https://i.imgur.com/4MQkDKm.gif', 'https://i.imgur.com/fm49srQ.gif', 'https://i.imgur.com/mIg8erJ.gif']
        
        image = random.choice(choices)
        
        embed = discord.Embed(description=hug.format(author, mention), colour=discord.Colour.green())
        embed.set_image(url=image)

        await ctx.send(embed=embed)

    @commands.command()
    async def icon(self, ctx):
       await ctx.send(ctx.guild.icon_url)

    @commands.command()
    async def killerop(self, ctx):
        """"""
        
        embed = discord.Embed(colour=discord.Colour.red(), description="KILLER here!")
        embed.set_author(name="Silence please :knife::drop_of_blood:")
        embed.set_image(url="https://media.discordapp.net/attachments/822436925486792739/846594675338903552/1621914274934.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def dueldecks(self, ctx):
        embed = discord.Embed(color = discord.Colour.green())
        embed.add_field(name = "Decks:", value = " [1(a)]({})\t\t[2(a)]({})\t\t[3(a)]({})\n\n[1(b)]({})\t\t[2(b)]({})\t\t[3(b)]({})".format('https://link.clashroyale.com/deck/en?deck=28000001;26000045;27000010;26000023;27000003;28000007;26000014;26000042','https://link.clashroyale.com/deck/en?deck=26000015;26000006;26000029;26000039;28000009;27000007;26000010;28000008','https://link.clashroyale.com/deck/en?deck=28000004;28000013;26000038;26000030;28000006;26000026;26000010;28000008','https://link.clashroyale.com/deck/en?deck=26000030;27000003;26000014;28000009;26000026;26000036;26000017;26000043','https://link.clashroyale.com/deck/en?deck=26000015;26000009;28000007;28000011;26000005;27000007;26000010;26000042','https://link.clashroyale.com/deck/en?deck=28000004;28000005;26000038;27000003;28000006;26000014;28000003;26000011'))
        embed.set_image(url = "https://media.discordapp.net/attachments/834072063504416819/846607443693535232/dck.jpg?width=1025&height=317")
        await ctx.send(embed=embed)


    @checks.is_owner()
    @commands.command()
    async def rollthewheel(self, ctx):
        await ctx.send("Wear your seatbelts @everyone", allowed_mentions = discord.AllowedMentions(everyone=True))
        await asyncio.sleep(5)
        embed = discord.Embed(title="Chiefs Wheel:", description = "Good Luck to everyone who's participating!", color = discord.Colour.green())
        embed.set_author(name = "Chiefs v1!")
        embed.set_image(url = "https://media.discordapp.net/attachments/838798651747729408/851341948034875422/Screenshot__352_-removebg-preview.png?width=476&height=473")
        msg = await ctx.send(embed = embed)
        

        embed1 = discord.Embed(title="Chiefs Wheel!", description = "Now rolling at the speed of 69 million miles per hour..", color = discord.Colour.green())
        embed1.set_author(name = "Chiefs v1!")
        embed1.set_image(url = "https://media.discordapp.net/attachments/838798651747729408/851351918479278140/giphy_3.gif")
        ctx.typing()
        await asyncio.sleep(20)
        await msg.edit(embed = embed1)
        await asyncio.sleep(15)
        ctx.typing()
        choices = ['RidAK#0443', '5h1u9?9#0443', 'A Random Person#0894', 'NoOne#7078', 'Drastic_Kilr#6687', 'ashdilly26#4125', 'Ross XD#9730', 'G3N3T1KZz#4090', 'DarkElement#4231', 'TheCoy#0833', 'Abinay#4910', 'wizard9666#0685', 'DaAdy ChilL#1301', 'Iamloa#7618', 'THE3NDIK?:registered:#3294']
        winner = random.choice(choices)
        embed2 = discord.Embed(title = "And the Winner of this giveaway is none other than @{}".format(str(winner)), description = "DM the Leader to claim your prize:kissing_heart:", color = discord.Colour.green())

        embed2.set_image(url = "https://cdn.discordapp.com/emojis/722539392341639208.png?v=1")
        await ctx.send(embed = embed2)
        return await ctx.send("Also thanks to everyone who participated, stay tuned for more such giveaways ;)")




