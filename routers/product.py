#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from models.product import Products
from schema.product import (
    Productsbase,
    ProductsCreate,
    ProductsPublic,
    ProductUpdate
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.product import ProductController

#//////////////////// dependencies importation ////////////////////////
from dependencies import AccessTokenBearer, RoleChecker


access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "soldier"])


product_router = APIRouter()

from controllers.product import ProductController

@product_router.post("/")
async def create_product(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    category_title: str,
    product: ProductsCreate,
):
    user_uid = token_details.get('user')['user_uid']
    created_product = await ProductController(session=session).create_product(user_uid=user_uid, category_title=category_title, product=product)
    return created_product

@product_router.get("/")
async def read_products(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await ProductController(session=session).get_products_controller() 

@product_router.get("/title")
async def read_product(
    *,
    session: AsyncSession = Depends(get_session),
    title: str,
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await ProductController(session=session).get_product_controller(title=title)

@product_router.delete("/")
async def delete_product(
    *,
    session: AsyncSession = Depends(get_session),
    title: str,
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await ProductController(session=session).delete_product_controller(title=title)

@product_router.patch ("/", deprecated=True)
async def update_product(*, session: AsyncSession = Depends(get_session), product: ProductUpdate,):
    return await ProductController(session=session).update_product_controller(product)