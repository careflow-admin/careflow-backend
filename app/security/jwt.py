import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Tuple

from app.config.settings import JWT_ALGORITHM, JWT_EXPIRES_MINUTES, JWT_SECRET


def create_access_token(data: Dict[str, Any], expires_minutes: int = None) -> str:
    if not JWT_SECRET:
        raise ValueError("JWT secret no configurado.")

    payload = dict(data)
    expires = JWT_EXPIRES_MINUTES if expires_minutes is None else expires_minutes
    payload["exp"] = int(time.time()) + int(expires) * 60
    return _encode_jwt(payload)


def decode_access_token(token: str) -> Dict[str, Any]:
    if not JWT_SECRET:
        raise ValueError("JWT secret no configurado.")

    header_b64, payload_b64, signature_b64 = _split_token(token)
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = _b64url_decode(signature_b64)
    expected = hmac.new(
        JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()

    if not hmac.compare_digest(signature, expected):
        raise ValueError("Token invalido.")

    header = _json_loads(_b64url_decode(header_b64))
    if header.get("alg") != JWT_ALGORITHM:
        raise ValueError("Token invalido.")

    payload = _json_loads(_b64url_decode(payload_b64))
    exp = payload.get("exp")
    if exp is not None and time.time() > float(exp):
        raise ValueError("Token expirado.")

    return payload


def _encode_jwt(payload: Dict[str, Any]) -> str:
    if JWT_ALGORITHM != "HS256":
        raise ValueError("Algoritmo JWT no soportado.")

    header = {"alg": JWT_ALGORITHM, "typ": "JWT"}
    header_b64 = _b64url_encode(_json_dumps(header))
    payload_b64 = _b64url_encode(_json_dumps(payload))
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(
        JWT_SECRET.encode("utf-8"), signing_input, hashlib.sha256
    ).digest()
    signature_b64 = _b64url_encode(signature)
    return f"{header_b64}.{payload_b64}.{signature_b64}"


def _split_token(token: str) -> Tuple[str, str, str]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token invalido.")
    return parts[0], parts[1], parts[2]


def _json_dumps(data: Dict[str, Any]) -> bytes:
    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")


def _json_loads(data: bytes) -> Dict[str, Any]:
    return json.loads(data.decode("utf-8"))


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)
