from .fl import FL

async def setup(bot):
    cog = FL(bot=bot)
    await cog.crtoken()
    bot.add_cog(cog)

