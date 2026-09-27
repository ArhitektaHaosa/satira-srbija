from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

from satira.config import settings

PROMPTS = Path(__file__).resolve().parents[2] / "prompts"


class LLMError(RuntimeError):
    pass


def complete(system: str, user: str) -> str:
    if settings.llm_provider != "ollama":
        raise LLMError(f"unsupported provider {settings.llm_provider}")
    payload = {
        "model": settings.ollama_model,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": settings.llm_temperature,
            "num_predict": settings.llm_max_tokens,
        },
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    url = settings.ollama_host.rstrip("/") + "/api/chat"
    try:
        response = httpx.post(url, json=payload, timeout=settings.llm_timeout)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise LLMError(f"ollama unreachable: {exc}") from exc
    data = response.json()
    text = (data.get("message") or {}).get("content") or ""
    if not text.strip():
        raise LLMError("empty model response")
    return text


def parse_json_object(raw: str) -> dict:
    text = raw.strip()
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text).strip()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise LLMError("model did not return JSON")
        obj = json.loads(text[start : end + 1])
    if not isinstance(obj, dict):
        raise LLMError("JSON root is not an object")
    return obj


def load_prompt(name: str) -> str:
    return (PROMPTS / name).read_text(encoding="utf-8")
