from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException

from models.product import Products
from schema.product import ProductsCreate, ProductUpdate

from controllers.category import CategoryController

class ProductController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_product(self, user_uid: str, category_title: str, product: ProductsCreate):
        
        category = await CategoryController(session=self.session).get_category_controller(title=category_title)
        category_uid = category.uid
        
        product_dict = product.model_dump()
        new_product = Products(
            **product_dict
        )
        
        new_product.users_uid = user_uid
        new_product.category_uid = category_uid
        new_product.is_active = True
        new_product.status = "Live"
        
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product
    
    #post product
    async def post_product_controller(self, product: ProductsCreate):
        db_product = Products.model_validate(product)
        self.session.add(db_product)
        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product
    
    #get all products
    async def get_products_controller(self):
        statement = select(Products)
        product = await self.session.exec(statement)
        product = product.all()
        return product
    
    #get product
    async def get_product_controller(self, title: str):
        statement = select(Products).where(Products.title == title)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="product with the given id not found! ")
        return result
    
    #delete product
    async def delete_product_controller(self, title: str):
        statement = select(Products).where(Products.title == title)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="product with given title not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "product deleted successfully!"}  # return a message to the client
    
    # update product
    async def update_product_controller(self, product: ProductUpdate):
        statement = select(Products).where(Products.title == product.title)
        db_product = await self.session.exec(statement)
        db_product =db_product.first()
        if product.title is None:
            raise HTTPException(status_code=405, detail="title field required")
        elif product.title == "string":
            raise HTTPException(status_code=405, detail="title field required")
        else:
            db_product.title = product.title
        
        if product.description is not None:
            db_product.description = product.description
        
        if product.unit_price is not None:
            db_product.unit_price = product.unit_price
        
        if product.sale_price is not None:
            db_product.sale_price = product.sale_price
        
        if product.is_active is not None:
            db_product.is_active = product.is_active
        
        if product.status is not None:
            db_product.status = product.status
        
        if product.created_at is not None:
            db_product.created_at = product.created_at
        
        if product.updated_at is not None:
            db_product.updated_at = product.updated_at
        
        
        self.session.add(db_product)
        await self.session.commit()
        return {"massage": "success!"}

