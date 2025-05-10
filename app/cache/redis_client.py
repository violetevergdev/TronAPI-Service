import redis.asyncio as redis


class RedisClient:
    def __init__(self, config):
        self.__config = config
        self.redis = None

    async def init(self):
        tmp_redis = redis.Redis(
            host=self.__config["host"],
            port=self.__config["port"],
            password=self.__config["password"],
            db=self.__config["database"],
            decode_responses=True,
        )
        try:
            if await tmp_redis.ping():
                self.redis = tmp_redis
        finally:
            return self.redis

    async def close(self):
        if self.redis:
            await self.redis.close()
