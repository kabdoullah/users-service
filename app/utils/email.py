from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi.background import BackgroundTasks

from app.configuration.config import EmailSettings


email_settings = EmailSettings()

conf = ConnectionConfig(
    MAIL_USERNAME = email_settings.MAIL_USERNAME,
    MAIL_PASSWORD = email_settings.MAIL_PASSWORD,
    MAIL_FROM = email_settings.MAIL_FROM,
    MAIL_PORT = email_settings.MAIL_PORT,
    MAIL_SERVER = email_settings.MAIL_SERVER,
    MAIL_FROM_NAME=email_settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

fm = FastMail(conf)

async def send_otp_email(email: str, otp: str, background_tasks: BackgroundTasks):
    html = f"""<p>Your OTP code is: {otp}</p> """

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    background_tasks.add_task(fm.send_message, message)
