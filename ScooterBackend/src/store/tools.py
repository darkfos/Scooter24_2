from redis import Redis
from typing import Any, Final, Dict, Callable
import json
import logging

# Settings
from src.settings.engine_settings import Settings


class RedisTools:

    __REDIS_CONNECTION: Final[Redis] = Redis(
        host=Settings.redis_settings.REDIS_HOST,
        port=Settings.redis_settings.REDIS_PORT,
        db=0
    )

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
                logging.info(
                    msg="Redis получение данных по ключу {}".format(
                        kwargs["redis_search_data"]
                    )
                )  # Logging
                return json.loads(redis_data)

            result_func = await func(*args, **kwargs)

            # Set data in redis DB
            await self.set_key_and_value(
                key=kwargs["redis_search_data"],
                value=result_func.model_dump_json()
            )

            # Logging
            logging.info(msg="Redis данные были сохранены в хранилище")
            return result_func

        return wrapper_service
