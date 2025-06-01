from email.message import EmailMessage
import aiosmtplib
from src.core.config import settings  # путь к твоему Settings-классу
from aiosmtplib import SMTP

async def send_invite_email(email: str, token: str, domein: str):
    if not all([settings.SMTP_FROM, settings.SMTP_HOST, settings.SMTP_PORT, settings.SMTP_USER, settings.SMTP_PASS]):
        raise ValueError("SMTP configuration is incomplete")

    msg = EmailMessage()
    msg["From"] = settings.SMTP_FROM
    msg["To"] = email
    msg["Subject"] = "Приглашение в команду"

    invite_url = f"http://teamflow.com/{domein}/invite/{token}"
    msg.set_content(f"Вас пригласили в организацию. Зарегистрируйтесь по ссылке:\n\n{invite_url}")

    smtp = SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT, use_tls=True)
    await smtp.connect()
    await smtp.login(settings.SMTP_USER, settings.SMTP_PASS)
    await smtp.send_message(msg)
    await smtp.quit()
