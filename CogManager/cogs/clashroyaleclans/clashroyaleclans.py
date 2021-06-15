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
credits_icon = 'https://images-ext-1.discordapp.net/external/jZqqzbGd-oAdn-t2JmmD0XlFJJjUs7e1Hd3phypFhMY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/698376874186768384/a_b5bce61cbada3a988140b5b93c6b7966.gif?width=473&height=473'



class InvalidRole(Exception):
    pass


class NoToken(Exception):
    pass


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


class ClashRoyaleClans(commands.Cog):
    """Commands for Clash Royale Family Management"""

    def __init__(self, bot):
        self.bot = bot

        crtools_cog = self.bot.get_cog("ClashRoyaleTools")
        self.tags = getattr(crtools_cog, "tags", None)
        self.constants = getattr(crtools_cog, "constants", "None")

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

        self.esports_path = str(bundled_data_path(self) / "esports.txt")
        with open(self.esports_path) as file:
            self.esports_text = file.read()

        self.claninfo_lock = asyncio.Lock()

        self.token_task = self.bot.loop.create_task(self.crtoken())
        self.refresh_task = self.refresh_data.start()
        self.last_updated = None

    async def crtoken(self):
        # Initialize clashroyale API
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token.get("token") is None:
            log.error(
                "CR Token is not SET. "
                "Use [p]set api clashroyale token,YOUR_TOKEN to set it"
            )
            raise NoToken
        self.clash = clashroyale.official_api.Client(
            token=token["token"], is_async=True, url="https://proxy.royaleapi.dev/v1"
        )

    def cog_unload(self):
        if self.refresh_task:
            self.refresh_task.cancel()
        if self.token_task:
            self.token_task.cancel()
        if self.clash:
            self.bot.loop.create_task(self.clash.close())

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

    @commands.command(name="refresh")
    @checks.mod_or_permissions()
    async def command_refresh(self, ctx: commands.Context):
        async with self.claninfo_lock:
            with open(self.claninfo_path) as file:
                self.family_clans = dict(json.load(file))
        clan_data = list()
        for k, v in self.family_clans.items():
            try:
                clan_tag = v["tag"]
                clan = await self.clash.get_clan(clan_tag)
                clan_data.append(dict(clan))
            # REMINDER: Order is important. RequestError is base exception class.
            except clashroyale.NotFoundError:
                log.critical("Invalid clan tag.")
                return await ctx.send(
                    "Invalid Clan Tag. Please inform a dev about this."
                )
            except clashroyale.RequestError:
                log.error("Error: Cannot reach ClashRoyale Server.")
                return await ctx.send(
                    "Error: cannot reach Clash Royale Servers. Please try again later."
                )
            else:
                logging.info("Updated data for clan {}.".format(k))
        clan_data = sorted(
            clan_data,
            key=lambda x: (
                x["clan_war_trophies"],
                x["required_trophies"],
                x["clan_score"],
            ),
            reverse=True,
        )
        await self.config.clans.set(clan_data)
        logging.info(
            "Updated data for all clans at {}.".format(
                datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            )
        )
        await simple_embed(
            ctx,
            "Use this command only when automated refresh is not working. Inform devs if that happens.",
        )
        self.last_updated = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        await ctx.tick()

    @commands.command(name="approve")
    @checks.mod_or_permissions()
    async def command_approve(
        self,
        ctx: commands.Context,
        member: discord.Member,
        clankey: str,
        account: int = 1,
    ):
        guild = ctx.guild
        valid_keys = [k["nickname"].lower() for k in self.family_clans.values()]
        if clankey.lower() not in valid_keys:
            return await simple_embed(
                ctx,
                "Please use a valid clanname:\n{}".format(
                    humanize_list(list(valid_keys))
                ),
                False,
            )
        clan_info = {}
        # Get requirements for clan to approve
        for name, data in self.family_clans.items():
            if data.get("nickname").lower() == clankey.lower():
                clan_info = data
        clan_name: str = clan_info.get("name")
        clan_tag = clan_info.get("tag")
        clan_role = clan_info.get("clanrole")
        clan_pb = clan_info["requirements"].get("personalbest")
        clan_cwr = clan_info["requirements"].get("cwr")
        clan_private = clan_info["requirements"].get("private")
        clan_waiting = clan_info["waiting"]
        clan_wd_wins = clan_info["requirements"].get("wdwins")

        is_in_clan = True
        try:
            player_tag = self.tags.getTag(member.id, account)
            if player_tag is None:
                return await simple_embed(
                    ctx,
                    "You must associate a tag with this member first using ``{}save #tag @member``".format(
                        ctx.prefix
                    ),
                    False,
                )
            player_data = await self.clash.get_player(player_tag)
            # Clan data for clan to approve
            app_clan_data = await self.clash.get_clan(clan_tag)

            ign = player_data.name
            if player_data.clan is None:
                is_in_clan = False
                player_clantag = ""
            else:
                player_clantag = player_data.clan.tag.strip("#")
        # REMINDER: Order is important. RequestError is base exception class.
        except AttributeError:
            return await ctx.send("Cannot connect to database. Please notify the devs.")
        except clashroyale.NotFoundError:
            return await ctx.send("Player tag is invalid.")
        except clashroyale.RequestError:
            return await simple_embed(
                ctx, "Error: cannot reach Clash Royale Servers. Please try again later."
            )

        # Check if member is already in a clan of family
        membership = False
        for name, data in self.family_clans.items():
            if data["tag"] == player_clantag:
                membership = True

        if not membership:
            player_trophies = player_data.trophies
            player_cards = player_data.cards
            player_pb = player_data.best_trophies
            player_wd_wins = player_data.warDayWins
            player_cwr = await self.discord_helper.clanwar_readiness(player_cards)

            if app_clan_data.get("members") == 50:
                return await simple_embed(
                    ctx, "Approval failed, the clan is Full.", False
                )

            if (player_trophies < app_clan_data.required_trophies) or (
                player_pb < clan_pb
            ):
                return await simple_embed(
                    ctx,
                    "Approval failed, you don't meet the trophy requirements.",
                    False,
                )

            cwr_met = True
            for league in clan_cwr:
                if clan_cwr[league] > 0:
                    if player_cwr[league]["percent"] < clan_cwr[league]:
                        cwr_met = False
            if not cwr_met:
                return await simple_embed(
                    ctx,
                    "Approval failed, you don't meet the CW Readiness requirements.",
                    False,
                )

            if player_wd_wins < clan_wd_wins:
                return await simple_embed(
                    ctx,
                    "Approval failed, you don't meet requirements for war day wins.",
                    False,
                )

            if app_clan_data.type == "closed":
                return await simple_embed(
                    ctx, "Approval failed, the clan is currently closed.", False
                )

            if clan_private:
                if clan_role not in [y.name for y in ctx.author.roles]:
                    return await simple_embed(
                        ctx,
                        "Approval failed, only {} staff can approve new recruits for this clan.".format(
                            clan_name
                        ),
                        False,
                    )

            if is_in_clan:
                warning = (
                    "\n\n:warning: **YOU WILL BE REJECTED "
                    "IF YOU JOIN ANY CLAN WITHOUT "
                    "APPROVAL**"
                )
                await ctx.send(
                    (
                        "{} Please leave your current clan now. "
                        "Your recruit code will arrive in 3 minutes.{}".format(
                            member.mention, warning
                        )
                    ),
                    allowed_mentions=discord.AllowedMentions(users=True),
                )
                await asyncio.sleep(180)

            try:
                recruit_code = "".join(
                    random.choice(string.ascii_uppercase + string.digits)
                    for _ in range(6)
                )

                embed = discord.Embed(color=discord.Colour.blue(), description=f"Congratulations, You have been approved to join [{clan_name} (#{clan_tag})](https://link.clashroyale.com/?clanInfo?id={clan_tag}). Your **RECRUIT CODE** is: ``{recruit_code}`` \n\n Click [here](https://link.clashroyale.com/?clanInfo?id={clan_tag}) or search for #{clan_tag} in-game.\n Send a request **using recruit code** above and wait for your clan leadership to accept you. It usually takes a few minutes to get accepted, but it may take up to a few hours. \n\n **IMPORTANT**: Once your clan leadership has accepted your request, let a staff member in discord know that you have been accepted. They will then unlock all the member channels for you.")
                embed.set_author(name="Chiefs United!", icon_url="https://media.discordapp.net/attachments/754780357349605467/760477780978434058/image0.gif?width=473&height=473")
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/598503254351020032.png?v=1")
                embed.set_image(url="https://images-ext-1.discordapp.net/external/wtqLXQjEmYQLdwmAUUo0gMMutN6MApAxnfHSqsMds7c/%3Fwidth%3D473%26height%3D473/https/media.discordapp.net/attachments/827982101507866726/829589928807497768/legend_logo-trans.png")
                embed.set_footer(text="Bot by Gladiator#6969", icon_url=ctx.guild.get_member(698376874186768384).avatar_url)
                await member.send(embed=embed, allowed_mentions=discord.AllowedMentions(roles=True, users=True))
                    
                await ctx.send((
                        member.mention
                        + " has been approved for **"
                        + clan_name
                        + "**. Please check your DM for instructions on how to join."
                    ),
                    allowed_mentions=discord.AllowedMentions(users=True),
                )

                try:
                    new_name = ign + " (Approved)"
                    await member.edit(nick=new_name)
                except discord.Forbidden:
                    await simple_embed(
                        ctx,
                        "I don't have permission to change nick for this user.",
                        False,
                    )

                role_to_ping = discord.utils.get(guild.roles, name=clan_role)

                embed = discord.Embed(color=0x0080FF)
                embed.set_author(
                    name="New Recruit", icon_url="https://images-ext-2.discordapp.net/external/NlEeweaq5B3VEQAX1J5SSRkBFYkkTewfeHOCxvm-KYM/%3Fsize%3D1024/https/cdn.discordapp.com/icons/760377603982360597/a_00830f54a39736534fa7a1d0b71f6057.gif?width=473&height=473"
                )
                embed.add_field(name="Name", value=ign, inline=True)
                embed.add_field(name="Recruit Code", value=recruit_code, inline=True)
                embed.add_field(name="Clan", value=clan_name, inline=True)
                embed.set_footer(text=credits, icon_url=ctx.guild.get_member(698376874186768384).avatar_url)

                channel = self.bot.get_channel(
                    await self.config.guild(ctx.guild).new_recruits_channel_id()
                )
                if channel and role_to_ping:
                    await channel.send(
                        role_to_ping.mention,
                        embed=embed,
                        allowed_mentions=discord.AllowedMentions(
                            roles=(await self.config.guild(ctx.guild).mentions())[
                                "on_newrecruit"
                            ]
                        ),
                    )
                elif not channel:
                    await ctx.send(
                        "Cannot find channel. Please contact a admin or a dev."
                    )
                elif not role_to_ping:
                    await ctx.send(f"Connot find role {clan_role}.")
            except discord.errors.Forbidden:
                return await ctx.send(
                    "Approval failed, {} please fix your privacy settings, "
                    "we are unable to send you Direct Messages.".format(member.mention),
                    allowed_mentions=discord.AllowedMentions(users=True),
                )
        else:
            await simple_embed(
                ctx,
                f"<:lvl:827893695047139348> Approval failed, {member.display_name} is already a part of {player_data.clan.name}! "
                f" \n ",
                False,
            )

    @commands.command(name="clanaudit")
    async def clanaudit(self, ctx, nickname: str):
        async with ctx.channel.typing():
            clan_info = self.get_clan_by_nickname(nickname)
            if clan_info is None:
                embed=discord.Embed(title="Unknown nickname", description="You entered a nickname not found found in clans.json", color=0xff0000)
                await ctx.channel.send(embed=embed)
                return

            clan_role = clan_info["clanrole"]
            clan_tag = clan_info["tag"]

            # List of all clan member tags from ClashRoyalAPI
            clan_member_by_name_by_tags = await self.get_clan_members(clan_tag)

            # Obtain all members with the clanrole
            role = discord.utils.get(ctx.guild.roles, name=clan_role)

            unknown_members = [] # People w/ role and no tags
            orphan_members = [] # People w/ role and have a tag and can't be found in the ClashRoyalAPI
            absent_names = [] # Tags (URLS?) of people who aren't in Discord
            for member in role.members:
                member_tags = self.tags.quickGetAllTags(member.id)
                if len(member_tags) == 0:
                    unknown_members.append(f"{member.mention}({member.name})")

                found = False
                for tag in member_tags:
                    if tag in clan_member_by_name_by_tags:
                        found = True
                        break
                if not found:
                    orphan_members.append(f"{member.mention}({member.name})")

            for tag,name in clan_member_by_name_by_tags.items():
                if len(self.tags.getUser(tag)) == 0:
                    absent_names.append(f"{name}")

            if len(unknown_members) == 0:
                unknown_members_str = 'None'
                unknown_count = 0
            else:
                unknown_members.sort(key=str.lower)
                unknown_members_str = "\n".join(unknown_members)
                unknown_count = len(unknown_members)

            if len(orphan_members) == 0:
                orphan_members_str = 'None'
                orphan_count = 0
            else:
                orphan_members.sort(key=str.lower)
                orphan_members_str = "\n".join(orphan_members)
                orphan_count = len(orphan_members)

            if len(absent_names) == 0:
                absent_names_str = 'None'
                absent_count = 0
            else:
                absent_names.sort(key=str.lower)
                absent_names_str = "\n".join(absent_names)
                absent_names_str = absent_names_str[:1024] # max length allowed for discord
                absent_count = len(absent_names)

            embed=discord.Embed(title=f"Clan Audit: {clan_info['name']}", color=0x00ff00)
            embed.add_field(name=f"({unknown_count}) Players with **{clan_role}** role, but have **NO** tags saved", value=unknown_members_str, inline=False)
            embed.add_field(name=f"({orphan_count}) Players with **{clan_role}** role, but have **NOT** joined the clan", value=orphan_members_str, inline=False)
            embed.add_field(name=f"({absent_count}) Players in **{clan_info['name']}**, but have **NOT** joined discord", value=absent_names_str, inline=False)

            await ctx.channel.send(
                embed=embed,
                allowed_mentions=discord.AllowedMentions(
                    users=True, roles=True
                ))

    def get_clan_by_nickname(self, nickname: str):
        for name, data in self.family_clans.items():
            if data.get("nickname").lower() == nickname:
                return data
        return None

    async def get_clan_members(self, clan_tag: str):
        members_names_by_tag = {}
        clan_members = await self.clash.get_clan_members(clan_tag)
        async for member in clan_members:
            members_names_by_tag[member["tag"].strip('#')] = member["name"]
        return members_names_by_tag

    @commands.command(name="newmember")
    @checks.mod()
    async def command_newmember(self, ctx, member: discord.Member):
        """
            Setup nickname, and roles for a new member
        """
        guild = ctx.guild

        # if not (await self.bot.is_mod(ctx.author)):
        #     return await ctx.send(
        #         "Sorry! You do not have enough permissions to run this command."
        #     )

        # Check if user already has any of member roles:
        # Use `!changeclan` to change already registered member's clan cause it needs role checking to remove existing roles
        # if await self.discord_helper._is_member(member, guild=ctx.guild):
        #     return await ctx.send("Error, " + member.mention + " is not a new member.")

        is_clan_member = False
        try:
            player_tags = self.tags.getAllTags(member.id)
        except AttributeError:
            return await ctx.send("Cannot connect to database. Please notify the devs.")
        clans_joined = []
        clan_roles = []
        discord_invites = []
        clan_nicknames = []
        ign = ""
        if len(player_tags) == 0:
            return await ctx.send(
                "You must associate a tag with this member first using ``{}save #tag @member``".format(
                    ctx.prefix
                )
            )

        # Get a list of all family clans joined.
        try:
            for tag in player_tags:
                player_data = await self.clash.get_player(tag)
                if player_data.clan is None:
                    player_clan_tag = ""
                    player_clan_name = ""
                else:
                    player_clan_tag = player_data.clan.tag.strip("#")
                    player_clan_name = player_data.clan.name
                for name, data in self.family_clans.items():
                    if data["tag"] == player_clan_tag:
                        is_clan_member = True
                        clans_joined.append(name)
                        clan_roles.append(data["clanrole"])
                        clan_nicknames.append(data["nickname"])
                        if data.get("invite"):
                            discord_invites.append(data["invite"])
                # Set ign to first available name
                if not ign and player_data.name:
                    ign = player_data.name
        except clashroyale.RequestError:
            return await simple_embed(
                ctx, "Error: cannot reach Clash Royale Servers. Please try again later."
            )

        if ign:
            newname = ign
        else:
            return await simple_embed(ctx, "Cannot find ign for user.", False)

        output_msg = ""
        if is_clan_member:
            newclanname = " | ".join(clan_nicknames)
            newname = ign + " | " + newclanname
            count = 0
            #for i in range(0, len(newname)):
              #count = count + 1;
            #if count > 32:
              #newname = ign + " | " + newclanname[0:7]

            try:
                await member.edit(nick=newname[:31])
            except discord.HTTPException:
                await simple_embed(ctx, "I don't have permission to change nick for this user.", False)
            else:
                	output_msg += "Nickname changed to **{}**\n".format(newname)

            try:
                await self.discord_helper._add_roles(member, clan_roles, reason = "used newmember")
                await discord.Member.remove_roles(member, discord.utils.get(member.guild.roles, name="unverified"))
                await discord.Member.add_roles(member, discord.utils.get(member.guild.roles, name="Chiefs"))
                output_msg += f"**{humanize_list(clan_roles)}** roles added."
            except discord.Forbidden:
                await ctx.send(
                    "{} does not have permission to edit {}’s roles.".format(
                        ctx.author.display_name, member.display_name
                    )
                )
            except discord.HTTPException:
                await ctx.send(
                    "Failed to add roles {}.".format(humanize_list(clan_roles))
                )
            except InvalidRole:
                await ctx.send(
                    "Server roles are not setup properly. "
                    "Please check if you have {} roles in server.".format(
                        humanize_list(clan_roles)
                    )
                )
            if output_msg:
                await simple_embed(ctx, output_msg, True)

            # TODO: Add welcome message to global chat
            await self.discord_helper._remove_roles(member, ["Guest"], reason="used newmwmber")

            roleName = discord.utils.get(guild.roles, name=clan_roles[0])
            recruitment_channel = self.bot.get_channel(
                await self.config.guild(ctx.guild).new_recruits_channel_id()
            )
            if recruitment_channel:
                await recruitment_channel.send(
                    "**{}** recruited **{} (#{})** to {}".format(
                        ctx.author.display_name, ign, tag, roleName.mention
                    ),
                    allowed_mentions=discord.AllowedMentions(
                        roles=(await self.config.guild(ctx.guild).mentions())["on_nm"]
                    ),
                )

            global_channel = self.bot.get_channel(
                await self.config.guild(ctx.guild).global_channel_id()
            )
            if global_channel:
                greeting_to_send = (random.choice(self.greetings)).format(member)
                await global_channel.send(
                    greeting_to_send,
                    allowed_mentions=discord.AllowedMentions(users=True),
                )

            try:
                await simple_embed(
                    member,
                    "Hi There! Congratulations on getting accepted into our clan. "
                    "We have unlocked all the member channels for you in our Discord Server. "
                    "DM any Admin if you have any problems.\n"
                    "Please do not leave our Discord server while you are in the clan. Thank you.",
                )

                await asyncio.sleep(10)
                for page in pagify(self.rules_text, delims=["\n\n\n"]):
                    await simple_embed(member, page)
                await asyncio.sleep(60)
              #  for page in pagify(self.esports_text, delims=["\n\n\n"]):
              #      await member.send(page)
            except discord.errors.Forbidden:
                await ctx.send(
                    (
                        "{} please fix your privacy settings, "
                        "we are unable to send you Direct Messages.".format(
                            member.mention
                        )
                    ),
                    allowed_mentions=discord.AllowedMentions(users=True),
                )

        else:
            await ctx.send(
                "You must be accepted into a clan before I can give you clan roles. "
                "Would you like me to check again in 2 minutes? (Yes/No)"
            )
            pred = MessagePredicate.yes_or_no(ctx)
            await self.bot.wait_for("message", check=pred)
            if not pred.result:
                return
            await ctx.send("Okay, I will retry this command in 2 minutes.")
            await asyncio.sleep(120)
            message = ctx.message
            message.content = ctx.prefix + "newmember {}".format(member.mention)
            await self.bot.process_commands(message)

    #@commands.command(name="inactive")
   # async def command_inactive(self, ctx, member: discord.Member):
     #   all_clan_roles = [c["clanrole"] for c in self.family_clans.values()]
      #  member_roles = set(member.roles)
      #  all_clan_roles += [
       #     "Member",
       # ]
       # await self.discord_helper._remove_roles(member, all_clan_roles, reason="used inactive")
        # If tag is not saved or connection to CR server is not available use current name to determine ign
       # try:
       #     tag = self.tags.getTag(member.id)
       # except AttributeError:
      #      return await ctx.send("Cannot connect to database. Please notify the devs.")
      #  if tag is None:
         #   new_nickname = (member.display_name.split("|")[0]).strip()
      #  try:
         #   new_nickname = (await self.clash.get_player(tag)).name
      #  except discord.HTTPException:
            #new_nickname = (member.display_name.split("|")[0]).strip()
     #   try:
      #      await member.edit(nick=new_nickname)
      #  except discord.Forbidden:
         #   await simple_embed(
              #  ctx, "I don't have permission to change nick for this user.", False
          #  )
      #  member_newroles = set(member.roles)
      #  removed_roles = [r.mention for r in member_roles.difference(member_newroles)]
       # if len(removed_roles) == 0:
         #   removed_roles = ["None"]
        #await simple_embed(
        #    ctx,
           # f"Removed roles: {humanize_list(removed_roles)}\nReset nickname to {new_nickname}",
       # )



    @commands.group(name="crclansset")
    @commands.guild_only()
    @checks.admin()
    async def crclansset(self, ctx):
        """ Set variables used by ClashRoylaleClans cog """
        pass

    @crclansset.group(name="clanmention")
    async def crclansset_clanmention(self, ctx):
        """ Set whether clan will be mentioned """
        pass

    @crclansset_clanmention.command(name="nm")
    async def crclanset_clanmention_nm(self, ctx, value: bool):
        """ Set whether clan will be mentioned on successful newmember """
        await self.config.guild(ctx.guild).mentions.on_nm.set(value)
        await ctx.tick()

    @crclansset_clanmention.command(name="waiting")
    async def crclanset_clanmention_waiting(self, ctx, value: bool):
        """ Set whether clan will be mentioned on successful addition to waiting list """
        await self.config.guild(ctx.guild).mentions.on_waitlist_add.set(value)
        await ctx.tick()

    @crclansset_clanmention.command(name="newrecruit")
    async def crclanset_clanmention_newrecruit(self, ctx, value: bool):
        """ Set whether clan will be mentioned when recruit is approved """
        await self.config.guild(ctx.guild).mentions.on_newrecruit.set(value)
        await ctx.tick()

    @crclansset.command(name="global")
    async def crclansset_global(self, ctx, channel: discord.TextChannel):
        """ Set channel used to welcome newly recruited members """
        await self.config.guild(ctx.guild).global_channel_id.set(channel.id)
        await ctx.tick()

    @crclansset.command(name="newrecruits")
    async def crclansset_newrecruits(self, ctx, channel: discord.TextChannel):
        """ Set channel used to inform staff about new recruits """
        await self.config.guild(ctx.guild).new_recruits_channel_id.set(channel.id)
        await ctx.tick()

    @crclansset.command(name="playerinfo")
    async def crclansset_playerinfo(self, ctx, value: bool):
        """ Set if player info is shown in output of legend """
        await self.config.guild(ctx.guild).player_info_legend.set(value)
        await ctx.tick()


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

