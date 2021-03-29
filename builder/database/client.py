import os
import logging
import inspect
import asyncpg
from typing import Optional
from builder.paths import TABLES_PATH

class DBClient:
    """
    The database client to use when executing or fetching records from the database
    Params:
        database (str): The database to connect to 
        password (str): The database password
        user (str): The user to use the database with, defaults to postgres
        host (str): The host to connect to, defaults to local host
    """

    __slots__ = ("_database", "_user", "_password", "_host", "connection", "logger")

    def __init__(self, *, database: str, password: str, user: str="postgres", host: Optional[str]=None):
        self._database = database
        self._password = password
        self._user = user
        self._host = host
        self.connection = None
        """The database connection"""
        self.logger = logging.getLogger("Builder DB")
        """The database logger"""

    async def create_pool(self, _): #as we're gonna use this method as subscription callback, it must take one argument (event)
        """
        Create the database pool
        """
        self.logger.info("Creating database pool.")
        self.connection = await asyncpg.create_pool(
            database=self._database,
            password=self._password,
            user=self._user,
            host=self._host
        )
        self.logger.info("Created database pool.")
        self.logger.info("Now creating tables.")
        await self.create_tables()
        self.logger.info("Created tables.")

    async def execute(self, *args, **kwargs):
        """
        Execute SQL code
        """
        return await self.connection.execute(*args, **kwargs)

    async def executescript(self, script):
        """
        Execute a SQL script
        """
        with open(script) as f:
            data = f.read()

        await self.execute(data)

    async def fetch(self, *args, **kwargs):
        """
        Fetch multiple records
        """
        return await self.connection.fetch(*args, **kwargs)

    async def fetchrow(self, *args, **kwargs):
        """
        Fetch a record
        """
        return await self.connection.fetchrow(*args, **kwargs)

    async def fetchval(self, *args, **kwargs):
        """
        Fetch a record value
        """
        return await self.connection.fetchval(*args, **kwargs)

    async def create_tables(self):
        """
        Create all tables in builder/database/tables
        """
        files = (
            os.path.join(TABLES_PATH, f)
            for f in os.listdir(TABLES_PATH)
        )
        
        for filename in files:
            await self.executescript(filename)
            self.logger.info("Executed SQL from %s and created table %s", filename, filename.split("/")[3][:-4])