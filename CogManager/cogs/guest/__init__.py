from .guest import Guest

async def setup(bot):
  cog = Guest(bot)
  await cog.crtoken()
  bot.add_cog(cog)
