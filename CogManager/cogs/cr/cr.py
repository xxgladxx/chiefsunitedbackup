import discord
from redbot.core import commands, Config, checks
from redbot.core.utils.embed import randomize_colour
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from random import choice
import clashroyale
from json import load
from redbot.core.data_manager import bundled_data_path
import json
import datetime
import datetime as dt
import io
import json
import logging
import os
import random
import re
import string
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional
import aiohttp
import discord
import yaml
from PIL import Image, ImageDraw, ImageFont
from redbot.core import Config, checks, commands
from redbot.core.data_manager import bundled_data_path, cog_data_path
from redbot.core.utils.chat_formatting import pagify
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from redbot.core.utils.predicates import MessagePredicate
from io import BytesIO
import numpy as np
	
PAGINATION_TIMEOUT = 120
prefix = '!'
class ClashRoyaleCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2512325)
        default_user = {"tag" : None, "nick" : None}
        self.config.register_user(**default_user)
        default_guild = {"clans" : {}}
        self.config.register_guild(**default_guild)
        self.constants = self.bot.get_cog('ClashRoyaleTools').constants
        CARDS_JSON_PATH = str(bundled_data_path(self) / "regions.json")
        with open(CARDS_JSON_PATH) as file:
            self.regions = dict(json.load(file))["region_data"]
        
    async def initialize(self):
        keys = await self.bot.get_shared_api_tokens("crapi")
        apikey = keys.get("api_key")
        if apikey is None:
            raise ValueError("The Clash Royale API key has not been set. Use [p]set api crapi api_key,YOURAPIKEY")
        self.crapi = clashroyale.OfficialAPI(apikey, is_async=True)

    async def decklink_url(self, deck, war=False):
        """Decklink URL."""
        ids = []
        for card in deck:
            ids.append(await self.card_to_key(card["name"]))
        url = 'https://link.clashroyale.com/deck/en?deck=' + ';'.join(ids)
        if war:
            url += '&ID=CRRYRPCC&war=1'
        return url


    def badEmbed(self, text):
        bembed = discord.Embed(color=0xff0000)
        bembed.set_author(name=text, icon_url="https://i.imgur.com/FcFoynt.png")
        return bembed
        
    def goodEmbed(self, text):
        gembed = discord.Embed(color=0x45cafc)
        gembed.set_author(name=text, icon_url="https://i.imgur.com/qYmbGK6.png")
        return gembed        

    @commands.command()
    async def save1111(self, ctx, tag, member: discord.Member = None):
        """Save your Clash Royale player tag"""
        if member == None:
            member = ctx.author        
        
        tag = tag.lower().replace('O', '0')
        if tag.startswith("#"):
            tag = tag.strip('#')

        try:
            player = await self.crapi.get_player("#" + tag)
            await self.config.user(member).tag.set(tag)
            await self.config.user(member).nick.set(player.name)
            await ctx.send(embed = self.goodEmbed("CR account {} was saved to {}".format(player.name, member.name)))
            
        except clashroyale.NotFoundError as e:
            await ctx.send(embed = self.badEmbed("No player with this tag found, try again!"))

        except clashroyale.RequestError as e:
            await ctx.send(embed = self.badEmbed(f"CR API is offline, please try again later! ({str(e)})"))
        
        except Exception as e:
            await ctx.send("**Something went wrong, please send a personal message to LA Modmail bot or try again!**")

    @commands.command(aliases=['rcr1111'])
    async def renamecr1(self, ctx, member:discord.Member=None):
        await ctx.trigger_typing()
        prefix = ctx.prefix
        member = ctx.author if member is None else member
        
        tag = await self.config.user(member).tag()
        if tag is None:
            return await ctx.send(embed = self.badEmbed(f"This user has no tag saved! Use {prefix}save <tag>"))
        
        player = await self.crapi.get_player(tag)
        nick = f"{player.name}" if player.clan is not None else f"{player.name}" 
        try:
            await member.edit(nick=nick[:31])
               
            role = discord.utils.get(member.guild.roles, name="Chiefs") if player.clan.name == 'Chiefs United!' else discord.utils.get(member.guild.roles, name="Guest")
            await discord.Member.add_roles(member, role)
                 
            await discord.Member.remove_roles(member, discord.utils.get(member.guild.roles, name="unverified"))                                
            await ctx.send(f"Done! New nickname: `{nick[:31]}`. Required roles added.")
        except discord.Forbidden:
            await ctx.send(f"I dont have permission to change nickname of this user!")
        except Exception as e:
            await ctx.send(f"Something went wrong: {str(e)}")
            
    @commands.command(aliases=['pr111'])
    async def profile1(self, ctx, member=None):
        
        """Clash Royale profile"""
        await ctx.trigger_typing()
        prefix = "/"
        tag = ""

        member = ctx.author if member is None else member

        if isinstance(member, discord.Member):
            tag = await self.config.user(member).tag()
        if tag is None:
                return await ctx.send(embed = self.badEmbed(f"This user has no tag saved! Use {prefix}save <tag>"))
        elif isinstance(member, str) and member.startswith("<"):
            id = member.replace("<", "").replace(">", "").replace("@", "").replace("!", "")
            try:
                member = discord.utils.get(ctx.guild.members, id=int(id))
                if member is not None:
                    tag = await self.config.user(member).tag()
                    if tag is None:
                        return await ctx.send(embed = self.badEmbed(f"This user has no tag saved! Use {prefix}save <tag>"))
            except ValueError:
                pass
        elif isinstance(member, str) and member.startswith("#"):
            tag = member.upper().replace('O', '0')
        elif isinstance(member, str):
            try:
                member = discord.utils.get(ctx.guild.members, id=int(member))
                if member is not None:
                    tag = await self.config.user(member).tag()
                    if tag is None:
                        return await ctx.send(embed = self.badEmbed(f"This user has no tag saved! Use {prefix}save <tag>"))
            except ValueError:
                member = discord.utils.get(ctx.guild.members, name=member)
                if member is not None:
                    tag = await self.config.user(member).tag()
                    if tag is None:
                        return await ctx.send(embed = self.badEmbed(f"This user has no tag saved! Use {prefix}save <tag>"))

        if tag is None or tag == "":
            desc = "/profile\n/profile @user\n/profile discord_name\n/profile discord_id\n/profile #CRTAG"
            embed = discord.Embed(title="Invalid argument!", colour=discord.Colour.red(), description=desc)
            return await ctx.send(embed=embed)
        try:
            player = await self.crapi.get_player(tag)
            chests = await self.crapi.get_player_chests(tag)
            
        except clashroyale.NotFoundError:
            return await ctx.send(embed = self.badEmbed("No clan with this tag found, try again!"))

        except clashroyale.RequestError as e:
            return await ctx.send(embed = self.badEmbed(f"CR API is offline, please try again later! ({str(e)})"))
        
        except Exception as e:
            return await ctx.send("**Something went wrong, please send a personal message to <@590906101554348053> or try again!**")

        ccwins, gcwins = 0, 0
        badges_str = '**Badges:** 2021 Player'
        
        for badge in player.badges:
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
                
        if player.tag == '#9VUCR20UL':  
                badges_str += ', Bot Developer'
        embed=discord.Embed(description = badges_str)
        embed.set_author(name=f"{player.name} {player.tag}", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/Qs0Ter9.png")
        if getattr(player, 'league_statistics', False):
            if not getattr(player.league_statistics.current_season, 'best_trophies', False):
                season_best = player.league_statistics.current_season.trophies
            else:
                season_best = player.league_statistics.current_season.best_trophies
                
        
        embed.add_field(name="Trophies", value=f"<:trophycr:827893698360377415> {player.trophies}")
        if player.trophies >= 4000:
            embed.add_field(name="Season Best", value=f"<:strophy:828219808138395648> {season_best}")
        embed.add_field(name="Highest Trophies", value=f"<:ltrophy:827893696157843467> {player.bestTrophies}")
        embed.add_field(name="Level", value=f"<:lvl:827893695047139348> {player.expLevel}")
        if player.expLevel == 13:
            embed.add_field(name="Star Points", value=f"<:lvl:827893695047139348> {player.star_points}")
        embed.add_field(name="Playing Since", value=f":alarm_clock: {account_age} days")
        embed.add_field(name="Arena", value=f"<:arena:827893484144820224> {player.arena.name}")
        if player.clan is not None:
            clanbadge = discord.utils.get(self.bot.emojis, name = str(player.clan.badgeId))
            embed.add_field(name="Clan", value=f"<:clan:827899551196512286> {player.clan.name}")
            embed.add_field(name="Position", value=f"<:social:827893695206522881> {player.role.capitalize()}")
        embed.add_field(name="Total Games Played", value=f"<:sword:827893697068662814> {player.battleCount}")
        embed.add_field(name="Wins/Losses", value=f"<:up:827893694706352139><:dw:828180361695199243> {player.wins}/{player.losses}")
        embed.add_field(name="Three Crown Wins", value=f"<:bc:827893695474696223> {player.threeCrownWins}")
        embed.add_field(name="Friendly Wins", value=f"<:fb:828221464384765964>{player.achievements[9].value}")
        embed.add_field(name="War Day Wins", value=f"<:cws:827893695927681034> {player.warDayWins}")
        embed.add_field(name="Clan Cards Collected", value=f"<:cards:827893696011567145> {player.clanCardsCollected}")
        embed.add_field(name="Max Challenge Wins", value=f"<:gt:827893482805919754> {player.challengeMaxWins}")
        embed.add_field(name="Challenge Cards Won", value=f"<:deck:827893484823248896> {player.challengeCardsWon}")
        embed.add_field(name="CC Wins", value=f"<:cc:827893697282048000> {ccwins}")
        embed.add_field(name="GC Wins", value=f"<:gc:829001448481095712> {gcwins}")
        embed.add_field(name="Favourite Card", value=f"<:leggy:827893479064600586> {player.currentFavouriteCard.name}")
        embed.add_field(name="Total Donations", value=f"<:trade:828177387287740426> {player.totalDonations}")      

        chests_msg = ""
        i = 0
        for chest in chests:
            emoji = discord.utils.get(self.bot.emojis, name = str(chest.name.lower().replace(" ", "")))
            chests_msg += f"{emoji}`{chest.index}`"
            chests_msg += "{}".format(str(chest.name.lower().replace(" ", "")))

            if i == 8:
                chests_msg +="X"
            i+=1

        embed.add_field(name="Upcoming Chests", value=chests_msg.split("X")[0], inline=False)
        embed.add_field(name="Rare Chests", value=chests_msg.split("X")[1], inline=False)
        embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
        await ctx.send(embed=randomize_colour(embed))

        
        #message = ctx.message
       # message.content = ctx.prefix + "deck gl " + await self.constants.decklink_url(player.current_deck)
       # message.author = member
    
        #await self.bot.process_commands(message)

        #await ctx.send(self.constants.decklink_url(player.current_deck))

    @commands.command()
    async def topladder(self,ctx,location = None):
     """Check the current top 1k players globally or in a region\nTo see list of available locations: !locations"""
     if location is None:
         loc_id = 'global'
         location = "Global"
     else:
         location = location

         for region in sorted(self.regions, key=lambda x: x["id"]):
             key = region["id"]
             name = region["name"]
             if location.lower() == name.lower():
                 loc_id = key



     ply = await self.crapi.get_top_players(loc_id)# limit = 1)            
     out = []
     async for player in ply:
         
            rank = player.rank
            trophies = player.trophies
            key = player.tag
            names = player.expLevel
            name = player.name
            out.append(
                "**{}. {}**\n**Tag: **{}\n**Trophies: **{}".format(
                    rank, name, key, trophies
                )
            )
     pages = []
     for page in pagify("\n\n".join(out), shorten_by=24):
            embed = discord.Embed(description=page, timestamp=dt.datetime.utcnow(), color=discord.Colour.green())
            embed.set_author(name="Top 1000 Leaderboard {}".format(location), icon_url=ctx.guild.icon_url)
            embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
            pages.append(embed)
     await menu(ctx, pages, DEFAULT_CONTROLS, timeout=PAGINATION_TIMEOUT)


    @commands.command()
    async def locations(self, ctx: commands.Context):
     """Display all available location.\n!topladder <location_name to check top players for a region"""
     out = []

     for region in sorted(self.regions, key=lambda x: x["id"]):
            name = region["name"]
            #names = ["name"]
            #name = region["id"]
            out.append(
                "**{}**".format(
                    name
                )
            )
     pages = []
     for page in pagify("\n".join(out), shorten_by=24):
            embed = discord.Embed(description=page, timestamp=dt.datetime.utcnow(), color = discord.Colour.green())
            embed.set_author(name="Available locations:", icon_url=ctx.guild.icon_url)
            embed.set_footer(text="Bot by Gladiator#6969", icon_url="https://images-ext-1.discordapp.net/external/kYJx8YK6XrdnbhUQEHHbFtsmN4X2ga4LbzgVMFllKi8/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_d545d6bab43dd8e041268f1d51fa4199.gif?width=473&height=473")
            pages.append(embed)
     await menu(ctx, pages, DEFAULT_CONTROLS, timeout=PAGINATION_TIMEOUT)         
        

