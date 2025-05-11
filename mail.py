from typing import List
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from configure import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mail_config = ConnectionConfig(
    MAIL_USERNAME = "electricallover45",
    MAIL_PASSWORD = "some password",
    MAIL_FROM = "electricallover45@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmai.com",
    MAIL_FROM_NAME= "BassalmBackendSupport",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER=Path(BASE_DIR, 'templates')
)

mail = FastMail(
    config=mail_config
)


def create_message(recipients: List[str], subject: str, body: str,):
    
    
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
        
    )
    
    return message




