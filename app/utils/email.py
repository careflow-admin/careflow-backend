import base64
import json
import logging
import smtplib
import time
import urllib.error
import urllib.parse
import urllib.request
from email.message import EmailMessage
from typing import Optional

from app.config.settings import (
    GMAIL_API_CLIENT_ID,
    GMAIL_API_CLIENT_SECRET,
    GMAIL_API_FROM_EMAIL,
    GMAIL_API_FROM_NAME,
    GMAIL_API_REFRESH_TOKEN,
    GMAIL_API_TIMEOUT,
    RESEND_API_KEY,
    RESEND_FROM_EMAIL,
    RESEND_FROM_NAME,
    RESEND_TIMEOUT,
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
_gmail_access_token: Optional[str] = None
_gmail_access_token_expires_at: float = 0.0


def _print_email_error(provider: str, to_email: str, error: Exception) -> None:
    print(f"[email] provider={provider} to={to_email} error={error}")


def _build_email_message(
    from_address: str,
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_email
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")
    return msg


def send_email(
    to_email: str, subject: str, body: str, html_body: Optional[str] = None
) -> None:
    if _gmail_api_any_configured():
        if not _gmail_api_configured():
            raise RuntimeError(
                "Partial Gmail API settings found. Set GMAIL_API_CLIENT_ID, "
                "GMAIL_API_CLIENT_SECRET, GMAIL_API_REFRESH_TOKEN, and "
                "GMAIL_API_FROM_EMAIL."
            )
        _send_email_gmail_api(to_email, subject, body, html_body=html_body)
        return

    if RESEND_API_KEY:
        _send_email_resend(to_email, subject, body, html_body=html_body)
        return

    missing = []
    if not SMTP_USERNAME:
        missing.append("SMTP_USERNAME")
    if not SMTP_PASSWORD:
        missing.append("SMTP_PASSWORD")
    if not SMTP_FROM_EMAIL:
        missing.append("SMTP_FROM_EMAIL")
    if missing:
        raise RuntimeError("Missing SMTP settings: " + ", ".join(missing))

    msg = _build_email_message(_format_from(), to_email, subject, body, html_body)

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
    except Exception as exc:
        logger.exception("Error sending email to %s", to_email)
        _print_email_error("smtp", to_email, exc)
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


def _format_fecha(value: object) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%Y-%m-%d")
    return str(value)


def _format_hora(value: object) -> str:
    if hasattr(value, "strftime"):
        return value.strftime("%H:%M")
    return str(value)


def _safe_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def send_cita_estado_email(
    to_email: str,
    paciente_nombre: str,
    medico_nombre: str,
    especialidad: str,
    fecha: object,
    hora: object,
    estado: object,
) -> None:
    estado_value = getattr(estado, "value", estado)
    estado_value = str(estado_value)
    if estado_value not in ("confirmada", "rechazada"):
        return

    fecha_text = _format_fecha(fecha)
    hora_text = _format_hora(hora)
    especialidad_text = f" ({especialidad})" if especialidad else ""

    if estado_value == "confirmada":
        subject = "Cita confirmada - CareFlow"
        estado_text = "confirmada"
        detalle_text = "Tu cita ha sido confirmada."
    else:
        subject = "Cita rechazada - CareFlow"
        estado_text = "rechazada"
        detalle_text = "Tu cita ha sido rechazada."

    body = (
        f"Hola {paciente_nombre},\n\n"
        f"Tu cita con el medico {medico_nombre}{especialidad_text} para el "
        f"{fecha_text} a las {hora_text} ha sido {estado_text}.\n\n"
        f"{detalle_text}\n\n"
        "Si necesitas reprogramar, solicita una nueva cita.\n\n"
        "CareFlow"
    )

    html_body = f"""\
<!doctype html>
<html>
    <head>
        <meta charset=\"utf-8\">
        <title>Estado de cita</title>
    </head>
    <body style=\"margin:0;padding:0;background-color:#f5f6f8;\">
        <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"background-color:#f5f6f8;padding:24px 0;\">
            <tr>
                <td align=\"center\">
                    <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"background-color:#ffffff;border:1px solid #e6e8eb;border-radius:8px;overflow:hidden;font-family:Arial, sans-serif;color:#111827;\">
                        <tr>
                            <td style=\"padding:24px 28px;background-color:#0f172a;color:#ffffff;\">
                                <div style=\"font-size:18px;font-weight:700;\">CareFlow</div>
                                <div style=\"font-size:13px;opacity:0.85;\">Estado de cita</div>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"padding:28px;\">
                                <p style=\"margin:0 0 12px;font-size:15px;line-height:1.5;\">Hola {paciente_nombre},</p>
                                <p style=\"margin:0 0 16px;font-size:15px;line-height:1.5;\">Tu cita con el medico <strong>{medico_nombre}</strong>{especialidad_text} para el <strong>{fecha_text}</strong> a las <strong>{hora_text}</strong> ha sido <strong>{estado_text}</strong>.</p>
                                <p style=\"margin:0;font-size:14px;line-height:1.5;color:#374151;\">{detalle_text}</p>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"padding:16px 28px;background-color:#f9fafb;font-size:12px;color:#6b7280;\">
                                Si necesitas reprogramar, solicita una nueva cita.
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


def send_receta_medica_email(
    to_email: str,
    paciente_nombre: str,
    medico_nombre: str,
    especialidad: str,
    medicamento_nombre: str,
    medicamento_descripcion: str,
    dosis: str,
    frecuencia: str,
    duracion: str,
    indicaciones: str,
    dosis_recomendada: str = "",
    contraindicaciones: str = "",
) -> None:
    especialidad_text = f" ({especialidad})" if especialidad else ""

    details = [
        ("Medicamento", _safe_text(medicamento_nombre)),
        ("Descripcion", _safe_text(medicamento_descripcion)),
        ("Dosis indicada", _safe_text(dosis)),
        ("Frecuencia", _safe_text(frecuencia)),
        ("Duracion", _safe_text(duracion)),
        ("Indicaciones", _safe_text(indicaciones)),
    ]

    optional_details = [
        ("Dosis recomendada", _safe_text(dosis_recomendada)),
        ("Contraindicaciones", _safe_text(contraindicaciones)),
    ]
    for label, value in optional_details:
        if value:
            details.append((label, value))

    text_details = "\n".join(
        f"{label}: {value}" for label, value in details if value
    )
    html_details = "\n".join(
        (
            "<tr>"
            f"<td style=\"padding:8px 12px;border:1px solid #e5e7eb;font-size:13px;color:#6b7280;width:180px;\">{label}</td>"
            f"<td style=\"padding:8px 12px;border:1px solid #e5e7eb;font-size:14px;color:#111827;\">{value}</td>"
            "</tr>"
        )
        for label, value in details
        if value
    )

    subject = "Receta medica - CareFlow"
    body = (
        f"Hola {paciente_nombre},\n\n"
        f"Se ha emitido una receta medica con el medico {medico_nombre}{especialidad_text}.\n\n"
        f"{text_details}\n\n"
        "Si tienes dudas, contacta al centro medico.\n\n"
        "CareFlow"
    )

    html_body = f"""\
<!doctype html>
<html>
    <head>
        <meta charset=\"utf-8\">
        <title>Receta medica</title>
    </head>
    <body style=\"margin:0;padding:0;background-color:#f5f6f8;\">
        <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"background-color:#f5f6f8;padding:24px 0;\">
            <tr>
                <td align=\"center\">
                    <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"background-color:#ffffff;border:1px solid #e6e8eb;border-radius:8px;overflow:hidden;font-family:Arial, sans-serif;color:#111827;\">
                        <tr>
                            <td style=\"padding:24px 28px;background-color:#0f172a;color:#ffffff;\">
                                <div style=\"font-size:18px;font-weight:700;\">CareFlow</div>
                                <div style=\"font-size:13px;opacity:0.85;\">Receta medica</div>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"padding:28px;\">
                                <p style=\"margin:0 0 12px;font-size:15px;line-height:1.5;\">Hola {paciente_nombre},</p>
                                <p style=\"margin:0 0 16px;font-size:15px;line-height:1.5;\">Se ha emitido una receta medica con el medico <strong>{medico_nombre}</strong>{especialidad_text}.</p>
                                <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"border-collapse:collapse;border:1px solid #e5e7eb;\">
                                    {html_details}
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style=\"padding:16px 28px;background-color:#f9fafb;font-size:12px;color:#6b7280;\">
                                Si tienes dudas, contacta al centro medico.
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


def _gmail_api_configured() -> bool:
    return all(
        [
            GMAIL_API_CLIENT_ID,
            GMAIL_API_CLIENT_SECRET,
            GMAIL_API_REFRESH_TOKEN,
            GMAIL_API_FROM_EMAIL,
        ]
    )


def _gmail_api_any_configured() -> bool:
    return any(
        [
            GMAIL_API_CLIENT_ID,
            GMAIL_API_CLIENT_SECRET,
            GMAIL_API_REFRESH_TOKEN,
            GMAIL_API_FROM_EMAIL,
        ]
    )


def _send_email_gmail_api(
    to_email: str, subject: str, body: str, html_body: Optional[str] = None
) -> None:
    missing = []
    if not GMAIL_API_CLIENT_ID:
        missing.append("GMAIL_API_CLIENT_ID")
    if not GMAIL_API_CLIENT_SECRET:
        missing.append("GMAIL_API_CLIENT_SECRET")
    if not GMAIL_API_REFRESH_TOKEN:
        missing.append("GMAIL_API_REFRESH_TOKEN")
    if not GMAIL_API_FROM_EMAIL:
        missing.append("GMAIL_API_FROM_EMAIL")
    if missing:
        raise RuntimeError("Missing Gmail API settings: " + ", ".join(missing))

    msg = _build_email_message(
        _format_gmail_from(), to_email, subject, body, html_body
    )
    raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    payload = {"raw": raw_message}
    access_token = _get_gmail_access_token()

    request = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=GMAIL_API_TIMEOUT) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        logger.error("Gmail API error: %s", error_body)
        _print_email_error("gmail_api", to_email, exc)
        raise
    except urllib.error.URLError as exc:
        logger.exception("Error sending email via Gmail API to %s", to_email)
        _print_email_error("gmail_api", to_email, exc)
        raise


def _send_email_resend(
    to_email: str, subject: str, body: str, html_body: Optional[str] = None
) -> None:
    missing = []
    if not RESEND_API_KEY:
        missing.append("RESEND_API_KEY")
    if not RESEND_FROM_EMAIL:
        missing.append("RESEND_FROM_EMAIL")
    if missing:
        raise RuntimeError("Missing Resend settings: " + ", ".join(missing))

    payload = {
        "from": _format_resend_from(),
        "to": [to_email],
        "subject": subject,
        "text": body,
    }
    if html_body:
        payload["html"] = html_body

    request = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=RESEND_TIMEOUT) as response:
            response.read()
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        logger.error("Resend API error: %s", error_body)
        _print_email_error("resend", to_email, exc)
        raise
    except urllib.error.URLError as exc:
        logger.exception("Error sending email via Resend to %s", to_email)
        _print_email_error("resend", to_email, exc)
        raise


