from __future__ import annotations

import secrets
from collections import deque
from time import time

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from satira.config import settings
from satira.pipeline import run, setup_logging

setup_logging()
app = FastAPI(title="Satira Srbija", version="0.1.0", docs_url=None, redoc_url=None)
HITS: deque[float] = deque()


class IdeaIn(BaseModel):
    idea: str = Field(min_length=8, max_length=4000)
    push: bool = True


def _auth(authorization: str | None = Header(default=None)) -> None:
    if not settings.api_token:
        raise HTTPException(503, "API_TOKEN is not set")
    expected = "Bearer " + settings.api_token
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(401, "unauthorized")
    now = time()
    while HITS and now - HITS[0] > 60:
        HITS.popleft()
    if len(HITS) >= settings.api_rate_limit:
        raise HTTPException(429, "rate limit")
    HITS.append(now)


@app.post("/v1/draft")
def create_draft(payload: IdeaIn, _: None = Depends(_auth)) -> dict:
    try:
        result = run(payload.idea, push=payload.push)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    return result


def main() -> None:
    import uvicorn

    uvicorn.run(
        "satira.app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False,
    )


if __name__ == "__main__":
    main()
