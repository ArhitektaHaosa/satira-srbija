from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schemas" / "article.schema.json"
ARTICLE_SCHEMA = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
VALIDATOR = Draft202012Validator(ARTICLE_SCHEMA)

CATEGORIES = ARTICLE_SCHEMA["properties"]["category"]["enum"]
SATIRE_LABEL = "Satira / Parodija"
DISCLAIMER_SNIPPET = "Ovaj tekst je satira/parodija"


def schema_errors(payload: dict) -> list[str]:
    return [
        f"{'.'.join(str(p) for p in err.path) or '$'}: {err.message}"
        for err in VALIDATOR.iter_errors(payload)
    ]
