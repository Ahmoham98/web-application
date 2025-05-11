from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from schema.user import UsersCreate, UsersUpdate, UsersUpdatePut
from models.user import Users
from utils.utilities import get_password_hash
from models.user import Users
from pydantic import EmailStr

class UserController:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_user_by_email(self, email: EmailStr):
        statement = select(Users).where(Users.email == email)
        result = await self.session.exec(statement)
        user = result.first()
        return user
    
    async def user_exists(self,  email: EmailStr):
        user = await self.get_user_by_email(email)
        
        if user :
            raise HTTPException(status_code=404, detail="user with given email already exists! ")
        
        return None
    
    # GET Functionalities
    async def get_users_controller(self):
        statement = select(Users)
        result = await self.session.exec(statement)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="No users found! ")
        return result
    
    async def get_user_controller(self, username: str):
        statement = select(Users).where(Users.username == username)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="User with given username not found!... ")
        return result

    #POST Functionalities
    async def create_user(self, user: UsersCreate):
        hashed_password = await get_password_hash(user.password)
        extra_data = {"hashed_password": hashed_password}
        user_dict = user.model_dump()
        user_dict.update(extra_data)
        new_user = Users(
            **user_dict
        )
        new_user.role = "user"
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
    
    # DELETE Functionalities
    async def delete_user_controller(self, username: str):
        statement = select(Users).where(Users.username == username)
        result = await self.session.exec(statement)
        result = result.first()
        if not result:
            raise HTTPException(status_code=404, detail="User with given username not found! ")
        await self.session.delete(result)
        await self.session.commit()
        
        return {"message": "user has been deleted successfully!"}
    
    #UPDATE Functionalities
    async def update_user_controller_put(self, user: UsersUpdatePut):
        db_user = await self.session.exec(select(Users).where(user.username == Users.username))
        db_user = db_user.one()
        
        if not db_user:
            HTTPException(status_code=400, detail=("No such user found for update... "))
        
        user_dict = user.model_dump()
        for k, v in user_dict.items():
            setattr(db_user, k, v)
        
        self.session.add(db_user)
        await self.session.commit()
        return {"massage": "success!"}
    
    async def update_user_controller(self, user: UsersUpdate):
        db_user = await self.session.exec(select(Users).where(user.username == Users.username))
        db_user = db_user.one()
        if user.username is None:
            raise HTTPException(status_code=405, detail="username field required")
        elif user.username == "string":
            raise HTTPException(status_code=405, detail="username field required")
        else:
            db_user.username = user.username
        
        if user.password is not None:
            user.password = await get_password_hash(user.password)
            db_user.hashed_password = user.password
        
        if user.email is not None:
            db_user.email = user.email
        
        if user.phone is not None:
            db_user.phone = db_user.phone
        
        if user.first_name is not None:
            db_user.first_name = user.first_name
        
        if user.last_name is not None:
            db_user.last_name = user.last_name
        
        if user.address is not None:
            db_user.address = user.address
        
        if user.role is not None:
            db_user.role = user.role
        
        if user.created_at is not None:
            db_user.created_at = user.created_at
        
        self.session.add(db_user)
        await self.session.commit()
        return {"massage": "success!"}
    
    async def update_user(self, user: Users, user_data: dict):
        
        for k, v in user_data.items():
            setattr(user, k, v)
        
        await self.session.commit()
        
        return user
        





