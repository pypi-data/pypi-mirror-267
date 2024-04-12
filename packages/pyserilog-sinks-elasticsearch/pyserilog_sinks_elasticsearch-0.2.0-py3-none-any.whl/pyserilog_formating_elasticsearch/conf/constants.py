import decimal
import re
from typing import Pattern


def _starmatch_to_regex(pattern: str) -> Pattern:
    """
    This is a duplicate of starmatch_to_regex() in utils/__init__.py

    Duplication to avoid circular imports
    """
    options = re.DOTALL
    # check if we are case-sensitive
    if pattern.startswith("(?-i)"):
        pattern = pattern[5:]
    else:
        options |= re.IGNORECASE
    i, n = 0, len(pattern)
    res = []
    while i < n:
        c = pattern[i]
        i = i + 1
        if c == "*":
            res.append(".*")
        else:
            res.append(re.escape(c))
    return re.compile(r"(?:%s)\Z" % "".join(res), options)


KEYWORD_MAX_LENGTH = 1024
LONG_FIELD_MAX_LENGTH = 10000
LABEL_RE = re.compile('[.*"]')
LABEL_TYPES = (bool, int, float, decimal.Decimal)


BASE_SANITIZE_FIELD_NAMES_UNPROCESSED = [
    "password",
    "passwd",
    "pwd",
    "secret",
    "*key",
    "*token*",
    "*session*",
    "*credit*",
    "*card*",
    "*auth*",
    "*principal*",
    "set-cookie",
]

BASE_SANITIZE_FIELD_NAMES = [_starmatch_to_regex(x) for x in BASE_SANITIZE_FIELD_NAMES_UNPROCESSED]


ERROR = "error"
MASK = "[REDACTED]"
SPAN = "span"
TRANSACTION = "transaction"