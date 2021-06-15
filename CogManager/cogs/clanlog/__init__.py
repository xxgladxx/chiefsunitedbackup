from .clanlog import ClanLog

async def setup(bot):
    cog = ClanLog(bot=bot)
    await cog.crtoken()
    bot.add_cog(cog)
