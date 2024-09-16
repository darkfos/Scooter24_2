from redis import Redis
from typing import Any, Type, Final, Dict, Callable
import json

class RedisTools:

    __REDIS_CONNECTION: Final[Redis] = Redis(host="localhost", port=6379, db=0)

    @classmethod
    async def set_key_and_value(cls, key: str, value: Dict):
        cls.__REDIS_CONNECTION.set(key, value, ex=20)

    @classmethod
    async def get_value(cls, key):
        return cls.__REDIS_CONNECTION.get(key)
    
    @classmethod
    async def get_keys(cls):
        return cls.__REDIS_CONNECTION.keys(pattern="*")
    
    def __call__(self, func: Callable) -> Any:
        async def wrapper_service(*args, **kwargs):
            redis_data = await self.get_value(key=kwargs["redis_search_data"])
            if redis_data:
                return json.loads(redis_data)
            result_func = await func(*args, **kwargs)
            print(result_func)
            #Set data in redis DB
            await self.set_key_and_value(key=kwargs["redis_search_data"], value=result_func.model_dump_json())

            return result_func
        return wrapper_service