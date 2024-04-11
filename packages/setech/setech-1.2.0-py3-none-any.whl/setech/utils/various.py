import json
import logging
from typing import Any
from uuid import uuid4

from .parse import SetechJSONEncoder

__all__ = ["get_logger", "get_nonce", "shortify_log_dict", "shorten_value"]


def get_logger(name: str = "service") -> logging.Logger:
    return logging.getLogger(name)


def shorten_value(value: Any) -> Any:
    """Recursively shorten long string values and return a shortened version copy object.

    :param value: Object in which to recursively search for strings to shorten
    :return: Shortened version of the value
    """
    if isinstance(value, str):
        return f"{value[:30]}...{value[-30:]}" if isinstance(value, str) and len(value) > 64 else value
    if isinstance(value, list):
        return [shorten_value(v) for v in value]
    if isinstance(value, tuple):
        return tuple(shorten_value(v) for v in value)
    if isinstance(value, dict):
        return {k: shorten_value(v) for k, v in value.items()}
    return value


def shortify_log_dict(dct: Any) -> dict[str, Any]:
    """Shorten long values and normalize (to json compatible format) dictionary values

    :param dct: Object to convert into json log favourable format
    :return: shortened and normalized dictionary
    """
    return shorten_value(json.loads(json.dumps(dct, cls=SetechJSONEncoder)))


def get_nonce() -> str:
    """Generate random 12 hexadecimal string

    :return: 12 hexadecimal char long string
    """
    return uuid4().hex[:12]
