from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from jinja2 import Template
import ssl
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
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465 
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
PROJECT_NAME = "Whistler microservices"
SERVER_HOST = settings.SERVER_HOST
ACCESS_TOKEN_EXPIRE_SECONDS = 3600 

def read_template(template_name: str) -> str:
    print(settings.EMAIL_TEMPLATES_DIR)
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

    # Render the subject
    if isinstance(subject_template, JinjaTemplate):
        subject = subject_template.render(**environment)
    else:
        # If it's a string, render it as a Jinja template
        subject = Template(subject_template).render(**environment)

    # Render the HTML content
    if isinstance(html_template, JinjaTemplate):
        html_content = html_template.render(**environment)
    else:
        html_content = Template(html_template).render(**environment)

    # Create a MIMEMultipart message
    mime_message = MIMEMultipart()
    mime_message['Subject'] = subject
    mime_message['From'] = EMAILS_FROM_EMAIL
    mime_message['To'] = email_to

    # Attach the HTML content
    mime_message.attach(MIMEText(html_content, 'html'))

    smtp_options = {
        "hostname": SMTP_HOST,
        "port": SMTP_PORT,
        "username": settings.SMTP_USER,
        "password": settings.SMTP_PASSWORD,
        "use_tls": EMAIL_USE_TLS,
        "tls_context": ssl.create_default_context(),
    }

    environment.update({
        "server_host": SERVER_HOST,
        "project_name": PROJECT_NAME,
    })

    try:
        async with SMTP(**smtp_options) as smtp:
            response = await smtp.send_message(mime_message)
            # rendered_message = message.render(**environment)
            # response = await smtp.send_message(rendered_message.as_string(),sender=EMAILS_FROM_EMAIL, recipients=[email_to])
            logger_system.info(f"send email result: {response}")
    except Exception as e :
        logger_system.error(f"Failed to send email : {str(e)}")
        raise

async def send_email_validation_email(data: EmailValidation) -> None:
    subject = f"{PROJECT_NAME} - {data.subject}"
    link = f"{SERVER_HOST}/users/verify?token={data.token.get_secret_value()}"
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
