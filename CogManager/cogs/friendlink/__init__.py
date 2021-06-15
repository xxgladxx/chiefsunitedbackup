from .friendlink import friendlink

async def setup(bot):
    cog = friendlink(bot=bot)
    await cog.crtoken()
    bot.add_cog(cog)