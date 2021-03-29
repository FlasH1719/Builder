import os
import hikari
import logging
from lightbulb import Bot
from datetime import datetime, timezone
from builder.database.client import DBClient
from builder.paths import PLUGINS_PATH

class BuilderBot(Bot):
    __slots__ = ("db", "_start_uptime", "logger")

    def __init__(self, database: DBClient, *args, **kwargs) -> None:
        self.db = database
        self.logger: logging.Logger = logging.getLogger("Builder Bot")
        self._start_uptime: datetime = datetime.now(tz=timezone.utc)

        super().__init__(*args, **kwargs)

        self.subscribe(hikari.StartingEvent, self.load_plugins)
        self.subscribe(hikari.StartedEvent, self.db.create_pool)

    async def load_plugins(self, _) -> None: #subscription callbacks have to be async and take one argument (event)
        """
        Load all plugins
        """

        plugins = (
            os.path.join(PLUGINS_PATH, f).replace("/", ".")[:-3]
            for f in os.listdir(PLUGINS_PATH)
        )

        for plugin in plugins:
            self.load_extension(plugin)
            self.logger.info("Loaded %s", plugin)