import bcrypt
from datetime import datetime ,timedelta
import jwt
from configure import Config
import uuid
import logging
from itsdangerous import URLSafeSerializer

ACCESS_TOKEN_EXPIRY = 3600


async def get_password_hash(password):
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt()).decode()


def verify_password(password, hashed_password):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password=password, hashed_password=hashed_password)


def create_access_token(token: dict, expiry: timedelta = None, refresh: bool = False):
    
    payload = {}
    
    payload['user'] = token
    if expiry:
        payload['exp'] = datetime.now() + expiry
    else:
        payload['exp'] = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY)
        
    payload['jti'] = str(uuid.uuid4())
    
    payload['refresh'] = refresh
    
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    
    return token


def decode_token(token: str) -> dict:
    
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return {"message": "not encoded"}

serializer = URLSafeSerializer(
    secret_key=Config.JWT_SECRET,
    salt="email-salt-for-configguration"
)

def create_url_safe_token(data: dict):
    token = serializer.dumps(data)
    return token


def decode_url_safe_token(token: str):
    try:
        token_data = serializer.loads(token)
        return token_data
    except Exception as e:
        logging.error(str(e))

