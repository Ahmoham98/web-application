from fastapi import FastAPI
from sqlmodel import SQLModel
from database import async_engine
from contextlib import asynccontextmanager
from routers import user, category, product
#from Middleware import register_middleware

DEFAULT_EXPIRATION = 3600

# create all the table models that we have in our metadata
async def create_db_tables():
    async with async_engine.begin() as conn:
        from models import user
        await conn.run_sync(SQLModel.metadata.create_all)


description = """
## Users
You will be able to:

* **Create users**
* **Read users**
* **update users**
* **update users**

## products
You will be able to:
* **Create products**
* **Read products**
* **update products**
* **delete products**

## orders
You will be able to:
* **Create orders**
* **Read orders**
* **update orders**
* **delete orders**


## order_items
You will be able to:
* **Create order items**
* **read order items**
* **update order items**
* **delete order items**


## categories
You will be able to:
* **Create categories**
* **Read categories**
* **update categories**
* **delete categories**

"""
tags_metadata = [
    {
        "name": "users",
        "description": "users endpoints. **login** Logic also implemented in here"
    },
    {
        "name": "products",
        "description": "products endpoints. **getting** & **reading** the products"
    },
    {
        "name": "orders",
        "description": "orders endpoints. **getting** & **reading** orders"
    },
    {
        "name": "order_items",
        "description": "order_items endpoints. **getting** & **reading** order_items"
    },
    {
        "name": "categories",
        "description": "categories endpoints. **getting** & **reading** categories"
    },
    {
        "name": "admin",
        "description": "admin part. for uploading and different accesses type from normal user"
    },
    {
        "name": "default",
        "description": "**get** root to check the server functionality and some other case usage"
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    #Load the database
    await create_db_tables()
    
    yield

version = "v1"

app = FastAPI(
    title="Online Pharmacy API's",
    description=description,
    summary="Online Pharmacy: save time by getting requirements online...",
    version="0.0.7",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

#register_middleware(app=app)


app.include_router(user.router, prefix= f"/api/{version}/users" ,tags=["users"])
app.include_router(category.category_router, prefix=f"/api/{version}/categories", tags=["categories"])
app.include_router(product.product_router, prefix=f"/api/{version}/products", tags=["products"])


@app.get("/")
async def get_root():
    return {"message": "Welcome you just loged in as root! "}


#redis in-memory caching
"""
you need to create a database and connect it using Redis class from redis python library...

import redis
r = redis.Redis(host='localhost', port=6379, db=0)

r.set('name', "Ahmad")

if r.get("name"):
    print ("cache hit")
else:
    print ("cache miss")"""

#fastapi caching
"""
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# with on_event declaration:
redis = aioredis.from_url("reids://localhost", encoding="utf8", decode_responses=True)
FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache:")
    
cache declaration after endpoint declaration:
@cache(expire=60)

"""

# reids caching with aiocache
"""
from aiocache import Cache
from aiocache.serializers import JsonSerializer
from fastapi import FastAPI, Depends

app = FastAPI()
cache = Cache(Cache.MEMORY, serializer=JsonSerializer()) / # OR YOU CAN GO FOR: / cache = Cache.from_url("redis://localhost:6379/0", serializer=JsonSerializer)

async def get_cache():
    return cache

@app.get ("items/{items_id})
async def read_item(item_id: int, cache: Cache = Depends(get_cache)):
    cache_key = f"item_{item_id}"
    item = await cache.get(cache_key)
    if item is not None:
        return item
    # Assume get_item_from_db is a function to fetch item from the database
    item = await get_item_from_db(item_id)
    await cache.set(cache_key, item, ttl= 10 * 60)  #cache for 10 minutes
    return item
"""
