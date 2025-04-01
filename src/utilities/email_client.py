from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

from config.configs import email_settings


class EmailClient:
    async def send_mail(
        self,
        recepients: List[EmailStr],
        body: str,
        subject: str = "Your verify code",
    ) -> dict:
        massage = MessageSchema(
            recipients=recepients, subject=subject, body=body, subtype="plain"
        )
        conf = ConnectionConfig(
            MAIL_USERNAME=email_settings.MAIL_USERNAME,
            MAIL_PASSWORD=email_settings.MAIL_PASSWORD,
            MAIL_FROM=email_settings.MAIL_FROM,
            MAIL_PORT=email_settings.MAIL_PORT,
            MAIL_SERVER=email_settings.MAIL_SERVER,
            MAIL_STARTTLS=email_settings.MAIL_STARTTLS,
            MAIL_SSL_TLS=email_settings.MAIL_SSL_TLS,
        )
        fast_mail = FastMail(config=conf)
        try:
            await fast_mail.send_message(message=massage)
        except Exception as e:
            raise Exception(str(e))
        return {"message": "Message sent successfully if status_code is 1"}


email_client = EmailClient()
