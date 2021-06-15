import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.embed import randomize_colour
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from random import choice
import clashroyale
import asyncio
import itertools
import json
import logging
import os
import random
import string
from datetime import datetime
from typing import List, Optional

import clashroyale
import discord
from discord.ext import tasks
from redbot.core import Config, checks, commands
from redbot.core.data_manager import bundled_data_path, cog_data_path
from redbot.core.utils.chat_formatting import humanize_list, pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu, start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate

credits = "Bot by Gladiator#6969"
credits_icon = "https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473"
log = logging.getLogger("red.cogs.clashroyaleclans")


async def simple_embed(
    ctx: commands.Context,
    message: str,
    success: Optional[bool] = None,
    mentions: dict = dict({"users": True, "roles": True}),
) -> discord.Message:
    """Helper function for embed"""
    if success is True:
        colour = discord.Colour.dark_green()
    elif success is False:
        colour = discord.Colour.dark_red()
    else:
        colour = discord.Colour.blue()
    embed = discord.Embed(description=message, color=colour)
    embed.set_footer(text=credits, icon_url=credits_icon)
    return await ctx.send(
        embed=embed, allowed_mentions=discord.AllowedMentions(**mentions)
    )


class Guest(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        self.config = Config.get_conf(self, identifier=2286464642345664456)
        default_global = {"clans": list()}
        default_guild = {
            "mentions": {
                "on_show_clan": {"users": True, "roles": True},
                "on_approve": {"users": True, "roles": True},
                "on_nm": True,
                "on_newrecruit": True,
                "on_waitlist_add": True,
            },
            "global_channel_id": 760484092268773376,
            "new_recruits_channel_id": 830126719624151121,
            "player_info_legend": True,
        }

        self.config.register_global(**default_global)
        self.config.register_guild(**default_guild)
        self.discord_helper = Helper(bot)
        self.claninfo_path = str(cog_data_path(self) / "clans.json")
        with open(self.claninfo_path) as file:
            self.family_clans = dict(json.load(file))
        self.greetings_path = str(bundled_data_path(self) / "welcome_messages.json")
        with open(self.greetings_path) as file:
            self.greetings = list((json.load(file)).get("GREETING"))


        self.rules_path = str(bundled_data_path(self) / "rules.txt")
        with open(self.rules_path) as file:
            self.rules_text = file.read()
        self.claninfo_lock = asyncio.Lock()

        self.token_task = self.bot.loop.create_task(self.crtoken())
        self.refresh_task = self.refresh_data.start()
        self.last_updated = None


    @tasks.loop(seconds=30)
    async def refresh_data(self):
        try:
            async with self.claninfo_lock:
                with open(self.claninfo_path) as file:
                    self.family_clans = dict(json.load(file))
            all_clan_data = list()
            for name, data in self.family_clans.items():
                try:
                    clan_tag = data["tag"]
                    clan_data = await self.clash.get_clan(clan_tag)
                    all_clan_data.append(dict(clan_data))
                # REMINDER: Order is important. RequestError is base exception class.
                except clashroyale.NotFoundError:
                    log.critical("Invalid clan tag.")
                except clashroyale.RequestError as err:
                    log.error("Error: Cannot reach ClashRoyale Server. {}".format(err))
            all_clan_data = sorted(
                all_clan_data,
                key=lambda x: (
                    x["clan_war_trophies"],
                    x["required_trophies"],
                    x["clan_score"],
                ),
                reverse=True,
            )
            await self.config.clans.set(all_clan_data)
            # log.info("Updated data for all clans.")
        except Exception as e:
            log.error("Encountered exception {} when refreshing clan data.".format(e))
        self.last_updated = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")


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

    @checks.admin()
    @commands.command()
    async def guest(self, ctx, user: discord.Member = None, account: int = 1):
        if user is None:
            user = ctx.author

        try:
            profiletag = self.tags.getTag(user.id, account)
            if profiletag is None:
                return await ctx.send("You don't have a tag saved. "
                                      "Use !save <tag> to save a tag or that account number doesn't exist,"
                                      " use !accounts to see the accounts you have saved")
            
            profiledata = await self.clash.get_player(profiletag)
        except clashroyale.RequestError:
            return await ctx.send("Error: cannot reach Clash Royale Servers. Please try again later.")
        nick = user.display_name
        global_channel = self.bot.get_channel(await self.config.guild(ctx.guild).global_channel_id())


        
        try:
            
            await user.edit(nick=profiledata.name)
   
            if profiledata.clan is not None and profiledata.clan.name != 'Chiefs United!'or profiledata.clan.name != 'Chiefs Rising!':
             await discord.Member.remove_roles(user, discord.utils.get(user.guild.roles, name="unverified"))

             nick = f"{profiledata.name} | Guest" if profiledata.clan is not None else f"{profiledata.name} | Guest" 
             await discord.Member.add_roles(user, discord.utils.get(user.guild.roles, name="Guest"))            
             await ctx.send(f"Done! New nickname: `{nick[:31]}`. Guest roles added.")
             if global_channel:
                 greeting_to_send = (random.choice(self.greetings)).format(user)
                 await global_channel.send(greeting_to_send,allowed_mentions=discord.AllowedMentions(users=True))
                 embed = discord.Embed(description=f"Congratulations {user.mention}, You have been approved to join our server as a guest! \n\n You have been given the access to channels alloted to guests. \n\n We wish you have a great time here, and soon join the Chiefs Club! \u270C")
                 embed.set_author(name="Chiefs United!", icon_url="https://media.discordapp.net/attachments/754780357349605467/760477780978434058/image0.gif?width=473&height=473")
                 embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/598503254351020032.png?v=1")
                 embed.set_image(url="https://images-ext-1.discordapp.net/external/wtqLXQjEmYQLdwmAUUo0gMMutN6MApAxnfHSqsMds7c/%3Fwidth%3D473%26height%3D473/https/media.discordapp.net/attachments/827982101507866726/829589928807497768/legend_logo-trans.png")
                 embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
                 await user.send(embed=embed)
             try:

                 await asyncio.sleep(60)
                 for page in pagify(self.rules_text, delims=["\n\n\n"]):
                   await simple_embed(user, page)
             except discord.errors.Forbidden:
                 await ctx.send(("{} please fix your privacy settings, we are unable to send you Direct Messages.".format(user.mention)), allowed_mentions=discord.AllowedMentions(users=True), )


             
            else:
             if profiledata.clan is not None:
               await ctx.send(f"Guest roles cannot be added as {user.mention} is already a clan member")
        except discord.Forbidden:
            await ctx.send(f"I dont have permission to change nickname of this user!")
        except Exception as e:
            await ctx.send(f"Something went wrong: {str(e)}")

                                            
class Helper:
    def __init__(self, bot):
        self.bot = bot
        self.constants = self.bot.get_cog("ClashRoyaleTools").constants

    @staticmethod
    async def get_user_count(guild: discord.Guild, name: str):
        """Returns the numbers of people with the member role"""
        role = discord.utils.get(guild.roles, name=name)
        return len(role.members)

    @staticmethod
    async def _add_roles(member: discord.Member, role_names: List[str], reason=""):
        """Add roles"""
        roles = [
            discord.utils.get(member.guild.roles, name=role_name)
            for role_name in role_names
        ]
        if any([x is None for x in roles]):
            raise InvalidRole
        try:
            await member.add_roles(*roles, reason="From clashroyaleclans: " + reason )
        except discord.Forbidden:
            raise
        except discord.HTTPException:
            raise

    @staticmethod
    async def _remove_roles(member: discord.Member, role_names: List[str], reason = ""):
        """Remove roles"""
        roles = [
            discord.utils.get(member.guild.roles, name=role_name)
            for role_name in role_names
        ]
        roles = [r for r in roles if r is not None]
        try:
            await member.remove_roles(*roles, reason="From clashroyaleclans: " + reason)
        except Exception:
            pass

    @staticmethod
    async def _is_member(member: discord.Member, guild: discord.Guild):
        """
            Check if member already has any of roles
        """
        """
            Credits: Gr8
        """
        _membership_roles = [
            discord.utils.get(guild.roles, name=r)
            for r in [
                "Member",
                "Co-Leader",
                "Hub Officer",
                "Hub Supervisor" "Clan Deputy",
                "Clan Manager",
            ]
        ]
        _membership_roles = set(_membership_roles)
        author_roles = set(member.roles)
        return bool(len(author_roles.intersection(_membership_roles)) > 0)

    async def clanwar_readiness(self, cards):
        """Calculate clanwar readiness"""
        readiness = {}
        league_levels = {"legendary": 12, "gold": 11, "silver": 10, "bronze": 9}

        for league in league_levels.keys():
            readiness[league] = {
                "name": league.capitalize(),
                "percent": 0,
                "cards": [],
                "levels": str(league_levels[league]),
            }
            for card in cards:
                if await self.constants.get_new_level(card) >= league_levels[league]:
                    readiness[league]["cards"].append(card.name)

            readiness[league]["percent"] = int(
                (len(readiness[league]["cards"]) / len(cards)) * 100
            )

        readiness["gold"]["cards"] = list(
            set(readiness["gold"]["cards"]) - set(readiness["legendary"]["cards"])
        )
        readiness["silver"]["cards"] = list(
            set(readiness["silver"]["cards"])
            - set(readiness["gold"]["cards"])
            - set(readiness["legendary"]["cards"])
        )
        readiness["bronze"]["cards"] = list(
            set(readiness["bronze"]["cards"])
            - set(readiness["silver"]["cards"])
            - set(readiness["gold"]["cards"])
            - set(readiness["legendary"]["cards"])
        )

        return readiness

    def emoji(self, name: str):
        """Emoji by name."""
        for emoji in self.bot.emojis:
            if emoji.name == name.replace(" ", "").replace("-", "").replace(".", ""):
                return "<:{}:{}>".format(emoji.name, emoji.id)
        return ""

    def getLeagueEmoji(self, trophies: int):
        """Get clan war League Emoji"""
        mapLeagues = {
            "legendleague": [3000, 99999],
            "gold3league": [2500, 2999],
            "gold2league": [2000, 2499],
            "goldleague": [1500, 1999],
            "silver3league": [1200, 1499],
            "silver2league": [900, 1199],
            "silverleague": [600, 899],
            "bronze3league": [400, 599],
            "bronze2league": [200, 399],
            "bronzeleague": [0, 199],
        }
        for league in mapLeagues.keys():
            if mapLeagues[league][0] <= trophies <= mapLeagues[league][1]:
                return self.emoji(league)

    def grouper(self, iterable, n):
        args = [iter(iterable)] * n
        return itertools.zip_longest(*args)

    async def get_best_league(self, cards):
        """Get best leagues using readiness"""
        readiness = await self.clanwar_readiness(cards)

        legend = readiness["legendary"]["percent"]
        gold = readiness["gold"]["percent"] - legend
        silver = readiness["silver"]["percent"] - gold - legend
        bronze = readiness["bronze"]["percent"] - silver - gold - legend

        readiness_count = {
            "legendary": legend,
            "gold": gold,
            "silver": silver,
            "bronze": bronze,
        }
        max_key = max(readiness_count, key=lambda k: readiness_count[k])

        return "{} League ({}%)".format(
            max_key.capitalize(), readiness[max_key]["percent"]
        )

    async def get_card_emoji(self, card_name: str):
        card_key = await self.constants.card_to_key(card_name)
        emoji = ""
        if card_key:
            emoji = self.emoji(card_key)
        if emoji == "":
            emoji = self.emoji(card_name)
        return emoji
           


            

