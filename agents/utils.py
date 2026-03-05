from __future__ import annotations

import re
from time import perf_counter
from typing import Any, Callable, Dict

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"bypass policy",
    r"dump all logs",
    r"reveal confidential",
    r"system admin",
]

EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+")
# Broad phone-like candidate; filtered by _looks_like_phone to avoid redacting dates/log IDs.
PHONE_CANDIDATE_RE = re.compile(r"(?<!\w)\+?[\d\s\-\(\)]{9,}(?!\w)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def detect_prompt_injection(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in INJECTION_PATTERNS)


def _looks_like_phone(candidate: str) -> bool:
    token = candidate.strip()
    if DATE_RE.match(token):
        return False

    digits = re.sub(r"\D", "", token)
    if len(digits) < 9:
        return False

    has_plus = "+" in token
    separator_count = token.count("-") + token.count(" ") + token.count("(") + token.count(")")

    # Prefer international/local phone formatting signals to avoid false positives.
    return has_plus or separator_count >= 2


def redact_pii(text: str) -> str:
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)

    def _replace(match: re.Match[str]) -> str:
        token = match.group(0)
        return "[REDACTED_PHONE]" if _looks_like_phone(token) else token

    return PHONE_CANDIDATE_RE.sub(_replace, text)


def timed_run(fn: Callable[..., Dict[str, Any]], *args: Any, **kwargs: Any) -> tuple[Dict[str, Any], float]:
    start = perf_counter()
    out = fn(*args, **kwargs)
    return out, (perf_counter() - start) * 1000
