from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Config
from app.db.database import PostgresDatabase
from app.cache.redis_client import RedisClient

config = Config().get_config()
db = PostgresDatabase(config["database"])
redis_client = RedisClient(config["redis"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.initialize()
    print("STARTUP:")
    app.state.db = db
    app.state.config = config
    app.state.redis = await redis_client.init()
    if app.state.redis:
        print("""\tRedis initialized""")
    else:
        print("\tRedis NOT initialized")

    yield

    if app.state.db:
        await app.state.db.close()

    if app.state.redis:
        await app.state.redis.close()

    print("SHUTDOWN: all was closed")
