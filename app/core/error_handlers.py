from typing import Any, Dict, Optional
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder


def _safe_serialize_ctx(ctx: Any) -> Optional[Dict[str, Any]]:
    if ctx is None:
        return None
    if isinstance(ctx, dict):
        # make sure all values inside ctx are primitives/strings
        return {
            k: (v if isinstance(v, (str, int, float, bool, type(None))) else str(v))
            for k, v in ctx.items()
        }
    # fallback: serialize as string
    return {"detail": str(ctx)}


def _safe_input_for_field(field: Optional[str], input_val: Any) -> Any:
    if input_val is None:
        return None
    if field == "password":
        return None
    if isinstance(input_val, (str, int, float, bool, type(None))):
        return input_val
    if isinstance(input_val, (bytes, bytearray)):
        try:
            return input_val.decode("utf-8", errors="ignore")
        except Exception:
            return str(input_val)
    # fallback to string representation
    try:
        return str(input_val)
    except Exception:
        return None


def _field_from_loc(loc: list) -> Optional[str]:
    for p in loc:
        if p not in {"body", "query", "path"}:
            return str(p)
    return None


def _normalize_error(e: dict) -> dict:
    loc = e.get("loc", [])
    raw_type = e.get("type", "")
    raw_msg = e.get("msg", "")
    input_val = e.get("input", None)
    ctx = e.get("ctx")

    field = _field_from_loc(loc) or "body"

    typ = raw_type
    msg = raw_msg
    new_ctx = _safe_serialize_ctx(ctx)
    safe_input = _safe_input_for_field(field, input_val)

    if field == "email":
        typ = "invalid_email"
        msg = "Email must be a valid email address (max 254 characters)."
        new_ctx = {"max_length": 254}
    elif field == "password":
        if (
            raw_type in {"string_too_short", "string_too_long"}
            or "length" in raw_msg.lower()
        ):
            typ = "password_length"
            msg = "Password length must be 8–32 characters."
            new_ctx = {"min_length": 8, "max_length": 32}
        elif "lowercase" in raw_msg.lower():
            typ = "password_lowercase"
            msg = "Password must contain at least one lowercase letter."
        elif "uppercase" in raw_msg.lower():
            typ = "password_uppercase"
            msg = "Password must contain at least one uppercase letter."
        elif "digit" in raw_msg.lower():
            typ = "password_digit"
            msg = "Password must contain at least one digit."
        elif "symbol" in raw_msg.lower():
            typ = "password_symbol"
            msg = "Password must contain at least one symbol (e.g., !@#$)."
        elif raw_type.startswith("value_error"):
            typ = "password_invalid"
            msg = "Invalid password."
    else:
        if raw_type.startswith("value_error"):
            typ = "invalid_input"
            msg = raw_msg or "Invalid input."

    return {
        "type": typ,
        "loc": loc,
        "msg": msg,
        "input": safe_input,
        "ctx": new_ctx,
    }


async def request_validation_exception_handler(_: Request, exc: RequestValidationError):
    normalized = [_normalize_error(e) for e in exc.errors()]
    body = {"detail": normalized}
    # ensure everything JSON serializable
    safe_body = jsonable_encoder(body)
    return JSONResponse(status_code=400, content=safe_body)
