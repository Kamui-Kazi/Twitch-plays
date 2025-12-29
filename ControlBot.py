import os
from dotenv import load_dotenv
import logging
import asyncio  # noqa: F401
import asqlite
import typing  # noqa: F401
import sqlite3
from KeyboardBot import KeyboardBot


import twitchio
from twitchio import eventsub
from twitchio.ext import commands

load_dotenv()
LOGGER: logging.Logger = logging.getLogger("ControlBot")


# This is where the Bot, its connections, and oauth are set up
class ControlBot(commands.Bot):
    def __init__(
        self, *, token_database: asqlite.Pool, auth_mode: bool = False
    ) -> None:
        self.token_database = token_database
        self.auth_mode: bool = auth_mode
        self.keyboard_bot = KeyboardBot()

        self.owner_name = os.environ["OWNER_NAME"]
        self.bot_name = os.environ["BOT_NAME"]
        self.target_id = os.environ["TARGET_ID"]
        self.target_name = os.environ["TARGET_NAME"]

        super().__init__(
            client_id=os.environ["CLIENT_ID"],
            client_secret=os.environ["CLIENT_SECRET"],
            bot_id=os.environ["BOT_ID"],
            owner_id=os.environ["OWNER_ID"],
            prefix=".",
        )

    async def event_ready(self):
        # When the bot is ready
        await self.keyboard_bot.start()
        LOGGER.info("Successfully logged in as: %s", self.bot_id)
        LOGGER.info(
            "you will have 5 seconds to click on the game before the bots start."
        )
        LOGGER.info("Twitch chat will have control in 5...")
        sleep(1)
        LOGGER.info("4...")
        sleep(1)
        LOGGER.info("3...")
        sleep(1)
        LOGGER.info("2...")
        sleep(1)
        LOGGER.info("1...")
        sleep(1)
        LOGGER.info("0...")
        LOGGER.info("Twitch chat now has control.")

    async def setup_hook(self) -> None:
        # Add our component which contains our commands...
        await self.add_component(ControlComponent(self))

        if not self.auth_mode:
            # Subscribe to chat messages (EventSub)
            subscription = eventsub.ChatMessageSubscription(
                broadcaster_user_id=self.target_id, user_id=self.bot_id
            )
            await self.subscribe_websocket(payload=subscription)

        else:
            # This is the first run, so skip EventSub subscription and mark it as completed
            LOGGER.info("First run — skipping EventSub subscription")
            async with self.token_database.acquire() as connection:
                await connection.execute(
                    "INSERT OR REPLACE INTO flags (key, value) VALUES ('eventsub_initialized', 'true')"
                )

    async def add_token(
        self, token: str, refresh: str
    ) -> twitchio.authentication.ValidateTokenPayload:
        # Make sure to call super() as it will add the tokens interally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(
            token, refresh
        )

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        # We don't need to call this manually, it is called in .login() from .start() internally...

        async with self.token_database.acquire() as connection:
            rows: list[sqlite3.Row] = await connection.fetchall(
                """SELECT * from tokens"""
            )

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        # Create our token table, if it doesn't exist..
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        query_flags = """CREATE TABLE IF NOT EXISTS flags(key TEXT PRIMARY KEY, value TEXT NOT NULL)"""

        async with self.token_database.acquire() as connection:
            await connection.execute(query)  # tokens table
            await connection.execute(query_flags)  # flags table

    async def event_command_error(self, payload: commands.CommandErrorPayload):
        ctx = payload.context
        LOGGER.warning("%s exeption raised by: %s", payload.exception, ctx.message.text)


class ControlComponent(commands.Component):
    def __init__(self, bot: ControlBot):
        self.bot = bot
        self.keyboard_bot = bot.keyboard_bot

    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        LOGGER.info(payload.text)
        await self.keyboard_bot.submit(payload.text.lower().strip())

    @commands.is_moderator()
    @commands.command(aliases=["quit_bot", "stop_bot", "kill_bot", "abort"])
    async def quitbot(self, ctx: commands.Context) -> None:
        raise Exception("the mods turned off the control bot.")

    # brwalf
