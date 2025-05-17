from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime

from models.product import Products
from schema.product import ProductsCreate, ProductUpdate

from controllers.category import CategoryController

class ProductController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def _check_title_exists(self, title: str, exclude_uid: str = None) -> bool:
        """Check if a product with given title exists"""
        query = select(Products).where(Products.title == title)
        if exclude_uid:
            query = query.where(Products.uid != exclude_uid)
        result = await self.session.exec(query)
        return result.first() is not None

    async def create_product(self, user_uid: str, category_title: str, product: ProductsCreate):
        # Check if product with same title exists
        if await self._check_title_exists(product.title):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this title already exists"
            )
        
        # Get category
        try:
            category = await CategoryController(session=self.session).get_category_controller(title=category_title)
        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category not found: {category_title}"
            )
        
        product_dict = product.model_dump()
        new_product = Products(
            **product_dict,
            users_uid=user_uid,
            category_uid=category.uid,
            is_active=True,
            status="Live"
        )
        
        try:
            self.session.add(new_product)
            await self.session.commit()
            await self.session.refresh(new_product)
            return new_product
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating product: {str(e)}"
            )
    
    async def get_products_controller(self):
        statement = select(Products)
        try:
            result = await self.session.exec(statement)
            return result.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching products: {str(e)}"
            )
    
    async def get_product_controller(self, uid: str):
        statement = select(Products).where(Products.uid == uid)
        try:
            result = await self.session.exec(statement)
            product = result.first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product not found..."
                )
            return product
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching product: {str(e)}"
            )
    
    async def delete_product_controller(self, uid: str):
        statement = select(Products).where(Products.uid == uid)
        try:
            result = await self.session.exec(statement)
            product = result.first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product not found: {uid}"
                )
            
            await self.session.delete(product)
            await self.session.commit()
            
        except HTTPException:
            raise
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting product: {str(e)}"
            )
    
    async def update_product_controller_put(self, uid: str, data: ProductUpdate):
        # First check if product exists
        statement = select(Products).where(Products.uid == uid)
        try:
            result = await self.session.exec(statement)
            product = result.first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product not found: {uid}"
                )
            
            # If title is being updated, check for duplicates
            if data.title and data.title != product.title:
                if await self._check_title_exists(data.title, exclude_uid=uid):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Product with this title already exists"
                    )
            
            # Update fields if provided
            update_data = data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(product, field, value)
            
            # Update the updated_at timestamp
            product.updated_at = datetime.utcnow()
            
            self.session.add(product)
            await self.session.commit()
            await self.session.refresh(product)
            
            return product
            
        except HTTPException:
            raise
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating product: {str(e)}"
            )
