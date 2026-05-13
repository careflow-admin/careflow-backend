import logging
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.config.settings import (
    SMTP_FROM_EMAIL,
    SMTP_FROM_NAME,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_TIMEOUT,
    SMTP_USE_SSL,
    SMTP_USE_TLS,
    SMTP_USERNAME,
)

logger = logging.getLogger(__name__)


def send_email(
    to_email: str, subject: str, body: str, html_body: Optional[str] = None
) -> None:
    missing = []
    if not SMTP_USERNAME:
        missing.append("SMTP_USERNAME")
    if not SMTP_PASSWORD:
        missing.append("SMTP_PASSWORD")
    if not SMTP_FROM_EMAIL:
        missing.append("SMTP_FROM_EMAIL")
    if missing:
        raise RuntimeError("Missing SMTP settings: " + ", ".join(missing))

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = _format_from()
    msg["To"] = to_email
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    try:
        if SMTP_USE_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT)

        with server:
            server.ehlo()
            if SMTP_USE_TLS and not SMTP_USE_SSL:
                server.starttls()
                server.ehlo()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception:
        logger.exception("Error sending email to %s", to_email)
        raise


def send_otp_email(to_email: str, codigo: str) -> None:
        subject = "Codigo OTP CareFlow"
        body = (
                f"Tu codigo OTP es: {codigo}\n\n"
                "Este codigo vence en 10 minutos.\n\n"
                "Si no solicitaste este codigo, ignora este correo."
        )
        html_body = f"""\
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Codigo OTP</title>
    </head>
    <body style="margin:0;padding:0;background-color:#f5f6f8;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color:#f5f6f8;padding:24px 0;">
            <tr>
                <td align="center">
                    <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color:#ffffff;border:1px solid #e6e8eb;border-radius:8px;overflow:hidden;font-family:Arial, sans-serif;color:#111827;">
                        <tr>
                            <td style="padding:24px 28px;background-color:#0f172a;color:#ffffff;">
                                <div style="font-size:18px;font-weight:700;">CareFlow</div>
                                <div style="font-size:13px;opacity:0.85;">Codigo OTP</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:28px;">
                                <p style="margin:0 0 12px;font-size:15px;line-height:1.5;">Hola,</p>
                                <p style="margin:0 0 16px;font-size:15px;line-height:1.5;">Usa este codigo para completar tu verificacion:</p>
                                <div style="font-size:28px;font-weight:700;letter-spacing:4px;padding:12px 16px;background:#f3f4f6;border-radius:6px;display:inline-block;">
                                    {codigo}
                                </div>
                                <p style="margin:16px 0 0;font-size:13px;color:#6b7280;">Este codigo vence en 10 minutos.</p>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:16px 28px;background-color:#f9fafb;font-size:12px;color:#6b7280;">
                                Si no solicitaste este codigo, puedes ignorar este correo.
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
"""
        send_email(to_email, subject, body, html_body=html_body)


def _format_from() -> str:
    if SMTP_FROM_NAME:
        return f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    return SMTP_FROM_EMAIL
