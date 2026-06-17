
from pathlib import Path
import os

from fastapi import APIRouter
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from pydantic import SecretStr
from starlette.responses import JSONResponse
from colorama import Fore

from ..utils import IS_DEV

router = APIRouter(
    tags=["Emails"],
    include_in_schema=IS_DEV
)

# Validate for missing env values
missing_envs: list[str] = []
env_values: list[str] = ["PUBLIC_EMAIL_ENABLED", "MAIL_USERNAME", "MAIL_PASSWORD", "MAIL_FROM", "MAIL_PORT", "MAIL_SERVER", "MAIL_STARTTLS", "MAIL_SSL_TLS", "USE_CREDENTIALS", "VALIDATE_CERTS"]

for env_value in env_values:
    if os.getenv(env_value) is None:
        missing_envs.append(env_value)

if len(missing_envs) > 0:
    print(f"{Fore.YELLOW} Warning: Missing environment variables for emails: '{', '.join(missing_envs)}'. Defaults will be used.")

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "open-scouting"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", SecretStr("password")),  # pyright: ignore[reportArgumentType]
    MAIL_FROM = os.getenv("MAIL_FROM", "dev@open-scouting.com"),
    MAIL_PORT = int(os.getenv("MAIL_PORT", 1025)),
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost"),
    MAIL_STARTTLS = os.getenv("MAIL_STARTTLS", False) == "true",
    MAIL_SSL_TLS = os.getenv("MAIL_SSL_TLS", False) == "true",
    USE_CREDENTIALS = os.getenv("USE_CREDENTIALS", True) == "true",
    VALIDATE_CERTS = os.getenv("VALIDATE_CERTS", False) == "true",
    TEMPLATE_FOLDER = Path(__file__).parent.parent / "email_templates"
)

@router.post("/email")
async def send_verification_code(email: NameEmail, code: int) -> JSONResponse:
    """
    Send a verification code to an email, using an email template

    Parameters:
        email (NameEmail): The email to send the verification code to
        code (int): The verification code to send

    Returns:
        JSONResponse: A message indicating that the email has been sent
    """
    template_data = {
        "email": email,
        "verification_code": code
    }

    message = MessageSchema(
        subject=f"Open Scouting Verification Code - {code}",
        recipients=[email],
        template_body=template_data,
        subtype=MessageType.html
    )

    fm = FastMail(conf)

    if os.getenv("PUBLIC_EMAIL_ENABLED", "false") == "false":
        return JSONResponse(status_code=403, content={"message": "emails are disabled"})
    else:
        await fm.send_message(message, template_name="verification_code.html")
        return JSONResponse(status_code=200, content={"message": "email has been sent"})     