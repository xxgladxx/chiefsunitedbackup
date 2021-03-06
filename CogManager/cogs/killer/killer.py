import discord
import random
import time
from redbot.core import commands


class Killer(commands.Cog):
    """Do unto others as you would have them do unto you"""

    def getActors(self, bot, killer, target):
        return {'id': bot.id, 'nick': bot.display_name, 'formatted': bot.mention}, {'id': killer.id, 'nick': killer.display_name, 'formatted': "<@{}>".format(killer.id)}, {'id': target.id, 'nick': target.display_name, 'formatted': target.mention}

    # SLAP
    @commands.command()
    async def slap(self, ctx, *, user: discord.Member):
        """Open hand, not a closed fist!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to slap the bot, eh?

            message1 = "{} looks at {}... βπ π€".format(
                killer['nick'], bot['nick'])
            message2 = "but {} suddenly slaps {} with his silver sword! π΅π« ππ€".format(
                bot['nick'], killer['nick'])

        elif killer['id'] == target['id']:  # wants to slap themselves

            message1 = "{} looks themselves in the mirror... πΌπ".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and smashes their head against it! β¨πΌπ₯π«"

            elif diceroll > 10:
                message2 = "and gently pats their cheeks to wake up! πΌπ"

            else:
                message2 = "and trips on the wet floor! Ouch! π€"

        else:  # wants to slap another user

            message1 = "{} raises their hand... βπ".format(killer['nick'])

            if diceroll > 89:
                message2 = "and mutilates {}! Oh my god, there's blood everywhere! π΅π₯π€π‘".format(
                    target['formatted'])

            elif diceroll > 50 and diceroll < 55:
                message2 = "and gives {} a romantic spanking ππ ππ".format(
                    target['formatted'])

            elif diceroll > 10:
                message2 = "and slaps {} senseless! π«π«ππ ".format(
                    target['formatted'])

            else:
                message2 = "and misses! So stupid! πππ¨ π"

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    # PUNCH
    @commands.command()
    async def punch(self, ctx, *, user: discord.Member):
        """Open up a can of whoop-ass on a user!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to punch the bot, eh?

            message1 = "{} waves their fists at {}... π€ βπ§".format(
                killer['nick'], bot['nick'])
            message2 = "but {} casts Igni on {}! π€ π₯π«π₯".format(
                bot['nick'], killer['formatted'])

        elif killer['id'] == target['id']:  # wants to punch themselves

            message1 = "{} looks at their own fist... πβ".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and bashes their head through the nearest wall! π«β?π₯"
            elif diceroll > 69:
                message2 = "and bashes their head against it until its broken! π‘π«π€"
            elif diceroll > 10:
                message2 = "and repeatedly hits themselves with their pathetic little hands π€π£π€"
            else:
                message2 = "tries to throw a punch, but misses and breaks their ankle! βΉοΈπ¦΅"

        else:  # wants to punch another user

            message1 = "{} raises their fists towards {}... π§ βπ ".format(
                killer['formatted'], target['formatted'])

            if diceroll > 89:
                message2 = "\"Omae wa mou shindeiru\", says {}, before {} explodes into a cloud of blood and guts. π₯π€―π₯ ππ".format(
                    killer['formatted'], target['formatted'])

            elif diceroll > 59:
                message2 = "and a flurry of punches break every bone in {}'s body! Ora! Ora! Ora! Ora! π£π€π€π€ π‘".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and punches {}Β right in the face! Hard! π£π€ π ".format(
                    target['formatted'])
            else:
                message2 = "and trips on a banana peel! Doofus! π€£π ππ"

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    # STAB
    @commands.command()
    async def stab(self, ctx, *, user: discord.Member):
        """Turn a user into shish kebab!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # tryng to shoot the bot, eh?

            message1 = "{} raises their dagger at {}... π πͺ π€".format(
                killer['nick'], bot['nick'])
            message2 = "but {} teleports behind {} and strikes! π΅π« βοΈπ€ {}".format(
                bot['nick'], killer['formatted'], '`"Nothing personell, kid"`')

        elif killer['id'] == target['id']:  # wants to slap themselves

            message1 = "{} holds a knife against their abdomen...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and cuts their own head off! How is that even possible!? ππ"
            elif diceroll > 10:
                message2 = "and commits sudoku! πͺπ΅"
            else:
                message2 = "and accidentally cuts their finger on a hentai magazine! ππ« {}-no skebe!".format(
                    target['nick'])

        else:  # wants to slap another user

            message1 = "{} raises their dagger... ππͺ πΆ".format(killer['nick'])

            if diceroll > 89:
                message2 = "and turns {} into a sheesh kebab! RIP in pieces! π‘πͺ π£ π΅ π€ π π β".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and stabs {}! Yikes! π πͺπ₯ βπ΅π€".format(
                    target['formatted'])
            elif diceroll > 5:
                message2 = "but {} dodges like a ninja! ππ¨ ππͺ".format(
                    target['formatted'])
            else:
                message2 = "and cuts his own hand off! What an amateur! ππͺπ€ π"

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    # SHOOT
    @commands.command()
    async def shoot(self, ctx, *, user: discord.Member):
        """Shoot another user (or yourself) dead!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if (target['id'] == bot['id']):  # tryng to shoot the bot, eh?

            message1 = "{} aims their gun, pulls the trigger...".format(
                killer['nick'])
            message2 = "but {} shot first! π΅ π₯π«π€".format(bot['nick'])

        elif killer['id'] == target['id']:  # wants to kill themselves

            message1 = "{} holds a gun to their head, pulls the trigger...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and explodes! Boom! Splat! What a mess! π₯π΅π₯"
            elif diceroll > 30:
                message2 = "and commits sudoku! π₯π΅π«"
            elif diceroll > 20:
                message2 = "and KYSed themselves! π₯π΅π«"
            elif diceroll > 10:
                message2 = "and somehow didn't miss! At least this idiot is good for something! π₯π΅π«"
            else:
                message2 = "and misses! What an idiot! Should've aimed at the temple! π₯π«π―"

        else:  # wants to kill other user

            message1 = "{} aims their gun, pulls the trigger...".format(
                killer['nick'])

            if diceroll > 89:
                message2 = "and {} explodes into a red, gut-ridden, eyeball-strewn paste. Fun!!! π₯π΄ π«π€ ".format(
                    target['formatted'])
            elif diceroll > 75:
                message2 = "and shoots {} in the head! Bang! π₯π΅ π«π".format(
                    target['formatted'])
            elif diceroll > 10:
                message2 = "and shoots {} dead! π± π₯π«π".format(
                    target['formatted'])
            elif diceroll > 5:
                message2 = "and misses {}! Doh! π π¨π«π£".format(
                    target['formatted'])
            else:
                message2 = "and shoots themselves instead of {}! LOL! π€£ π₯π΅π«".format(
                    target['formatted'])

        await ctx.send(message1)
        time.sleep(1)
        await ctx.send(message2)

    # LOVE
    @commands.command()
    async def love(self, ctx, *, user: discord.Member):
        """Show some affection for once!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # love the bot
            message = "{} loves {} π π€".format(killer['nick'], bot['nick'])
        elif killer['id'] == target['id']:  # loves themselves
            message = "{} loves themselves, because nobody else does π".format(
                killer['nick'])
        else:
            if diceroll > 90:
                message = "{} and {} sitting under a tree... π".format(
                    killer['formatted'], target['formatted'])
            elif diceroll > 10:
                message = "{} loves {} aww... π π".format(
                    killer['formatted'], target['formatted'])
            else:
                message = "{} loves {}, but not in return π­ π".format(
                    killer['formatted'], target['formatted'])

        await ctx.send(message)

    # SEX
    @commands.command()
    async def sex(self, ctx, *, user: discord.Member):
        """Sex a user, because there's no NSFW channel!"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # sex the bot
            if diceroll > 89:
                message = "{} is taken by {} on top of a stuffed unicorn ππ¦π€".format(
                    killer['formatted'], bot['nick'])
            else:
                message = "Everbody wants to sex {}, get in line, loser!".format(
                    bot['nick'])
        elif killer['id'] == target['id']:  # sex themselves
            message = "{} does as they are told and f***s themselves π".format(
                killer['formatted'])
        else:
            message = "This is a Christmas Discord, get a room! π"

        await ctx.send(message)

    # SUCC
    @commands.command()
    async def succ(self, ctx, *, user: discord.Member):
        """Succ a user like a lollipop"""

        bot, killer, target = self.getActors(
            ctx.bot.user, ctx.message.author, user)

        diceroll = random.randint(0, 100)

        if target['id'] == bot['id']:  # succ the bot
            if diceroll > 89:
                message = "{} enjoys {}'s magic juice πππ€".format(
                    killer['formatted'], bot['nick'])
            else:
                message = "You already succ CDPR's dick every day!"
        elif killer['id'] == target['id']:  # succ themselves
            message = "{} succs themselves. Impressive, I guess...".format(
                killer['formatted'])
        else:
            if diceroll > 80:
                message = "Sucks to be you, {}".format(killer['formatted'])
            else:
                message = "This is a Christmas Discord, get a room! π"

        await ctx.send(message)
