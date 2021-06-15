import discord
from redbot.core import commands
from redbot.core import checks
from typing import Optional


class SimpleEmbed(commands.Cog):
	"""Simply send embeds."""
	def __init__(self, bot):
		self.bot = bot
	
	@checks.has_permissions(manage_messages=True)
	@commands.bot_has_permissions(embed_links=True)
	@commands.command()
	async def sendembed(self, ctx, color: Optional[discord.Color]=None, *, text):
		"""
		Send an embed.
		
		Use the optional parameter `color` to change the color of the embed.
		The embed will contain the text `text`.
		All normal discord formatting will work inside the embed.
		Send the optional image with the command to insert an image at the bottom of the embed.
		"""
		if color is None:
			color = await ctx.embed_color()
		embed = discord.Embed(
			description=text,
			color=color
		)
		if ctx.message.attachments:
			content = await ctx.message.attachments[0].to_file()
			embed.set_image(url="attachment://" + str(content.filename))
		await ctx.send(embed=embed, file=content if ctx.message.attachments else None)
		try:
			await ctx.message.delete()
		except discord.Forbidden:
			pass

	async def red_delete_data_for_user(self, **kwargs):
		"""Nothing to delete."""
		return
	def goodEmbed(self, text):
		gembed = discord.Embed(color=0x45cafc)
		gembed.set_author(name=text, icon_url="https://i.imgur.com/qYmbGK6.png")
		return gembed  

	@commands.command()
	async def shop(self, ctx):
		embed = discord.Embed(title="Invite", url = "https://discord.gg/nKarkppYsy", description = "🛒The Shop🛒", color = 0x00ff59)
		embed.set_author(name="Chiefs United!", url="https://discord.gg/nKarkppYsy", icon_url="https://media.discordapp.net/attachments/819989548879708171/823505579691474954/download.png")
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/754780357349605467/760462448846831646/image1.png?width=473&height=473")
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!buyrole - Buy a Custom Role", value="5M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!buy 1 - Add custom emoji to your name", value="50k Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!buy 2 - Make your own custom command", value="5M Chiefs Coins", inline =False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)

		embed.add_field(name="!buy 3 - Buy Rare role", value="60k Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!buy 4 - Buy Epic Role [rare req]", value= "75k Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!buy 5 - Buy Legendary Role [epic req]", value="1M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)

		embed.add_field(name="!buy 6 - Buy Pass Royale [leggy req]", value="10M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="!buy 7 - Buy Nitro Classic [leggy req]", value="10M Chiefs Coins", inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)


		embed.set_footer(text="Bot by Gladiator#0004", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
		await ctx.send(embed = embed)


	@commands.command()
	async def selfrolesxyz(self, ctx):
		embed = discord.Embed(title="Invite", url = "https://discord.gg/nKarkppYsy", description = "__Self Roles Menu__", color = 0x00ff59)
		embed.set_author(name="Chiefs United!", url="https://discord.gg/nKarkppYsy", icon_url="https://cdn.discordapp.com/emojis/712055480393924678.gif?v=1")
		embed.set_thumbnail(url="https://media.discordapp.net/attachments/754780357349605467/760462448846831646/image1.png?width=473&height=473")
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200B", value="Clash Royale Official news {}".format('<:bluecrown:828933130928914432>'), inline=False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200b", value="RoyaleAPI Official updates {}".format('<:api:821788682205266002>'), inline =False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200b", value="Get notified when someone gets GC 12 wins {}".format('<:gc:821787008623050773>'), inline=False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200b", value= "Get notified when someone gets CC 12 wins {}".format('<:cc:821787009110638602>'), inline=False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200b", value="Get notified when a Heist begins {}".format('<:moneyop:843720716817530920>'), inline=False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name=":video_game:", value="Get notified when a Roulette match begins", inline=False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200b", value="Get pinged when someone starts a duel {}".format('<:battle:830120936426438706>'), inline=False)
		#embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.add_field(name="\u200b", value="Casino role, maybe you can win allin, MAYBE! {}".format('<:cashbag:843721631200837652>'), inline=False)
		embed.add_field(name="\u200B", value="\u200B", inline =False)
		embed.set_footer(text="Bot by Gladiator#0004", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
		await ctx.send(embed = embed)

	@commands.command()
	async def registerme(self, ctx):
		message = ctx.message
		await message.add_reaction("<a:tick:822032492395102209>")
		role = discord.utils.get(ctx.author.guild.roles, name="2v2_registered")
		await discord.Member.add_roles(ctx.author, role)
		await ctx.author.send(embed = self.goodEmbed("Thanks for registering in Chiefs Duo Combat!"))
