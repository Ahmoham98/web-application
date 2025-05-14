#//////////////////// Typing, Date and time importations ////////////////////////
from typing import Annotated
from datetime import timedelta, datetime

#//////////////////// fastapi, sqlmodel and pydantic importations ////////////////////////
from fastapi import HTTPException, status, Header, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

#//////////////////// Asyncsession ////////////////////////
from database import get_session

#//////////////////// Models and Schemas importations ////////////////////////
from models.user import Users
from schema.user import (
    UsersCreate,
    UsersPublic,
    UsersUpdate,
    UsersUpdatePut
)
from schema.login import UserLoginModel
from schema.email import EmailModel, PasswrodResetRequestModel, PasswordResetConfirmModel

#//////////////////// Controllers class importation ////////////////////////
from controllers.user import UserController

from pydantic import EmailStr

from utils.utilities import (
    create_access_token,
    decode_token,
    verify_password,
    create_url_safe_token,
    decode_url_safe_token,
    get_password_hash
)

from dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker

from mail import mail, create_message

from configure import Config

#from redis import add_jti_to_blocklist

from celery_tasks import send_email

access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(["admin", "soldier"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRY = 2


router = APIRouter(
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    *,
    session: AsyncSession = Depends(get_session),
    user: UsersCreate,
    bg_tasks: BackgroundTasks,
):
    email = user.email
    user_exists = await UserController(session=session).user_exists(email=email)
    new_user = await UserController(session=session).create_user(user=user)
    
    token = create_url_safe_token({"email": email})
    
    link = f"http://{Config.DOMAIN}/api/v1/users/verify_email/{token}"
    
    html_message = f"""
    <h1>Verify your email</h1>
    <p>Please click this <a href={link}>link</a> to verify your email</p>
    """
    
    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_message
    )
    
    bg_tasks.add_task(mail.send_message, message)
    
    
    return {
        "messaeg": "Account has been successfully created! Check your email inbox to verify your account... ",
        "user": new_user
    }

@router.post("/login")
async def login_user(
    *,
    session: AsyncSession = Depends(get_session),
    login_data: UserLoginModel
):
    email = login_data.email
    password = login_data.password
    user = await UserController(session=session).get_user_by_email(email=email)
    
    if user :
        password_valid = verify_password(password=password, hashed_password=user.hashed_password)
        
        if password_valid:
            
            user_data = {
                'email': user.email, 
                'user_uid': str(user.uid),
                'role': user.role,
            }
            
            access_token = create_access_token(
                token=user_data
            )
            
            refresh_token = create_access_token(
                token=user_data,
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse(
                content={
                    "message": "login successful!",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email": user.email,
                        "uid": str(user.uid)
                    }
                }
            )
            
        
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid email or password!"
    )

