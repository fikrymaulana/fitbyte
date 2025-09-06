from __future__ import annotations
import re
import unicodedata

_ZERO_WIDTH = [
    "\u200b",  # ZERO WIDTH SPACE
    "\u200c",  # ZERO WIDTH NON-JOINER
    "\u200d",  # ZERO WIDTH JOINER
    "\ufeff",  # ZERO WIDTH NO-BREAK SPACE
]
_ZW_RE = re.compile("|".join(map(re.escape, _ZERO_WIDTH)))

_CTRL_RE = re.compile(r"[\x00-\x1F\x7F]")  # control chars


def sanitize_email_input(v: str) -> str:
    if v is None:
        raise ValueError("Email is required")
    if not isinstance(v, str):
        v = str(v)

    # normalize unicode, remove zero-width, strip spaces
    v = unicodedata.normalize("NFC", v)
    v = _ZW_RE.sub("", v).strip()

    if re.search(r"\s", v) or _CTRL_RE.search(v):
        raise ValueError("Email must not contain whitespace or control characters")

    if len(v) > 254:
        raise ValueError("Email must be at most 254 characters")

    return v
