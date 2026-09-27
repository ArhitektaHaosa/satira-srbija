from __future__ import annotations

import hashlib
import json
import math
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import httpx

from satira.config import settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    topic TEXT,
    entities TEXT,
    category TEXT,
    summary TEXT,
    slug TEXT,
    idea_hash TEXT,
    embedding TEXT,
    wp_post_id INTEGER,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS versions (
    id INTEGER PRIMARY KEY,
    article_row INTEGER,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def _connect() -> sqlite3.Connection:
    path = Path(settings.memory_db)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def idea_hash(idea: str) -> str:
    return hashlib.sha256(idea.strip().encode("utf-8")).hexdigest()[:16]


def nearby(idea: str, limit: int = 5) -> list[dict]:
    vec = embed(idea)
    with _connect() as conn:
        rows = conn.execute(
            "SELECT title, topic, category, summary, slug, embedding FROM articles ORDER BY id DESC LIMIT 80"
        ).fetchall()
    scored: list[tuple[float, dict]] = []
    for row in rows:
        item = dict(row)
        stored = []
        if item.get("embedding"):
            try:
                stored = json.loads(item["embedding"])
            except json.JSONDecodeError:
                stored = []
        item.pop("embedding", None)
        score = cosine(vec, stored) if stored and vec else lexical(idea, item)
        scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [item for score, item in scored[:limit] if score >= 0.15]


def remember(payload: dict, idea: str, wp_post_id: int | None) -> None:
    now = datetime.now(timezone.utc).isoformat()
    vec = embed(payload.get("title", "") + " " + payload.get("excerpt", ""))
    with _connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO articles(title, topic, entities, category, summary, slug, idea_hash, embedding, wp_post_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.get("title"),
                payload.get("layers", {}).get("satire", "")[:240],
                json.dumps(payload.get("tags") or [], ensure_ascii=False),
                payload.get("category"),
                payload.get("excerpt"),
                payload.get("slug"),
                idea_hash(idea),
                json.dumps(vec) if vec else None,
                wp_post_id,
                now,
            ),
        )
        conn.execute(
            "INSERT INTO versions(article_row, payload, created_at) VALUES (?, ?, ?)",
            (cur.lastrowid, json.dumps(payload, ensure_ascii=False), now),
        )


def embed(text: str) -> list[float]:
    url = settings.ollama_host.rstrip("/") + "/api/embeddings"
    try:
        response = httpx.post(
            url,
            json={"model": settings.embed_model, "prompt": text[:4000]},
            timeout=20.0,
        )
        if response.status_code >= 400:
            return []
        data = response.json()
        return list(data.get("embedding") or [])
    except httpx.HTTPError:
        return []


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def lexical(idea: str, item: dict) -> float:
    tokens = set(re.findall(r"\w+", idea.lower()))
    other = set(re.findall(r"\w+", " ".join(str(v or "") for v in item.values()).lower()))
    if not tokens or not other:
        return 0.0
    return len(tokens & other) / len(tokens | other)