@router.get('/verify_email/{token}')
async def verify_user_account(
    *,
    session: AsyncSession = Depends(get_session),
    token: str
):
    token_data = decode_url_safe_token(token=token)
    user_email = token_data.get("email")
    
    if user_email:
        user = await UserController(session=session).get_user_by_email(email=user_email)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User with given email not found"
            )
        await UserController(session=session).update_user(user=user, user_data={'is_verified': True})
        
        return JSONResponse(
            content={
                "message": "You have been verified successfully :)",
                "instructions": "Now you can simple login"
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={
            "message": "Error occurred during verification"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    
    expiry_timestamp = token_details["exp"]
    
    user_data = token_details['user']
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            token=user_data
        )
        
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid or expired token"
    )


"""@router.get("/logout")
async def revoke_token(token_details: dict = Depends(access_token_bearer)):
    
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti=jti)
    
    return JSONResponse(
        content={
            "message": "User logged out successfully!"
        }
    )
"""
@router.get("/me")
async def get_current_user(
    user: dict = Depends(get_current_user),
    _:bool = Depends(role_checker)
):
    return user



@router.post('/send_mail')
async def send_mail(email: EmailModel):
    emails = email.addresses
    
    html_message = "<h1>Welcome to the app</h1>"
    
    #you can also call it as celery task: 
    """
    -- for using this line of code, you need to remove next to code part "(message that call the create massege 
    function and bg_tasks that push the send mail to background to handle it as background task)" --
    
    subject = "Welcome to our app"
    
    send_email.delay(recipients=emails, subject=subject, body=html_message)
    
    # you need to create a worker with the following command
    $ celecy -A celery_tasks.c_app worker
             -- path to the celery app 
    """
    
    message = create_message(
        recipients=emails,
        subject="Welcome",
        body=html_message
    )
    
    await mail.send_message(message)
    
    return {"message": "Email sent successfully!"}



@router.post('/password-reset-request')
async def password_reset_request(email_data: PasswrodResetRequestModel):
    email = email_data.email
    
    token = create_url_safe_token({"email": email})
    
    link = f"http://{Config.DOMAIN}/api/v1/users/password-reset-confirm/{token}"
    
    html_message = f"""
    <h1>Reset your password</h1>
    <p>Please click this <a href={link}>link</a> to reset your password </p>
    """
    message = create_message(
        recipients=[email],
        subject="Password Recovery",
        body=html_message
    )
    
    await mail.send_message(message)
    
    
    return JSONResponse(
        content={
            "message": "please check your email for instructions to reset your password",
            "token": f"{token}"
        },
        status_code=status.HTTP_200_OK
    )



@router.post('/password-reset-confirm/{token}')
async def reset_account_password(
    *,
    session: AsyncSession = Depends(get_session),
    token: str,
    passwords: PasswordResetConfirmModel,
):
    new_password = passwords.new_password
    confirm_new_password = passwords.confirm_new_password
    if new_password != confirm_new_password:
        raise HTTPException(detail='Passwords do not match!', status_code=status.HTTP_400_BAD_REQUEST)
    token_data = decode_url_safe_token(token=token)
    user_email = token_data.get("email")
    
    if user_email:
        user = await UserController(session=session).get_user_by_email(email=user_email)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User with given email not found"
            )
        
        password_hash = await get_password_hash(new_password)
        await UserController(session=session).update_user(user=user, user_data={'hashed_password': password_hash})
        
        return JSONResponse(
            content={
                "message": "Your password have been reset successfully :)"
            },
            status_code=status.HTTP_200_OK
        )
    
    
    return JSONResponse(
        content={
            "message": "Error occurred during Password Reset"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )





@router.get("/", response_model=list[UsersPublic], openapi_extra={"x-aperture-labs-portal": "blue"}, operation_id="users_getusers_userviews_getall")
async def get_users(
    *,
    session: AsyncSession = Depends(get_session),
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    """ 
        Handles get_all user requests and hand it over to the backend to get all the users 
            ** you need admin access for this operation **
    """

    result = await UserController(session=session).get_users_controller()
    return result

#Creating a post request endpoint to /users
@router.post("/", response_model=UsersPublic)
async def create_user(*, session: AsyncSession = Depends(get_session), user : UsersCreate):
    """
        Handles post user request and hand it over to the backend to create a new user with given data
    """
    user_exists = await UserController(session=session).user_exists(email=user.email)
    result = await UserController(session=session).create_user(user=user)
    return result

#Creating get request endpoint with sending parameters to /users with /users/{id}  done *_*
@router.get("/{user_username}/")
async def get_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_username: str,
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    """ 
        Handles get user requests with the given username and hand it over to the backend to get the user with the given username
            ** you need admin access for this operation **          make sure you type valid email, it will be used for your password recovery
    """
    result = await UserController(session=session).get_user_controller(username=user_username)
    return result

@router.delete("/{user_username}")
async def delete_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_username: str,
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    """
        Handles delete requests and hand it over to the backend to manage delete operation
    """
    result = await UserController(session=session).delete_user_controller(username=user_username)
    return result

@router.put ("/",)
async def update_user(
    *,
    session: AsyncSession = Depends(get_session),
    user: UsersUpdatePut,
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    """
        Handles full update and send it over to the backend to manage the put operation
    """
    result = await UserController(session=session).update_user_controller_put(user=user)
    return result

@router.patch ("/")
async def update_user(
    *,
    session: AsyncSession = Depends(get_session),
    user: UsersUpdate,
    token_details = Depends(access_token_bearer),
    _:bool = Depends(role_checker),
):
    """
        Handles partial update and send it over to the backend to manage the update oparation
    """
    result = await UserController(session=session).update_user_controller(user=user)
    return result








