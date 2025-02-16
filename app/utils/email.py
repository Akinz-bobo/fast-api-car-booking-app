from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
conf = ConnectionConfig(
    MAIL_USERNAME= settings.SMTP_USERNAME,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAIL_SENDER,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_SERVER,
    MAIL_STARTTLS=True,  # Use this instead of MAIL_TLS
    MAIL_SSL_TLS=False,  # Use this instead of MAIL_SSL
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(subject: str, email_to: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)