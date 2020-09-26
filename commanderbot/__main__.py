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
ARG_PARSER.add_argument(
    "--tokenfile",
    help="Bot token file (prefer using the BOT_TOKEN environment variable)",
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
    LOG.warning("Bot token provided in a form other than the BOT_TOKEN environment variable.")

    if ARGS.token:
        LOG.info("Using bot token provided as an argument.")
        BOT_TOKEN = ARGS.token

    elif ARGS.tokenfile:
        LOG.info(f"Reading bot token from file: {ARGS.tokenfile}")
        with open(os.path.abspath(ARGS.tokenfile)) as fp:
            BOT_TOKEN = fp.read()

    else:
        BOT_TOKEN = input("Enter bot token: ")

LOG.warning("Running bot...")

BOT = CommanderBot(CONFIG)

BOT.run(BOT_TOKEN)

LOG.warning("Bot has shut down.")

LOG.info("Goodbye!")
