"""import redis.asyncio as aioredis
from configure import Config

JTI_EXPIRY = 3600

token_blocklist = aioredis.from_url(Config.REDIS_URL)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )

async def token_in_blocklist(jti: str) -> bool:
    await token_blocklist.get(jti)
    
    if jti is not None:
        return True
    else:
        return False
"""