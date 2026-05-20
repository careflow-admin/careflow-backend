import os
from pathlib import Path


def _load_env_file() -> None:
	env_path = Path(__file__).resolve().parent.parent / ".env"
	if not env_path.exists():
		return

	try:
		from dotenv import load_dotenv
	except ImportError:
		load_dotenv = None

	if load_dotenv:
		load_dotenv(env_path)
		return

	# Basic fallback parser for KEY=VALUE lines.
	for line in env_path.read_text(encoding="utf-8").splitlines():
		line = line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue
		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip().strip("\"'")
		os.environ.setdefault(key, value)


_load_env_file()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./careflow.db")


def _int_env(name: str, default: int) -> int:
	raw = os.getenv(name)
	if not raw:
		return default
	try:
		return int(raw)
	except ValueError:
		return default

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = _int_env("SMTP_PORT", 587)
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME or "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "CareFlow")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes", "on")
SMTP_USE_SSL = os.getenv("SMTP_USE_SSL", "false").lower() in ("1", "true", "yes", "on")
SMTP_TIMEOUT = _int_env("SMTP_TIMEOUT", 20)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_FROM_EMAIL = os.getenv("RESEND_FROM_EMAIL", "")
RESEND_FROM_NAME = os.getenv("RESEND_FROM_NAME", "CareFlow")
RESEND_TIMEOUT = _int_env("RESEND_TIMEOUT", 20)

GMAIL_API_CLIENT_ID = os.getenv("GMAIL_API_CLIENT_ID")
GMAIL_API_CLIENT_SECRET = os.getenv("GMAIL_API_CLIENT_SECRET")
GMAIL_API_REFRESH_TOKEN = os.getenv("GMAIL_API_REFRESH_TOKEN")
GMAIL_API_FROM_EMAIL = os.getenv("GMAIL_API_FROM_EMAIL", "")
GMAIL_API_FROM_NAME = os.getenv("GMAIL_API_FROM_NAME", "CareFlow")
GMAIL_API_TIMEOUT = _int_env("GMAIL_API_TIMEOUT", 20)

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES = _int_env("JWT_EXPIRES_MINUTES", 60)
