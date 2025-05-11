#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from schema.category import (
    CategoriesCreate,
    CategoriesPublic,
    CategoriesUpdate
)

#//////////////////// Controllers class importation ////////////////////////
from controllers.category import CategoryController

#//////////////////// dependencies ////////////////////////
from dependencies import AccessTokenBearer, RoleChecker


access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "soldier"])

category_router = APIRouter()



@category_router.post("/", response_model=CategoriesPublic)
async def create_order(
    *,
    session: AsyncSession = Depends(get_session),
    category_item: CategoriesCreate,
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).post_category_controller(category_item=category_item)

@category_router.get("/")            # need to be fixed
async def get_orders(
    *,
    session: AsyncSession = Depends(get_session),
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).get_categories_controller()

@category_router.get("/{category_title}")
async def get_order(
    *,
    session: AsyncSession = Depends(get_session),
    title: str,
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).get_category_controller(title=title)

@category_router.get("/uid")
async def get_order(
    *,
    session: AsyncSession = Depends(get_session),
    uid: str,
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).get_category_by_uid(uid=uid)

@category_router.delete("/{category_title}")
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    title: str,
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).delete_category_cotroller(title=title)

@category_router.patch ("/")
async def update_category(
    *,
    session: AsyncSession = Depends(get_session),
    category: CategoriesUpdate,
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).update_category_controller(category=category)

@category_router.put("/")
async def update_category_put(
    *,
    session: AsyncSession = Depends(get_session),
    category: CategoriesUpdate,
    user_data = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    return await CategoryController(session=session).update_category_put(category=category)