def _format_resend_from() -> str:
    if RESEND_FROM_NAME:
        return f"{RESEND_FROM_NAME} <{RESEND_FROM_EMAIL}>"
    return RESEND_FROM_EMAIL


def _format_gmail_from() -> str:
    if GMAIL_API_FROM_NAME:
        return f"{GMAIL_API_FROM_NAME} <{GMAIL_API_FROM_EMAIL}>"
    return GMAIL_API_FROM_EMAIL


def _get_gmail_access_token() -> str:
    global _gmail_access_token
    global _gmail_access_token_expires_at

    now = time.time()
    if _gmail_access_token and now < _gmail_access_token_expires_at:
        return _gmail_access_token

    token_payload = {
        "client_id": GMAIL_API_CLIENT_ID,
        "client_secret": GMAIL_API_CLIENT_SECRET,
        "refresh_token": GMAIL_API_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }
    request = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode(token_payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=GMAIL_API_TIMEOUT) as response:
            token_body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        logger.error("Gmail token error: %s", error_body)
        _print_email_error("gmail_token", "access_token", exc)
        raise
    except urllib.error.URLError as exc:
        logger.exception("Error requesting Gmail access token")
        _print_email_error("gmail_token", "access_token", exc)
        raise

    token_data = json.loads(token_body)
    access_token = token_data.get("access_token")
    if not access_token:
        raise RuntimeError("Missing access_token in Gmail API response")

    expires_in = int(token_data.get("expires_in", 3600))
    _gmail_access_token = access_token
    _gmail_access_token_expires_at = now + max(expires_in - 60, 0)
    return access_token
