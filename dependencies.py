from typing import List
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from utils.utilities import decode_token
from sqlalchemy.ext.asyncio.session import AsyncSession
from database import get_session
from controllers.user import UserController
from models.user import Users
#redis token_blocklist
#from redis import token_in_blocklist

#Base class for doing all fo the jwt checks
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
    
        token = creds.credentials
        
        token_data = decode_token(token=token)
        
        if not self.token_valid(token=token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token"
                        }
            )
        
        """#aioredis part for revoke an access token and logout
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "This token is invalid or expired",
                    "resolution": "Please get new token"
                        }
            )"""
        
        
        self.verify_token_data(token_data=token_data)
        
        return token_data
    
    def token_valid(self, token: str) -> bool:
        
        token_data = decode_token(token=token)
        
        if token_data is not None:
            return True 
        else :
            return False
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes... ")
    
    

#child classes for checking access token and refresh token

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
            if token_data and token_data["refresh"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide an access token... "
                )

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
            if token_data and not token_data["refresh"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Please provide a refresh token... "
                )


async def get_current_user(
    *,
    session: AsyncSession = Depends(get_session),
    token_detail: dict = Depends(AccessTokenBearer())
):
    
    user_email = token_detail['user']['email']
    
    user = await UserController(session=session).get_user_by_email(email=user_email)
    
    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: Users = Depends(get_current_user)):
        
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough privileges"
        )
        


