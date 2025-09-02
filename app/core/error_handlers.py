from __future__ import annotations

from typing import Any, Dict, Optional, List
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

ALLOWED_SYMBOLS_STR = "!@#$"


def _safe_serialize_ctx(ctx: Any) -> Optional[Dict[str, Any]]:
    if ctx is None:
        return None
    if isinstance(ctx, dict):
        return {
            k: (v if isinstance(v, (str, int, float, bool, type(None))) else str(v))
            for k, v in ctx.items()
        }
    return {"detail": str(ctx)}


def _safe_input_for_field(field: Optional[str], input_val: Any) -> Any:
    if field == "password":
        return input_val
    if input_val is None:
        return None
    if isinstance(input_val, (str, int, float, bool, type(None))):
        return input_val
    if isinstance(input_val, (bytes, bytearray)):
        try:
            return input_val.decode("utf-8", errors="ignore")
        except Exception:
            return str(input_val)
    try:
        return str(input_val)
    except Exception:
        return None


def _field_from_loc(loc: List[Any]) -> Optional[str]:
    for p in loc:
        if p not in {"body", "query", "path"}:
            return str(p)
    return None


def _contains(text: str, *needles: str) -> bool:
    t = text.lower()
    return any(n.lower() in t for n in needles)


def _map_email_error(
    raw_type: str, raw_msg: str, ctx: Optional[Dict[str, Any]]
) -> tuple[str, str, Optional[Dict[str, Any]]]:
    # default
    typ = "invalid_email"
    msg = raw_msg or "Email must be a valid email address."

    if _contains(raw_msg, "control"):
        typ = "email_control_chars"
    elif _contains(raw_msg, "whitespace"):
        typ = "email_whitespace"
    elif _contains(raw_msg, "special-use", "reserved name", "reserved"):
        typ = "email_domain_reserved"
    elif raw_type in {"string_too_long"} or _contains(raw_msg, "at most", "too long"):
        typ = "email_too_long"
    # else biarkan invalid_email

    new_ctx = _safe_serialize_ctx(ctx) or {}
    if "max_length" not in new_ctx:
        new_ctx["max_length"] = 254
    return typ, msg, new_ctx


def _map_password_error(
    raw_type: str, raw_msg: str, ctx: Optional[Dict[str, Any]]
) -> tuple[str, str, Optional[Dict[str, Any]]]:
    # default
    typ = "password_invalid"
    msg = raw_msg or "Invalid password."
    new_ctx = _safe_serialize_ctx(ctx) or {}

    if raw_type in {"string_too_short", "string_too_long"} or _contains(
        raw_msg, "length", "at least", "at most", "characters"
    ):
        typ = "password_length"
        new_ctx.setdefault("min_length", 8)
        new_ctx.setdefault("max_length", 32)
    elif _contains(raw_msg, "whitespace"):
        typ = "password_whitespace"
    elif _contains(raw_msg, "control"):
        typ = "password_control_chars"
    elif _contains(raw_msg, "lowercase"):
        typ = "password_lowercase"
    elif _contains(raw_msg, "uppercase"):
        typ = "password_uppercase"
    elif _contains(raw_msg, "digit"):
        typ = "password_digit"
    elif _contains(raw_msg, "symbol"):
        typ = "password_symbol"
        new_ctx.setdefault("allowed_symbols", ALLOWED_SYMBOLS_STR)

    return typ, msg, new_ctx or None


def _normalize_error(e: dict) -> dict:
    loc = e.get("loc", [])
    raw_type = e.get("type", "") or ""
    raw_msg = e.get("msg", "") or ""
    input_val = e.get("input", None)
    ctx = e.get("ctx")

    field = _field_from_loc(loc) or "body"

    # default passthrough
    typ = raw_type if raw_type else "invalid_input"
    msg = raw_msg if raw_msg else "Invalid input."
    new_ctx = _safe_serialize_ctx(ctx)
    safe_input = _safe_input_for_field(field, input_val)

    if field == "email":
        typ, msg, new_ctx = _map_email_error(raw_type, raw_msg, ctx)
    elif field == "password":
        typ, msg, new_ctx = _map_password_error(raw_type, raw_msg, ctx)
    else:
        if raw_type.startswith("value_error"):
            typ = "invalid_input"

    return {
        "type": typ,
        "loc": loc,
        "msg": msg,
        "input": safe_input,
        "ctx": new_ctx,
    }


async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
    normalized = [_normalize_error(e) for e in exc.errors()]
    safe_body = jsonable_encoder({"detail": normalized})
    return JSONResponse(status_code=400, content=safe_body)
