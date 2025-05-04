from typing import AsyncGenerator, Dict, Optional
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
import os

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker


class Database(ABC):
    REQUIRED_KEYS = {'user', 'password', 'host', 'port', 'database'}

    def __init__(self, config: str):
        self._config = config
        self._engine: Optional[AsyncEngine] = None
        self._async_session: Optional[async_sessionmaker[AsyncSession]] = None

    async def initialize(self) -> None:
        self._engine = create_async_engine(self._create_url(), echo=False)
        self._async_session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    def _validate_config(self) -> None:
        missing_keys = self.REQUIRED_KEYS - set(self._config.keys())
        if missing_keys:
            raise ValueError(f'Missing database config keys: {", ".join(missing_keys)}')

        for key, val in self._config.items():
            if not isinstance(val, str):
                raise ValueError(f'Database config value must be a string: key: {key} value: {val}')

            if val in ("", " "):
                raise ValueError(f'Database config value must not be empty: key: {key}')

    @abstractmethod
    def _create_url(self) -> str:
        pass

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


class PostgresDatabase(Database):
    def __init__(self, config):
        if os.getenv('ENV') == 'test':
            config = config['postgres_test']
        else:
            config = config['postgres']
        super().__init__(config)
        self._validate_config()

    def _create_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self._config['user']}:{self._config['password']}@"
            f"{self._config['host']}:{self._config['port']}/"
            f"{self._config['database']}"
        )

