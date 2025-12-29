import sys

if (sys.version_info[0] < 3) and (sys.version_info[1] < 11):
    raise Exception("Python 3.11 or a more recent version is required.")

import os
from dotenv import load_dotenv
import logging
import asyncio
import asqlite

from ControlBot import ControlBot

import twitchio

LOGGER: logging.Logger = logging.getLogger("Bot")


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def env_exists():
    if (
        os.environ["OWNER_NAME"] != ""
        and os.environ["OWNER_ID"] != ""
        and os.environ["BOT_NAME"] != ""
        and os.environ["BOT_ID"] != ""
        and os.environ["TARGET_ID"] != ""
        and os.environ["TARGET_NAME"] != ""
        and os.environ["CLIENT_ID"] != ""
        and os.environ["CLIENT_SECRET"] != ""
    ):
        return True
    else:
        return False


def run_bots(auth_mode: bool = False) -> None:
    clear_console()
    load_dotenv()
    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        async with (
            asqlite.create_pool("tokens.db") as tdb,
            ControlBot(auth_mode=auth_mode, token_database=tdb) as cbot,
        ):
            await cbot.setup_database()
            await cbot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")
    except Exception:
        LOGGER.warning("shutting down due to Panic Button...")


if __name__ == "__main__":
    run_bots()
