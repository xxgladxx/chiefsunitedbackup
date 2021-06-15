"""RemindMe cog for Red-DiscordBot ported and enhanced by PhasecoreX."""
import asyncio
import logging
import time as current_time

import discord
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import humanize_timedelta

from .abc import CompositeMetaClass
from .commands import Commands

__author__ = "PhasecoreX"
log = logging.getLogger("red.pcxcogs.remindme")


class RemindMe(Commands, commands.Cog, metaclass=CompositeMetaClass):
    """Never forget anything anymore."""

    default_global_settings = {
        "schema_version": 0,
        "total_sent": 0,
        "max_user_reminders": 20,
        "reminders": [],
    }
    default_guild_settings = {
        "me_too": False,
    }
    SEND_DELAY_SECONDS = 30

    def __init__(self, bot):
        """Set up the cog."""
        super().__init__()
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=1224364860, force_registration=True
        )
        self.config.register_global(**self.default_global_settings)
        self.config.register_guild(**self.default_guild_settings)
        self.bg_loop_task = None
        self.me_too_reminders = {}
        self.reminder_emoji = "\N{BELL}"

    async def initialize(self):
        """Perform setup actions before loading cog."""
        await self._migrate_config()
        self._enable_bg_loop()

    async def _migrate_config(self):
        """Perform some configuration migrations."""
        if not await self.config.schema_version():
            # Add/generate USER_REMINDER_ID, rename some fields
            current_reminders = await self.config.reminders()
            new_reminders = []
            user_reminder_ids = {}
            for reminder in current_reminders:
                user_reminder_id = user_reminder_ids.get(reminder["ID"], 1)
                new_reminder = {
                    "USER_REMINDER_ID": user_reminder_id,
                    "USER_ID": reminder["ID"],
                    "REMINDER": reminder["TEXT"],
                    "FUTURE": reminder["FUTURE"],
                    "FUTURE_TEXT": reminder["FUTURE_TEXT"],
                    "JUMP_LINK": None,
                }
                user_reminder_ids[reminder["ID"]] = user_reminder_id + 1
                new_reminders.append(new_reminder)
            await self.config.reminders.set(new_reminders)
            await self.config.schema_version.set(1)

    def _enable_bg_loop(self):
        """Set up the background loop task."""
        self.bg_loop_task = self.bot.loop.create_task(self.bg_loop())

        def error_handler(fut: asyncio.Future):
            try:
                fut.result()
            except asyncio.CancelledError:
                pass
            except Exception as exc:
                log.exception(
                    "Unexpected exception occurred in background loop of RemindMe: ",
                    exc_info=exc,
                )
                asyncio.create_task(
                    self.bot.send_to_owners(
                        "An unexpected exception occurred in the background loop of RemindMe.\n"
                        "Reminders will not be sent out until the cog is reloaded.\n"
                        "Check your console or logs for details, and consider opening a bug report for this."
                    )
                )

        self.bg_loop_task.add_done_callback(error_handler)

    def cog_unload(self):
        """Clean up when cog shuts down."""
        if self.bg_loop_task:
            self.bg_loop_task.cancel()

    async def red_delete_data_for_user(self, *, requester, user_id: int):
        """There's already a [p]forgetme command, so..."""
        users_reminders = await self.get_user_reminders(user_id)
        await self._do_reminder_delete(users_reminders)

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self, payload: discord.raw_models.RawReactionActionEvent
    ):
        """Watches for bell reactions on reminder messages.

        Thank you SinbadCogs!
        https://github.com/mikeshardmind/SinbadCogs/blob/v3/rolemanagement/events.py
        """
        if not payload.guild_id or await self.bot.cog_disabled_in_guild_raw(
            self.qualified_name, payload.guild_id
        ):
            return
        if str(payload.emoji) != self.reminder_emoji:
            return
        guild = self.bot.get_guild(payload.guild_id)
        if not guild:
            return
        member = guild.get_member(payload.user_id)
        if member.bot:
            return

        try:
            reminder = self.me_too_reminders[payload.message_id]
            users_reminders = await self.get_user_reminders(member.id)
            reminder["USER_ID"] = member.id
            if self._reminder_exists(users_reminders, reminder):
                return
            reminder["USER_REMINDER_ID"] = self.get_next_user_reminder_id(
                users_reminders
            )
            async with self.config.reminders() as current_reminders:
                current_reminders.append(reminder)
            message = "Hello! I will also send you "
            if reminder["REPEAT"]:
                human_repeat = humanize_timedelta(seconds=reminder["REPEAT"])
                message += f"those reminders every {human_repeat}"
                if human_repeat != reminder["FUTURE_TEXT"]:
                    message += (
                        f", with the first reminder in {reminder['FUTURE_TEXT']}."
                    )
                else:
                    message += "."
            else:
                message += f"that reminder in {reminder['FUTURE_TEXT']}."

            await member.send(message)
        except KeyError:
            return

    async def get_user_reminders(self, user_id: int):
        """Return all of a users reminders."""
        result = []
        async with self.config.reminders() as current_reminders:
            for reminder in current_reminders:
                if reminder["USER_ID"] == user_id:
                    result.append(reminder)
        return result

    @staticmethod
    def get_next_user_reminder_id(reminder_list):
        """Get the next reminder ID for a user."""
        next_reminder_id = 1
        used_reminder_ids = set()
        for reminder in reminder_list:
            used_reminder_ids.add(reminder["USER_REMINDER_ID"])
        while next_reminder_id in used_reminder_ids:
            next_reminder_id += 1
        return next_reminder_id

    @staticmethod
    def _reminder_exists(reminder_list, reminder):
        """Check if a reminder is already in this reminder list (ignores user reminder ID)."""
        for existing_reminder in reminder_list:
            if (
                existing_reminder["USER_ID"] == reminder["USER_ID"]
                and existing_reminder["REMINDER"] == reminder["REMINDER"]
                and existing_reminder["FUTURE"] == reminder["FUTURE"]
                and existing_reminder["FUTURE_TEXT"] == reminder["FUTURE_TEXT"]
            ):
                return True
        return False

    async def bg_loop(self):
        """Background loop."""
        await self.bot.wait_until_ready()
        while True:
            await self.check_reminders()
            await asyncio.sleep(5)

    async def check_reminders(self):
        """Send reminders that have expired."""
        to_remove = []
        for reminder in await self.config.reminders():
            current_time_seconds = int(current_time.time())
            if reminder["FUTURE"] <= current_time_seconds:
                user = self.bot.get_user(reminder["USER_ID"])
                if user is None:
                    # Can't see the user (no shared servers): delete reminder
                    to_remove.append(reminder)
                    continue

                delay = current_time_seconds - reminder["FUTURE"]
                embed = discord.Embed(
                    title=f":bell:{' (Delayed)' if delay > self.SEND_DELAY_SECONDS else ''} Reminder! :bell:",
                    color=await self.bot.get_embed_color(user),
                )
                if delay > self.SEND_DELAY_SECONDS:
                    embed.set_footer(
                        text=f"This was supposed to send {humanize_timedelta(seconds=delay)} ago.\n"
                        "I might be having network or server issues, or perhaps I just started up.\n"
                        "Sorry about that!"
                    )
                embed_name = f"From {reminder['FUTURE_TEXT']} ago:"
                if "REPEAT" in reminder and reminder["REPEAT"]:
                    embed_name = f"Repeating reminder every {humanize_timedelta(seconds=max(reminder['REPEAT'], 86400))}:"
                reminder_text = reminder["REMINDER"]
                if len(reminder_text) > 900:
                    reminder_text = reminder_text[:897] + "..."
                if "JUMP_LINK" in reminder:
                    reminder_text += f"\n\n[original message]({reminder['JUMP_LINK']})"
                embed.add_field(
                    name=embed_name,
                    value=reminder_text,
                )

                try:
                    await user.send(embed=embed)
                except (discord.Forbidden, discord.NotFound):
                    # Can't send DM's to user: delete reminder
                    to_remove.append(reminder)
                except discord.HTTPException:
                    # Something weird happened: retry next time
                    pass
                else:
                    total_sent = await self.config.total_sent()
                    await self.config.total_sent.set(total_sent + 1)
                    to_remove.append(reminder)
        if to_remove:
            async with self.config.reminders() as current_reminders:
                for reminder in to_remove:
                    try:
                        new_reminder = None
                        if "REPEAT" in reminder and reminder["REPEAT"]:
                            new_reminder = reminder.copy()
                            if new_reminder["REPEAT"] < 86400:
                                new_reminder["REPEAT"] = 86400
                            while new_reminder["FUTURE"] <= int(current_time.time()):
                                new_reminder["FUTURE"] += new_reminder["REPEAT"]
                            new_reminder["FUTURE_TEXT"] = humanize_timedelta(
                                seconds=new_reminder["REPEAT"]
                            )
                        current_reminders.remove(reminder)
                        if new_reminder:
                            current_reminders.append(new_reminder)
                    except ValueError:
                        pass
