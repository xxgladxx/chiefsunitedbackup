from attr import __description__
import discord
import clashroyale
from redbot.core import commands, checks, Config
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from redbot.core import Config, checks, commands
from redbot.core.data_manager import bundled_data_path, cog_data_path
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from redbot.core.utils.predicates import MessagePredicate
from io import BytesIO
import numpy as np
import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.embed import randomize_colour
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from random import choice
import clashroyale
from json import load
from redbot.core.data_manager import bundled_data_path
import io


class ClashRoyale(commands.Cog):
    """Clash royale commands and functions"""

    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        self.cards = self.bot.get_cog('Deck').cards

    async def crtoken(self):
        # Clash Royale API config
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Make sure to have royaleapi ip added (128.128.128.128) Use !set api "
                  "clashroyale token,YOUR_TOKEN to set it")
        self.clash = clashroyale.official_api.Client(token=token['token'], is_async=True,
                                                     url="https://proxy.royaleapi.dev/v1")

    def cog_unload(self):
        if self.clash:
            self.bot.loop.create_task(self.clash.close())

    def getCards(self, maxPlayers):
        """Converts maxPlayers to Cards
        Credit Gr8"""
        cards = {
            "50": 25,
            "100": 100,
            "200": 400,
            "1000": 2000
        }
        return cards[str(maxPlayers)]

    def getArenaEmoji(self, trophies):
        """Get Arena and League Emoji"""
        arenaMap = {
            "arena1": [0, 299],
            "arena2": [300, 599],
            "arena3": [600, 999],
            "arena4": [1000, 1299],
            "arena5": [1300, 1599],
            "arena6": [1600, 1999],
            "arena7": [2000, 2299],
            "arena8": [2300, 2599],
            "arena9": [2600, 2999],
            "arena10": [3000, 3299],
            "arena11": [3300, 3599],
            "arena12": [3600, 4199],
            "arena13": [4200, 4599],
            "arena14": [4600, 4999],

            "league1": [5000, 5299],
            "league2": [5300, 5599],
            "league3": [5600, 5999],
            "league4": [6000, 6299],
            "league5": [6300, 6599],
            "league6": [6500, 6999],
            "arena19": [7000, 7299],
            "league7": [7200, 7699],
            "league8": [7600, 7999],
            "league9": [8000, 99999]
        }
        for arena in arenaMap.keys():
            if arenaMap[arena][0] <= trophies <= arenaMap[arena][1]:
                return self.emoji(arena)


    def getArenaEmoji1(self, trophies):
        """Get Arena and League Emoji"""
        arenaMap = {
            "arena1": [0, 299],
            "arena2": [300, 599],
            "arena3": [600, 999],
            "arena4": [1000, 1299],
            "arena5": [1300, 1599],
            "arena6": [1600, 1999],
            "arena7": [2000, 2299],
            "arena8": [2300, 2599],
            "arena9": [2600, 2999],
            "arena10": [3000, 3299],
            "arena11": [3300, 3599],
            "arena12": [3600, 4199],
            "arena13": [4200, 4599],
            "arena14": [4600, 4999],

            "league1": [5000, 5299],
            "league2": [5300, 5599],
            "league3": [5600, 5999],
            "league4": [6000, 6299],
            "league5": [6300, 6599],
            "league6": [6500, 6999],
            "arena19": [7000, 7299],
            "league7": [7200, 7699],
            "league8": [7600, 7999],
            "league9": [8000, 99999]
        }
        for arena in arenaMap.keys():
            if arenaMap[arena][0] <= trophies <= arenaMap[arena][1]:
                return self.emoji1(arena)


    def getArenaImageXXX(self, trophies):
        """Get Arena and League Emoji"""
        arenaMap = {
            "arena1": [0, 299],
            "arena2": [300, 599],
            "arena3": [600, 999],
            "arena4": [1000, 1299],
            "arena5": [1300, 1599],
            "arena6": [1600, 1999],
            "arena7": [2000, 2299],
            "arena8": [2300, 2599],
            "arena9": [2600, 2999],
            "arena10": [3000, 3299],
            "arena11": [3300, 3599],
            "arena12": [3600, 4199],
            "arena13": [4200, 4599],
            "arena14": [4600, 4999],

            "league1": [5000, 5299],
            "league2": [5300, 5599],
            "league3": [5600, 5999],
            "league4": [6000, 6299],
            "league5": [6300, 6599],
            "league6": [6500, 6999],
            "arena19": [7000, 7299],
            "league7": [7200, 7699],
            "league8": [7600, 7999],
            "league9": [8000, 99999]
        }
        for arena in arenaMap.keys():
            if arenaMap[arena][0] <= trophies <= arenaMap[arena][1]:
                return 'https://royaleapi.github.io/cr-api-assets/arenas/' + arena + '.png'

    def getArenaImage(self, trophies):
        """Get Arena and League Emoji"""
        arenaMap = {
            "arena1": [0, 299],
            "arena2": [300, 599],
            "arena3": [600, 999],
            "arena4": [1000, 1299],
            "arena5": [1300, 1599],
            "arena6": [1600, 1999],
            "arena7": [2000, 2299],
            "arena8": [2300, 2599],
            "arena9": [2600, 2999],
            "arena10": [3000, 3299],
            "arena11": [3300, 3599],
            "arena12": [3600, 4199],
            "arena13": [4200, 4599],
            "arena14": [4600, 4999],

            "league1": [5000, 5299],
            "league2": [5300, 5599],
            "league3": [5600, 5999],
            "league4": [6000, 6299],
            "league5": [6300, 6599],
            "league6": [6500, 6999],
            "arena19": [7000, 7299],
            "league7": [7200, 7699],
            "league8": [7600, 7999],
            "league9": [8000, 99999]
        }
        for arena in arenaMap.keys():
            if arenaMap[arena][0] <= trophies <= arenaMap[arena][1]:
                return 'https://gladcr.github.io/assetsv1/' + arena + '.png'


    def getCoins(self, maxPlayers):
        """Converts maxPlayers to Coins
        credit """
        coins = {
            "50": 175,
            "100": 700,
            "200": 2800,
            "1000": 14000
        }
        return coins[str(maxPlayers)]

    def emoji(self, name):
        """Emoji by name."""
        name = str(name)
        for emote in self.bot.emojis:
            if emote.name == name.replace(" ", "").replace("-", "").replace(".", ""):
                return '<:{}:{}>'.format(emote.name, emote.id)
        return ''

    def emoji1(self, name):
        """Emoji by name."""
        name = str(name)
        for emote in self.bot.emojis:
            if emote.name == name.replace(" ", "").replace("-", "").replace(".", ""):
                return '<{}>'.format(emote.id)
        return ''


    def roleNameConverter(self, role):
        """Just makes the role names look better"""
        if role == "leader":
            return "Leader"
        elif role == "coLeader":
            return "Co-Leader"
        elif role == "elder":
            return "Elder"
        else:
            return "Member"

    @commands.command()
    async def clashprofile(self, ctx, user: discord.Member = None, account: int = 1):
        """Show Clash Royale Stats"""

        # todo weird thing !cp accountnum

        if user is None:
            user = ctx.author

        try:
            profiletag = self.tags.getTag(user.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                      "Use !save <tag> to save a tag or that account number doesn't exist,"
                                      " use !accounts to see the accounts you have saved")
            profiledata = await self.clash.get_player(profiletag)
            chests = await self.clash.get_player_chests(profiletag)

        except clashroyale.RequestError:
            return await ctx.send("Error: cannot reach Clash Royale Servers. Please try again later.")


        ccwins, gcwins = 0, 0

        badges_str = '**Badges:** 2020 Player'

        account_age = 'Indeterminate'

        for badge in profiledata.badges:
            if badge.name == 'Classic12Wins':
                ccwins = badge.progress
            elif badge.name == 'Grand12Wins':
                gcwins = badge.progress
            elif badge.name == 'Played1Year':
                account_age = str(badge.progress)
            elif badge.name == 'Played3Years':
                badges_str += ', OG Clash Royale Player'
            elif badge.name == "LadderTournamentTop1000_1":
                badges_str += ', Top 1000 Global Tournament Finish'
            elif badge.name == "LadderTop1000_1":
                badges_str += ', Top 1000 Ladder Finish'

        if profiletag == '9VUCR20UL':
            badges_str += ', Bot Developer'

        if profiledata.current_season is not None:
            if profiledata.current.season.rank is not None: 
              badges_str += ',Currently Top/ {}'.format(profiledata.current_season.rank)          


        games1v1 = profiledata.battle_count - (profiledata.battle_count - (profiledata.wins + profiledata.losses))

        embed = discord.Embed(color=discord.Color.blue(), description=badges_str)
        embed.set_author(name=profiledata.name + " (" + profiledata.tag + ")",
                         icon_url=await self.constants.get_clan_image(profiledata),
                         url="https://royaleapi.com/player/" + profiledata.tag.strip("#"))
        # changed ArenaImage to ArenaEmoji for the time being #embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/{}.png?v=1'self.getArenaImage1(profiledata.trophies))
        embed.set_thumbnail(url=self.getArenaImage(profiledata.trophies))



        embed.add_field(name="Trophies",
                        value="{} {:,}".format(self.emoji("trophycr"), profiledata.trophies),
                        inline=True)

        # todo proper league stats with formatting (rank if applicable, prev season + best season)

        if getattr(profiledata, 'league_statistics', False):
            if not getattr(profiledata.league_statistics.current_season, 'best_trophies', False):
                season_best = profiledata.league_statistics.current_season.trophies
            else:
                season_best = profiledata.league_statistics.current_season.best_trophies
            embed.add_field(name="Season Best", value='{} {:,}'.format(self.emoji("seasonh"),
                                                                       season_best), inline=True)

        embed.add_field(name="Highest Trophies", value="{} {:,}".format(self.getArenaEmoji(profiledata.best_trophies),
                                                                        profiledata.best_trophies), inline=True)
        level = self.emoji("exp{}".format(profiledata.exp_level)) 
        if level is None or level == '':
            level = str(profiledata.exp_level)

        embed.add_field(name="Level", value="{}{}".format(self.emoji("exp"),profiledata.exp_level), inline=True)
        if profiledata.exp_level > 12:
            embed.add_field(name="Star Points",
                            value="{} {:,}".format(self.emoji("lvl"), profiledata.star_points), inline=True)
        if getattr(profiledata, "clan"):
            embed.add_field(name=f"{self.roleNameConverter(profiledata.role)} of",
                            value=f'{self.emoji("clans")} {profiledata.clan.name}')

        total_cards = await self.clash.get_all_cards()
        total_cards = len(total_cards)
        embed.add_field(name="Cards Found", value="{} {}/{}".format(self.emoji("card"), len(profiledata.cards),
                                                                    str(total_cards)),
                        inline=True)
        embed.add_field(name="Favourite Card", value="{} {}".format(self.emoji(profiledata.current_favourite_card.id),
                                                                    profiledata.current_favourite_card.name),
                        inline=True)
        embed.add_field(name="Games Played", value="{} {:,}".format(self.emoji("sword"), profiledata.battle_count),
                        inline=True)
        embed.add_field(name="Tourney Games Played",
                        value="{} {:,}".format(self.emoji("gt"), profiledata.tournament_battle_count), inline=True)
        embed.add_field(name="Wins", value="{} {:,} ({:.1f}%)".format(self.emoji("bc"), profiledata.wins,
                                                                      (profiledata.wins / games1v1) * 100), inline=True)
        embed.add_field(name="Losses", value="{} {:,} ({:.1f}%)".format(self.emoji("rc"), profiledata.losses,
                                                                        (profiledata.losses / games1v1) * 100),
                        inline=True)
        embed.add_field(name="Three Crown Wins",
                        value="{} {:,} ({:.1f}%)".format(self.emoji("3c"), profiledata.three_crown_wins, (
                                    profiledata.three_crown_wins / profiledata.battle_count) * 100), inline=True)
        embed.add_field(name="Friendly Wins",
                        value="{} {:,}".format(self.emoji("frnd"), profiledata.achievements[9].value), inline=True)
        embed.add_field(name="War Day Wins", value="{} {}".format(self.emoji("cws"), profiledata.war_day_wins),
                        inline=True)
        embed.add_field(name="Total Donations", value="{} {:,}".format(self.emoji("card"), profiledata.total_donations),
                        inline=True)
        embed.add_field(name="Donations Recieved",
                        value="{} {:,}".format(self.emoji("cwon"), profiledata.clan_cards_collected), inline=True)
        embed.add_field(name="Challenge Max Wins",
                        value="{} {}".format(self.emoji("maxw"), profiledata.challenge_max_wins), inline=True)
        embed.add_field(name="Grand Challenge Wins", value="{}{}".format(self.emoji("gc"), gcwins), inline=True)
        embed.add_field(name="Classic Challenge Wins", value="{}{}".format(self.emoji("cc"), ccwins), inline=True)
        if account_age != "Indeterminate":
            embed.add_field(name="Account Age", value=f'⏰ {account_age}', inline=True)
        embed.add_field(name="Challenge Cards Won",
                        value="{} {:,}".format(self.emoji("cards"), profiledata.challenge_cards_won), inline=True)
        embed.add_field(name="Tournament Cards Won",
                        value="{} {:,}".format(self.emoji("ltrophy"), profiledata.tournament_cards_won), inline=True)
        embed.add_field(name="Hosted/Joined Tourneys",
                        value="{} {:,}/{:,}".format(self.emoji("carda"), profiledata.achievements[6].value,
                                                    profiledata.achievements[7].value), inline=True)
        embed.add_field(name="Clans Joined",
                        value="{} {:,}".format(self.emoji("social"), profiledata.achievements[0].value), inline=True)

        embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/jZqqzbGd-oAdn-t2JmmD0XlFJJjUs7e1Hd3phypFhMY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_b5bce61cbada3a988140b5b93c6b7966.gif?width=473&height=473")

        await ctx.send(embed=embed)

    @commands.command(aliases=['clashdeck'])
    async def clashDeck(self, ctx, member: discord.Member = None, account: int = 1):
        """View yours or other's clash royale Deck"""
        member = member or ctx.message.author
        await ctx.trigger_typing()
        try:
            profiletag = self.tags.getTag(member.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                       "Use !save <tag> to save a tag or that account number doesn't exist,"
                                       " use !accounts to see the accounts you have saved")
            profiledata = await self.clash.get_player(profiletag)
        except clashroyale.RequestError:
            return await self.bot.say("Error: cannot reach Clash Royale Servers. Please try again later.")
    
        #await ctx.send(profiledata.current_deck)
        message = ctx.message
        message.content = ctx.prefix + "deck gl " + await self.constants.decklink_url(profiledata.current_deck)
        message.author = member
    
        await self.bot.process_commands(message)

    @commands.command(aliases=['chests'])
    async def nextchests(self, ctx, member: discord.Member = None, account: int = 1):
        """View yours or other's chest cycle"""
        member = member or ctx.message.author
        await ctx.trigger_typing()
        try:
            profiletag = self.tags.getTag(member.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                       "Use !save <tag> to save a tag or that account number doesn't exist,"
                                       " use !accounts to see the accounts you have saved")
            profiledata = await self.clash.get_player(profiletag)
            chests = await self.clash.get_player_chests(profiletag)


        except clashroyale.RequestError:
            return await self.bot.say("Error: cannot reach Clash Royale Servers. Please try again later.")
    
        chests_msg = ""
        i = 0
        for chest in chests:
            emoji = discord.utils.get(self.bot.emojis, name = str(chest.name.lower().replace(" ", "")))
            chests_msg += f"{emoji}`{chest.index}`"
            #chests_msg += "{}".format(str(chest.name.lower().replace(" ", "")))

            if i == 8:
                chests_msg +="X"
            i+=1
        embed = discord.Embed(color=discord.Color.green(), description="**Chest Cycle :**")
        embed.set_author(name=profiledata.name + " (" + profiledata.tag + ")",
                         icon_url=await self.constants.get_clan_image(profiledata),
                         url="https://royaleapi.com/player/" + profiledata.tag.strip("#"))
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/827982101507866726/830003361281343528/legend_logo-trans.png?width=473&height=473")
        embed.add_field(name="\u200B", value="\u200B", inline=False)

        embed.add_field(name="Upcoming Chests", value="{}".format(chests_msg.split("X")[0]), inline=False)
        embed.add_field(name="Rare Chests", value="{}".format(chests_msg.split("X")[1]), inline=False)
        embed.set_image(url="https://cdn.discordapp.com/emojis/830015568190504960.gif?v=1")
        embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/jZqqzbGd-oAdn-t2JmmD0XlFJJjUs7e1Hd3phypFhMY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_b5bce61cbada3a988140b5b93c6b7966.gif?width=473&height=473")
        await ctx.send(embed=embed)


    @commands.command()
    async def ncchest(self, ctx, member: discord.Member = None, account: int = 1):
        """View yours or other's chest cycle"""
        member = member or ctx.message.author
        await ctx.trigger_typing()
        try:
            profiletag = self.tags.getTag(member.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                       "Use !save <tag> to save a tag or that account number doesn't exist,"
                                       " use !accounts to see the accounts you have saved")
            profiledata = await self.clash.get_player(profiletag)
            await ctx.send(f"```{await self.clash.get_player_chests(profiletag)}```")
        except Exeption as e:
            await ctx.send(e)        


    #@checks.is_owner()           
    @commands.command()
    async def badges(self, ctx: commands.Context, member: discord.Member = None, account: int = 1):
        """Know badges in Clash Royale"""
        if member is None:
          member = ctx.author
        else:
            member = member
        
        await ctx.trigger_typing()
        try:
            profiletag = self.tags.getTag(member.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                       "Use !save <tag> to save a tag or that account number doesn't exist,"
                                       " use !accounts to see the accounts you have saved")
            player = await self.clash.get_player(profiletag)

        except clashroyale.RequestError:
            return await self.bot.say("Error: cannot reach Clash Royale Servers. Please try again later.")    

 

        #initialise all path vars as None / 0
        bi = None
        gi = None 
        yb1, yb2, yb3, yb4, yb5 = None, None, None, None, None
        k_wins = None
        TopLadder = None
        gt, ladder = None, None
        gt_length = 0
        ladder_length = 0
        cww, crl18, crl19 = None, None, None
        progress_18, progress_19 = 0, 0
        numberofbadges = 0
        
        #checking badges
        for badge in player.badges:
            if badge.name == 'Classic12Wins': 


                if badge.progress < 10:
                    bi = str(bundled_data_path(self) / "badge assets" / "ach-cc-x1-fs8.png")

                elif badge.progress >= 10 and badge.progress <100:
                    bi = str(bundled_data_path(self) / "badge assets" / "ach-cc-x10-fs8.png")
                else:
                    bi = str(bundled_data_path(self) / "badge assets" / "ach-cc-x100-fs8.png") 
                numberofbadges += 1
            
            elif badge.name == 'Grand12Wins':
                 if badge.progress < 10:
                    gi = str(bundled_data_path(self) / "badge assets" / "ach-gc-x1-fs8.png")
                 elif badge.progress >= 10 and badge.progress <100:
                    gi = str(bundled_data_path(self) / "badge assets" / "ach-gc-x10-fs8.png")
                 else:
                    gi = str(bundled_data_path(self) / "badge assets" / "ach-gc-x100-fs8.png")  
                 numberofbadges += 1 
            
            elif badge.name == 'Played1Year':
                yb1 = str(bundled_data_path(self) / "badge assets" / "ach-year-1-fs8.png")
                numberofbadges += 1

            elif badge.name == 'Played2Years':
                yb2 = str(bundled_data_path(self) / "badge assets" / "ach-year-2-fs8.png")
                numberofbadges += 1

            elif badge.name == 'Played3Years':
                yb3 = str(bundled_data_path(self) / "badge assets" / "ach-year-3-fs8.png")
                numberofbadges += 1

            elif badge.name == 'Played4Years':
                yb4 = str(bundled_data_path(self) / "badge assets" / "ach-year-4-fs8.png")     
                numberofbadges += 1   

            elif badge.name == 'Played5Years':
                yb5 = str(bundled_data_path(self) / "badge assets" / "ach-year-5-fs8.png")
                numberofbadges += 1

            elif badge.name == '1000Wins':
                k_wins = str(bundled_data_path(self) / "badge assets" / "ach-wins-fs8.png")
                numberofbadges += 1

            elif badge.name == 'TopLeague':
                if badge.progress >= 5000 and badge.progress < 5300:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-1-fs8.png")   
                elif badge.progress >= 5300 and badge.progress < 5600:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-2-fs8.png")  
                elif badge.progress >= 5600 and badge.progress < 6000:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-3-fs8.png") 
                elif badge.progress >= 6000 and badge.progress < 6300:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-4-fs8.png")   
                elif badge.progress >= 6300 and badge.progress < 6600:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-5-fs8.png")  
                elif badge.progress >= 6600 and badge.progress < 7000:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-6-fs8.png")  
                elif badge.progress >= 7000 and badge.progress < 7300:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-7-fs8.png")  
                elif badge.progress >= 7300 and badge.progress < 7600:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-8-fs8.png")  
                elif badge.progress >= 7600 and badge.progress < 8000:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-9-fs8.png")  
                else:
                    TopLadder = str(bundled_data_path(self) / "badge assets" / "ach-league-10-fs8.png") 
                numberofbadges += 1

            elif badge.name.startswith('LadderTournamentTop1000'):
                 gt = str(bundled_data_path(self) / "badge assets" / "ach-tournament-fs8.png") 
                 gt_length = gt_length + 1

            elif badge.name.startswith('LadderTop1000'):
                ladder = str(bundled_data_path(self) / "badge assets" / "ach-rank-fs8.png") 
                ladder_length = ladder_length + 1

            elif badge.name == 'ClanWarWins':
                if badge.progress >= 1 and badge.progress <10:
                    cww = str(bundled_data_path(self) / "badge assets" / "cw 1x.png")
                elif badge.progress >=10 and badge.progress <100:
                    cww = str(bundled_data_path(self) / "badge assets" / "cw 10x.png")
                else:
                    cww = str(bundled_data_path(self) / "badge assets" / "cw 100x.png")
                numberofbadges += 1


            elif badge.name == 'Crl20Wins':
                crl18 = str(bundled_data_path(self) / "badge assets" / "ach-crl-fs8.png")
                progress_18 = badge.progress
                numberofbadges += 1
 
            elif badge.name == 'Crl20Wins2019':
                crl19 = str(bundled_data_path(self) / "badge assets" / "ach-crl-fs8.png")
                progress_19 = badge.progress
                numberofbadges += 1

        #checking number of GT and Ladder badges
        #also creating array with finishes
        gt_countervalue = 1
        ladder_countervalue = 1 
        gt_array = np.empty([5], dtype = "<U10")
        ladder_array = np.empty([5], dtype = "<U10")

        for badge in player.badges:
            if badge.name == 'LadderTournamentTop1000_{}'.format(str(gt_countervalue)):
                numberofbadges += 1     
                #array for GT finishes        
                gt_array[gt_countervalue-1] = badge.progress  
                gt_countervalue += 1            
            elif badge.name == 'LadderTop1000_{}'.format(str(ladder_countervalue)): 
                numberofbadges += 1
                #array for Ladder finishes 
                ladder_array[ladder_countervalue-1] = badge.progress
                ladder_countervalue += 1
            

        size0 = 100, 100
        bg_size = 0, 0
        if numberofbadges == 0:
            await ctx.send("No badges found :(")
            return

        elif numberofbadges <= 5 :
            bg_size = 5*size0[0], size0[1]
        
        elif numberofbadges <= 10 :
            bg_size = 5*size0[0], 2*size0[1]
        
        elif numberofbadges <= 15:
            bg_size = 5*size0[0], 3*size0[0]
        
        elif numberofbadges <=20:
            bg_size = 5*size0[0], 4*size0[0]
        
        else:
            return await ctx.send("You got too many badges to display :joy:")


        nextplacement = 0,0
        bgb = Image.open(str(bundled_data_path(self) / "crbg.png"))
        bgb = bgb.convert('RGBA')
        bgb = bgb.resize((bg_size))
        if bi is not None:
            img1 = Image.open(bi)
            img1 = img1.convert('RGBA')
            img1 = img1.resize((size0))
            bgb.alpha_composite(img1, (nextplacement))
            nextplacement = size0[0], 0

        if gi is not None:
            img2 = Image.open(gi)
            img2 = img2.convert('RGBA')
            img2 = img2.resize((size0))
            bgb.alpha_composite(img2, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
             nextplacement = 2*size0[0], 0

        if yb1 is not None:
            img3 = Image.open(yb1)
            img3 = img3.convert('RGBA')
            img3 = img3.resize((size0))
            bgb.alpha_composite(img3, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0

        if yb2 is not None:
            img4 = Image.open(yb2)
            img4 = img4.convert('RGBA')
            img4 = img4.resize((size0))
            bgb.alpha_composite(img4, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0

        if yb3 is not None:
            img5 = Image.open(yb3)
            img5 = img5.convert('RGBA')
            img5 = img5.resize((size0))
            bgb.alpha_composite(img5, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]


        if yb4 is not None:
            img6 = Image.open(yb4)
            img6 = img6.convert('RGBA')
            img6 = img6.resize((size0))
            bgb.alpha_composite(img6, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]


        if yb5 is not None:
            img7 = Image.open(yb5)
            img7 = img7.convert('RGBA')
            img7 = img7.resize((size0))
            bgb.alpha_composite(img7, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]
            elif nextplacement == (size0[0], size0[1]):
                nextplacement = 2*size0[0], size0[1]

        if k_wins is not None:
            img8 = Image.open(k_wins)
            img8 = img8.convert('RGBA')
            img8 = img8.resize((size0))
            bgb.alpha_composite(img8, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]
            elif nextplacement == (size0[0], size0[1]):
                nextplacement = 2*size0[0], size0[1]
            elif nextplacement == (2*size0[0], size0[1]):
                nextplacement = 3*size0[0], size0[1]

                

        if TopLadder is not None:
            img9 = Image.open(TopLadder)
            img9 = img9.convert('RGBA')
            img9 = img9.resize((size0))
            bgb.alpha_composite(img9, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]
            elif nextplacement == (size0[0], size0[1]):
                nextplacement = 2*size0[0], size0[1]
            elif nextplacement == (2*size0[0], size0[1]):
                nextplacement = 3*size0[0], size0[1]
            elif nextplacement == (3*size0[0], size0[1]):
                nextplacement = 4*size0[0], size0[1]


        if crl19 is not None:
            img13 = Image.open(crl19)
            img13 = img13.convert('RGBA')
            img13 = img13.resize((size0))
            draw = ImageDraw.Draw(img13)
            font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
            text = '{}'.format(progress_19)

            draw.text((40, 64), text, align ="centre", font=font)
            bgb.alpha_composite(img13, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]
            elif nextplacement == (size0[0], size0[1]):
                nextplacement = 2*size0[0], size0[1]
            elif nextplacement == (2*size0[0], size0[1]):
                nextplacement = 3*size0[0], size0[1]
            elif nextplacement == (3*size0[0], size0[1]):
                nextplacement = 4*size0[0], size0[1]
            elif nextplacement == (4*size0[0], size0[1]):
                 nextplacement = 0, 2*size0[1]



        if crl18 is not None:
            img12 = Image.open(crl18)
            img12 = img12.convert('RGBA')
            img12 = img12.resize((size0))

            draw = ImageDraw.Draw(img12)
            font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
            text = '{}'.format(progress_18)

            draw.text((40, 64), text, align ="centre", font=font)
            bgb.alpha_composite(img12, (nextplacement))            
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]
            elif nextplacement == (size0[0], size0[1]):
                nextplacement = 2*size0[0], size0[1]
            elif nextplacement == (2*size0[0], size0[1]):
                nextplacement = 3*size0[0], size0[1]
            elif nextplacement == (3*size0[0], size0[1]):
                nextplacement = 4*size0[0], size0[1]
            elif nextplacement == (4*size0[0], size0[1]):
                 nextplacement = 0, 2*size0[1]
            elif nextplacement == (0, 2*size0[1]):
                 nextplacement = size0[0], 2*size0[1]

        if cww is not None:
            img11 = Image.open(cww)
            img11 = img11.convert('RGBA')
            img11 = img11.resize((size0))
            bgb.alpha_composite(img11, (nextplacement))
            if nextplacement == (0,0):
                nextplacement = size0[0], 0
            elif nextplacement == (size0[0], 0):
                nextplacement = 2*size0[0], 0
            elif nextplacement == (2*size0[0], 0):
                nextplacement = 3*size0[0], 0
            elif nextplacement == (3*size0[0], 0):
                nextplacement = 4*size0[0], 0
            elif nextplacement == (4*size0[0],0):
                nextplacement = 0, size0[1]
            elif nextplacement == (0, size0[1]):
                nextplacement = size0[0], size0[1]
            elif nextplacement == (size0[0], size0[1]):
                nextplacement = 2*size0[0], size0[1]
            elif nextplacement == (2*size0[0], size0[1]):
                nextplacement = 3*size0[0], size0[1]
            elif nextplacement == (3*size0[0], size0[1]):
                nextplacement = 4*size0[0], size0[1]
            elif nextplacement == (4*size0[0], size0[1]):
                 nextplacement = 0, 2*size0[1]
            elif nextplacement == (0, 2*size0[1]):
                 nextplacement = size0[0], 2*size0[1]
            elif nextplacement == (size0[0], 2*size0[1]):
                 nextplacement = 2*size0[0], 2*size0[1]
        

        if gt is not None:
            img10 = Image.open(gt)
            img10 = img10.convert('RGBA')
            img10 = img10.resize((size0))
            if gt_array[0] != '':
                gt_1 = Image.open(gt)
                gt_1 = gt_1.convert('RGBA')
                gt_1 = gt_1.resize((size0))
                text = "#{}".format(gt_array[0])
                draw = ImageDraw.Draw(gt_1)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(gt_1, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
            if gt_array[1] != '':
                gt_2 = Image.open(gt)
                gt_2 = gt_2.convert('RGBA')
                gt_2 = gt_2.resize((size0))
                text = "#{}".format(gt_array[1])
                draw = ImageDraw.Draw(gt_2)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(gt_2, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]

            if gt_array[2] != '':
                gt_3 = Image.open(gt)
                gt_3 = gt_3.convert('RGBA')
                gt_3 = gt_3.resize((size0))
                text = "#{}".format(gt_array[2])
                draw = ImageDraw.Draw(gt_3)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(gt_3, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]

            if gt_array[3] != '':
                gt_4 = Image.open(gt)
                gt_4 = gt_4.convert('RGBA')
                gt_4 = gt_4.resize((size0))
                text = "#{}".format(gt_array[3])
                draw = ImageDraw.Draw(gt_3)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(gt_4, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]
                elif nextplacement == (size0[0], 3*size0[1]):
                                nextplacement = 2*size0[0], 3*size0[1]

            if gt_array[4] != '':
                gt_5 = Image.open(gt)
                gt_5 = gt_5.convert('RGBA')
                gt_5 = gt_5.resize((size0))
                text = "#{}".format(gt_array[4])
                draw = ImageDraw.Draw(gt_5)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(gt_5, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]
                elif nextplacement == (size0[0], 3*size0[1]):
                                nextplacement = 2*size0[0], 3*size0[1]
                elif nextplacement == (2*size0[0], 3*size0[1]):
                                nextplacement = 3*size0[0], 3*size0[1]


        if ladder is not None:
            ladder_image = Image.open(ladder)
            ladder_image = ladder_image.convert('RGBA')
            ladder_image = ladder_image.resize((size0))

            if ladder_array[0] != '':
                lr_1 = Image.open(ladder)
                lr_1 = lr_1.convert('RGBA')
                lr_1 = lr_1.resize((size0))
                text = "#{}".format(ladder_array[0])
                draw = ImageDraw.Draw(lr_1)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(lr_1, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]
                elif nextplacement == (size0[0], 3*size0[1]):
                                nextplacement = 2*size0[0], 3*size0[1]
                elif nextplacement == (2*size0[0], 3*size0[1]):
                                nextplacement = 3*size0[0], 3*size0[1]
                elif nextplacement == (3*size0[0], 3*size0[1]):
                                nextplacement = 4*size0[0], 3*size0[1]
            if ladder_array[1] != '':
                lr_2 = Image.open(ladder)
                lr_2 = lr_2.convert('RGBA')
                lr_2 = lr_2.resize((size0))
                text = "#{}".format(ladder_array[1])
                draw = ImageDraw.Draw(lr_2)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(lr_2, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]
                elif nextplacement == (size0[0], 3*size0[1]):
                                nextplacement = 2*size0[0], 3*size0[1]
                elif nextplacement == (2*size0[0], 3*size0[1]):
                                nextplacement = 3*size0[0], 3*size0[1]
                elif nextplacement == (3*size0[0], 3*size0[1]):
                                nextplacement = 4*size0[0], 3*size0[1]
                elif nextplacement == (4*size0[0], 3*size0[1]):
                                nextplacement = 0, 4*size0[1]
            if ladder_array[2] != '':
                lr_3 = Image.open(ladder)
                lr_3 = lr_3.convert('RGBA')
                lr_3 = lr_3.resize((size0))
                text = "#{}".format(ladder_array[2])
                draw = ImageDraw.Draw(lr_3)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(lr_3, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]
                elif nextplacement == (size0[0], 3*size0[1]):
                                nextplacement = 2*size0[0], 3*size0[1]
                elif nextplacement == (2*size0[0], 3*size0[1]):
                                nextplacement = 3*size0[0], 3*size0[1]
                elif nextplacement == (3*size0[0], 3*size0[1]):
                                nextplacement = 4*size0[0], 3*size0[1]
                elif nextplacement == (4*size0[0], 3*size0[1]):
                                nextplacement = 0, 4*size0[1]                        
                elif nextplacement == (0, 4*size0[1]):
                                nextplacement = size0[0], 4*size0[1]  

            if ladder_array[3] != '':
                lr_4 = Image.open(ladder)
                lr_4 = lr_4.convert('RGBA')
                lr_4 = lr_4.resize((size0))
                text = "#{}".format(ladder_array[3])
                draw = ImageDraw.Draw(lr_4)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(lr_4, (nextplacement))
                if nextplacement == (0,0):
                                nextplacement = size0[0], 0
                elif nextplacement == (size0[0], 0):
                                nextplacement = 2*size0[0], 0
                elif nextplacement == (2*size0[0], 0):
                                nextplacement = 3*size0[0], 0
                elif nextplacement == (3*size0[0], 0):
                                 nextplacement = 4*size0[0], 0
                elif nextplacement == (4*size0[0],0):
                                nextplacement = 0, size0[1]
                elif nextplacement == (0, size0[1]):
                                nextplacement = size0[0], size0[1]
                elif nextplacement == (size0[0], size0[1]):
                                nextplacement = 2*size0[0], size0[1]
                elif nextplacement == (2*size0[0], size0[1]):
                                nextplacement = 3*size0[0], size0[1]
                elif nextplacement == (3*size0[0], size0[1]):
                                nextplacement = 4*size0[0], size0[1]
                elif nextplacement == (4*size0[0], size0[1]):
                                 nextplacement = 0, 2*size0[1]
                elif nextplacement == (0, 2*size0[1]):
                                nextplacement = size0[0], 2*size0[1]
                elif nextplacement == (size0[0], 2*size0[1]):
                             nextplacement = 2*size0[0], 2*size0[1]
                elif nextplacement == (2*size0[0], 2*size0[1]):
                                nextplacement = 3*size0[0], 2*size0[1]
                elif nextplacement == (3*size0[0], 2*size0[1]):
                                nextplacement = 4*size0[0], 2*size0[1]
                elif nextplacement == (4*size0[0], 2*size0[1]):
                                nextplacement = 0, 3*size0[1]
                elif nextplacement == (0, 3*size0[1]):
                                nextplacement = size0[0], 3*size0[1]
                elif nextplacement == (size0[0], 3*size0[1]):
                                nextplacement = 2*size0[0], 3*size0[1]
                elif nextplacement == (2*size0[0], 3*size0[1]):
                                nextplacement = 3*size0[0], 3*size0[1]
                elif nextplacement == (3*size0[0], 3*size0[1]):
                                nextplacement = 4*size0[0], 3*size0[1]
                elif nextplacement == (4*size0[0], 3*size0[1]):
                                nextplacement = 0, 4*size0[1]                        
                elif nextplacement == (0, 4*size0[1]):
                                nextplacement = size0[0], 4*size0[1]  
                elif nextplacement == (size0[0], 4*size0[1]):
                                nextplacement = 2*size0[0], 4*size0[1]

            if ladder_array[4] != '':
                lr_5 = Image.open(ladder)
                lr_5 = lr_5.convert('RGBA')
                lr_5 = lr_5.resize((size0))
                text = "#{}".format(ladder_array[4])
                draw = ImageDraw.Draw(lr_5)
                font = ImageFont.truetype(font = str(bundled_data_path(self) / "OpenSans-ExtraBold.ttf"), size=18)
                draw.text((35, 64), text, align ="centre", font=font)
                bgb.alpha_composite(lr_5, (nextplacement))


            
            


        #bgb.alpha_composite(img1)
        #bgb.alpha_composite(img2, (size0[0],0))

        with io.BytesIO() as f:
            bgb.save(f, "PNG")
            filename = "bgb.png"
            f.seek(0)
            embed = discord.Embed(color=discord.Colour.green(), description="**{}'s Clash Royale badges{}**".format(player.name,self.emoji("wfame")))
            embed.set_author(name = "\u200B", url="https://discord.gg/VWBjECATcF", icon_url=ctx.guild.icon_url)
            embed.set_image(url="attachment://{}".format(filename))
            embed.set_footer(text="Bot by Gladiator#6969", icon_url = "https://images-ext-1.discordapp.net/external/jZqqzbGd-oAdn-t2JmmD0XlFJJjUs7e1Hd3phypFhMY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_b5bce61cbada3a988140b5b93c6b7966.gif?width=473&height=473")
            await ctx.send(file=discord.File(f, filename=filename), embed=embed)
 
        #await ctx.send("GT BADGES :- {} \n LADDER BADGES :- {}".format(gt_array, ladder_array))       



