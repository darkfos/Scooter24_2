from fastapi import APIRouter
from src.store.tools import RedisTools


redis_router: APIRouter = APIRouter(prefix="/redis/test")

@redis_router.get(
    path="/get_pair_data/{pair}"
)
async def get_pair_data(pair: str):
    if pair not in [key.encode("utf-8") for key in await RedisTools.get_keys()]:
        return None
    return {"pair": pair, "price": await RedisTools.get_pair(pair)}
