import argparse
import json
import os

from commanderbot_lib.bot.commander_bot import CommanderBot
from commanderbot_lib.logging import get_logger, setup_logging

ARG_PARSER = argparse.ArgumentParser()
ARG_PARSER.add_argument("config", help="Configuration file")
ARG_PARSER.add_argument(
    "--token",
    help="Bot token (prefer using the BOT_TOKEN environment variable)",
)
ARG_PARSER.add_argument("--log", help="Log level", default="WARNING")
ARGS = ARG_PARSER.parse_args()

setup_logging(ARGS.log, detailed=True)

LOG = get_logger(__name__)

LOG.info("Hello!")

LOG.info(f"Log level: {ARGS.log}")
LOG.info(f"Configuration file: {ARGS.config}")

LOG.debug("Parsing configuration file...")

CONFIG = json.load(open(ARGS.config))

LOG.debug("Successfully parsed configuration file!")

LOG.info(f"Number of configuration keys: {len(CONFIG)}")

BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

if not BOT_TOKEN:
    BOT_TOKEN = ARGS.token
    if BOT_TOKEN:
        LOG.warning(
            "Bot token provided via --token argument, instead of the BOT_TOKEN environment "
            "variable.",
        )
    else:
        LOG.warning(
            "No BOT_TOKEN environment variable set, and no --token argument provided.",
        )
        BOT_TOKEN = input("Enter bot token: ")


LOG.info("Bot token: " + BOT_TOKEN[:4] + "*" * (len(BOT_TOKEN) - 4))

LOG.warning("Running bot...")

BOT = CommanderBot(CONFIG)

BOT.run(BOT_TOKEN)

LOG.warning("Bot has shut down.")

LOG.info("Goodbye!")
