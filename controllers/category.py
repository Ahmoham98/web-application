from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.category import Categories
from schema.category import CategoriesCreate, CategoriesUpdate


class CategoryController:
    def __init__(self, session):
        self.session = session
    
    async def post_category_controller(self, category_item: CategoriesCreate):
        category_dict = category_item.model_dump()
        new_category = Categories(
            **category_dict
        )
        self.session.add(new_category)
        await self.session.commit()
        await self.session.refresh(new_category)
        return new_category
    
    async def get_categories_controller(self):
        statement = select(Categories)
        result = await self.session.exec(statement)
        result = result.all()
        return result
    
    async def get_category_controller(self, title: str):
        statement = select(Categories).where(Categories.title == title)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="category with given id is not found! ")
        return result
    
    async def get_category_by_uid(self, uid: str):
        statement = select(Categories).where(Categories.uid == uid)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="category with given id is not found! ")
        return result
    
    async def delete_category_cotroller(self, title: str):
        result = await self.get_category_controller(title)
        if not result:
            raise HTTPException(status_code=404, detail="category with given id is not found! ")
        if not result:
            raise HTTPException(status_code=404, detail="category with given id not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "category deleted successfully!"}  # return a message to the client
    
    async def update_category_controller(self, category: CategoriesUpdate):
        result = await self.get_category_controller(category.title)
        
        if category.title is None:
            raise HTTPException(status_code=405, detail="title field required")
        elif category.title == "string":
            raise HTTPException(status_code=405, detail="title field required")
        else:
            result.title = category.title
        
        if category.description is not None:
            result.description = category.description
        
        if category.created_at is not None:
            result.created_at = category.created_at
        
        self.session.add(result)
        await self.session.commit()
        return {"massage": "success!"}
    
    async def update_category_put(self, category: CategoriesUpdate):
        result = await self.get_category_controller(category.title)
        
        for k, v in result.items():
            setattr(result, k, v)
        
        return {"message": "success"}

