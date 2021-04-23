from dataclasses import dataclass
from datetime import datetime, timedelta
from logging import Logger, getLogger
from typing import Any, Dict, List, Optional, Union

from discord.ext.commands import Context
from discord.ext.commands.errors import (
    BadArgument,
    BotMissingPermissions,
    CheckFailure,
    CommandNotFound,
    MissingPermissions,
    MissingRequiredArgument,
    NoPrivateMessage,
    TooManyArguments,
)

from commanderbot.core.bot.abc.commander_bot_base import CommanderBotBase

__all__ = (
    "ConfiguredExtension",
    "CommanderBot",
)


@dataclass
class ConfiguredExtension:
    name: str
    disabled: bool = False
    options: Optional[Dict[str, Any]] = None

    @staticmethod
    def deserialize(data: Union[str, Dict[str, Any]]) -> "ConfiguredExtension":
        if isinstance(data, str):
            # Extensions starting with a `!` are disabled.
            disabled = data.startswith("!")
            return ConfiguredExtension(name=data, disabled=disabled)
        try:
            return ConfiguredExtension(**data)
        except Exception as ex:
            raise ValueError(f"Invalid extension configuration: {data}") from ex


class CommanderBot(CommanderBotBase):
    def __init__(self, config: Dict[str, Any]):
        # Remove options that don't belong to the discord.py Bot base.
        extensions_data = config.get("extensions")
        # Initialize discord.py Bot base.
        super().__init__(**config)
        # Grab our own logger instance.
        self.log: Logger = getLogger("CommanderBot")
        # Remember when we started and the last time we connected.
        self._started_at: datetime = datetime.utcnow()
        self._connected_since: Optional[datetime] = None
        # Configure extensions.
        self.configured_extensions: Dict[str, ConfiguredExtension] = {}
        if extensions_data:
            self._configure_extensions(extensions_data)
        else:
            self.log.warning("No extensions configured.")

    def _configure_extensions(self, extensions_data: list):
        if not isinstance(extensions_data, list):
            raise ValueError(f"Invalid extensions: {extensions_data}")

        self.log.info(f"Processing {len(extensions_data)} extensions...")

        all_extensions: List[ConfiguredExtension] = [
            ConfiguredExtension.deserialize(entry) for entry in extensions_data
        ]

        self.configured_extensions = {}
        for ext in all_extensions:
            self.configured_extensions[ext.name] = ext

        enabled_extensions: List[ConfiguredExtension] = [
            ext for ext in all_extensions if not ext.disabled
        ]

        self.log.info(f"Loading {len(enabled_extensions)} enabled extensions...")

        for ext in enabled_extensions:
            self.log.info(f"[->] {ext.name}")
            try:
                self.load_extension(ext.name)
            except:
                self.log.exception(f"Failed to load extension: {ext.name}")

        self.log.info(f"Finished loading extensions.")

    # @implements CommanderBotBase
    @property
    def started_at(self) -> datetime:
        return self._started_at

    # @implements CommanderBotBase
    @property
    def connected_since(self) -> Optional[datetime]:
        return self._connected_since

    # @implements CommanderBotBase
    @property
    def uptime(self) -> Optional[timedelta]:
        if self.connected_since is not None:
            return datetime.utcnow() - self.connected_since

    # @implements CommanderBotBase
    def get_extension_options(self, ext_name: str) -> Optional[Dict[str, Any]]:
        if configured_extension := self.configured_extensions.get(ext_name):
            return configured_extension.options

    # @overrides Bot
    async def on_connect(self):
        self.log.warning("Connected to Discord.")
        self._connected_since = datetime.utcnow()

    # @overrides Bot
    async def on_disconnect(self):
        self.log.warning("Disconnected from Discord.")

    # @overrides Bot
    async def on_command_error(self, ctx: Context, ex: Exception):
        if isinstance(ex, CommandNotFound):
            pass
        elif isinstance(ex, (MissingRequiredArgument, TooManyArguments, BadArgument)):
            await ctx.reply(f"🤢 Bad input: {ex}")
            await ctx.send_help(ctx.command)
        elif isinstance(ex, MissingPermissions):
            await ctx.reply(f"😠 You don't have permission to do that.")
        elif isinstance(ex, BotMissingPermissions):
            await ctx.reply(f"😳 I don't have permission to do that.")
        elif isinstance(ex, NoPrivateMessage):
            await ctx.reply(f"🤐 You can't do that in a private message.")
        elif isinstance(ex, CheckFailure):
            await ctx.reply(f"🤔 You can't do that.")
        else:
            try:
                raise ex
            except:
                self.log.exception(f"Ignoring exception in command: {ctx.command}")
            await ctx.reply(f"🔥 Something went wrong trying to do that.")
