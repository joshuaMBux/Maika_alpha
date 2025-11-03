import json
import os
from datetime import datetime


def load_json(path: str, default: dict | list | None = None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else {}


def iso_now() -> str:
    return datetime.utcnow().isoformat()


def get_content_path(*parts: str) -> str:
    base = os.path.join("data", "content")
    return os.path.join(base, *parts)


