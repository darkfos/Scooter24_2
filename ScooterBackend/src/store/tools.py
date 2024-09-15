from redis import Redis
from typing import Type, Final


class RedisTools:

    __REDIS_CONNECTION: Final[Redis] = Redis(host="redis", port=6379)

    @classmethod
    async def set_pair(cls, pair: str, price: str):
        cls.__REDIS_CONNECTION.set(pair, price)

    @classmethod
    async def get_pair(cls, pair):
        return cls.__REDIS_CONNECTION.get(pair)
    
    @classmethod
    async def get_keys(cls):
        return cls.__REDIS_CONNECTION.keys(pattern="*")
