#from sqlmodel import Session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from configure import Config

#create asynchronous connection and connection creating a connection pool
async_engine = create_async_engine(
    Config.DATABASE_URL,
    pool_size= 10,  #maximum number of permanent connection to maintain in the pool
    max_overflow=10,    #maximum number of additional connection that can be created if the pool ia exhausted
    pool_timeout=30,    #number of seconds to wait for a connection if the pool is exhausted
    pool_recycle=1800   #maximum age (in seconds) of connection that can be reused
)


#Configuring Session Local
AsyncSessionLocal = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session



"""# For Async support
engine = create_async_engine(
    DATABASE_URL,
    echo= True, #Log sql queries for debugging
    pool_size=10,   #maximum number of permanent connection to maintain in the pool
    max_overflow=10,    #maximum number of additional connection that can be created if the pool ia exhausted
    pool_timeout=30,    #number of seconds to wait for a connection if the pool is exhausted
    pool_recycle=1800   #maximum age (in seconds) of connection that can be reused
)
"""
"""#Configuring Session Local
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession,
)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session"""