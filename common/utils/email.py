from pathlib import Path
from typing import Any, Dict
from common.config import settings
import emails
from emails.template import JinjaTemplate
from aiosmtplib import SMTP
from user_service.schemes import EmailValidation
from common.utils.logger import logger_system 

EMAILS_FROM_NAME = "Whitslter"
EMAILS_FROM_EMAIL = "no-reply@example.com"
EMAILS_TO_EMAIL = "contact@example.com"
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_TLS = True
PROJECT_NAME = "Whistler microservices"
SERVER_HOST = settings.SERVER_HOST
ACCESS_TOKEN_EXPIRE_SECONDS = 3600 

def read_template(template_name: str) -> str:
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / template_name) as f:
        return f.read()

async def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
    template_name: str = None,
) -> None:
    if template_name:
        html_template = read_template(template_name)

    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(EMAILS_FROM_NAME, EMAILS_FROM_EMAIL),
    )

    smtp_options = {
        "hostname": SMTP_HOST,
        "port": SMTP_PORT,
        "username": settings.SMTP_USER,
        "password": settings.SMTP_PASSWORD,
        "use_tls": SMTP_TLS,
    }

    environment.update({
        "server_host": SERVER_HOST,
        "project_name": PROJECT_NAME,
    })

    async with SMTP(**smtp_options) as smtp:
        response = await smtp.send_message(message, to=email_to, render=environment)
        logger_system.info(f"send email result: {response}")

async def send_email_validation_email(data: EmailValidation) -> None:
    subject = f"{PROJECT_NAME} - {data.subject}"
    link = f"{SERVER_HOST}?token={data.token}"
    template_name = "confirm_email.html"
    await send_email(
        email_to=data.email,
        subject_template=subject,
        template_name=template_name,
        environment={'link': link}
    )

async def send_test_email(email_to: str) -> None:
    subject = f"{PROJECT_NAME} - Test email"
    template_name = "test_email.html"
    await send_email(
        email_to=email_to,
        subject_template=subject,
        template_name=template_name,
        environment={"project_name": PROJECT_NAME, "email": email_to},
    )

async def send_magic_login_email(email_to: str, token: str) -> None:
    subject = f"Your {PROJECT_NAME} magic login"
    template_name = "magic_login.html"
    link = f"{SERVER_HOST}?magic={token}"
    await send_email(
        email_to=email_to,
        subject_template=subject,
        template_name=template_name,
        environment={
            "project_name": PROJECT_NAME,
            "valid_minutes": int(ACCESS_TOKEN_EXPIRE_SECONDS / 60),
            "link": link,
        },
    )

async def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    subject = f"{PROJECT_NAME} - Password recovery for user {email}"
    template_name = "reset_password.html"
    link = f"{SERVER_HOST}/reset-password?token={token}"
    await send_email(
        email_to=email_to,
        subject_template=subject,
        template_name=template_name,
        environment={
            "project_name": PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": int(ACCESS_TOKEN_EXPIRE_SECONDS / 60),
            "link": link,
        },
    )

async def send_new_account_email(email_to: str, username: str, password: str) -> None:
    subject = f"{PROJECT_NAME} - New account for user {username}"
    template_name = "new_account.html"
    link = SERVER_HOST
    await send_email(
        email_to=email_to,
        subject_template=subject,
        template_name=template_name,
        environment={
            "project_name": PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
