from .cbot import Cleverbotcog


def setup(bot):
    bot.add_cog(Cleverbotcog(bot))
