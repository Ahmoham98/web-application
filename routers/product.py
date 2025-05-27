#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
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
is_pharmacist = RoleChecker(["pharmacist"])


product_router = APIRouter()

@product_router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductsPublic)
async def create_product(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
    category_title: str,
    product: ProductsCreate,
):
    user_uid = token_details.get('user')['user_uid']
    created_product = await ProductController(session=session).create_product(
        user_uid=user_uid, 
        category_title=category_title, 
        product=product
    )
    return created_product

@product_router.get("/", response_model=list[ProductsPublic])
async def read_products(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
):
    """Get all products from the database """
    return await ProductController(session=session).get_products_controller() 

@product_router.get("/{product_uid}", response_model=ProductsPublic)
async def read_product(
    *,
    session: AsyncSession = Depends(get_session),
    product_uid: str,
    token_details=Depends(access_token_bearer),
    _: bool = Depends(role_checker),
):
    """get specific product by uid"""
    return await ProductController(session=session).get_product_controller(uid=product_uid)

@product_router.delete("/{product_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    product_uid: str,  # Fixed type annotation
    _:bool = Depends(role_checker),
):
    """Delete a product by product uid"""
    await ProductController(session=session).delete_product_controller(uid=product_uid)
    return None

@product_router.put("/{product_uid}", response_model=ProductsPublic)
async def update_product(
    *,
    product_uid: str,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _: bool = Depends(role_checker)
):
    """Update a product by product uid"""
    return await ProductController(session=session).update_product_controller_put(
        uid=product_uid,
        data=product_data
    )

