import redis.asyncio as aioredis
from configure import Config

# Token expiration time in seconds (1 hour)
JTI_EXPIRY = 3600

# Initialize Redis connection
redis_client = aioredis.from_url(
    Config.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

async def init_redis():
    """Initialize Redis connection and test it"""
    try:
        await redis_client.ping()
        return True
    except Exception as e:
        print(f"Redis connection failed: {str(e)}")
        return False

async def add_jti_to_blocklist(jti: str) -> None:
    """Add a JWT token ID to the blocklist"""
    try:
        await redis_client.set(
            name=f"blocklist:{jti}",
            value="1",
            ex=JTI_EXPIRY
        )
        return True
    except Exception as e:
        print(f"Error adding token to blocklist: {str(e)}")
        return False

async def token_in_blocklist(jti: str) -> bool:
    """Check if a JWT token ID is in the blocklist"""
    try:
        result = await redis_client.get(f"blocklist:{jti}")
        return result is not None
    except Exception as e:
        print(f"Error checking token blocklist: {str(e)}")
        return True  # Fail secure: if we can't check, assume token is blocked

# Cache utilities
async def set_cache(key: str, value: str, expires: int = JTI_EXPIRY) -> bool:
    """Set a key-value pair in Redis cache"""
    try:
        await redis_client.set(key, value, ex=expires)
        return True
    except Exception as e:
        print(f"Error setting cache: {str(e)}")
        return False

async def get_cache(key: str) -> str:
    """Get a value from Redis cache"""
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"Error getting cache: {str(e)}")
        return None




