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

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME or "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "CareFlow")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes", "on")
SMTP_TIMEOUT = int(os.getenv("SMTP_TIMEOUT", "20"))

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))
