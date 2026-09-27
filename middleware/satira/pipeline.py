from __future__ import annotations

import json
import logging
from pathlib import Path

from satira import llm, memory
from satira.validator import validate_article
from satira.wordpress import WordPressError, create_draft

LOG = logging.getLogger("satira")
MAX_CORRECTIONS = 1


def run(idea: str, push: bool = True) -> dict:
    idea = idea.strip()
    if len(idea) < 8:
        raise ValueError("idea too short")
    nearby = memory.nearby(idea)
    system = llm.load_prompt("system-satiricar.md")
    user = _writer_user(idea, nearby)
    raw = llm.complete(system, user)
    article = llm.parse_json_object(raw)
    errors = validate_article(article)
    if errors:
        article = _correct(article, errors)
        errors = validate_article(article)
    if errors:
        LOG.warning("validation failed after correction: %s", errors)
        return {
            "ok": False,
            "errors": errors,
            "article": article,
            "wordpress": None,
        }
    wp = None
    if push:
        try:
            wp = create_draft(article)
        except WordPressError as exc:
            LOG.error("wordpress draft failed: %s", exc)
            memory.remember(article, idea, None)
            return {
                "ok": False,
                "errors": [str(exc)],
                "article": article,
                "wordpress": None,
            }
    memory.remember(article, idea, (wp or {}).get("id"))
    return {"ok": True, "errors": [], "article": article, "wordpress": wp}


def _correct(previous: dict, errors: list[str]) -> dict:
    template = llm.load_prompt("correction-pass.md")
    user = template.replace("{{ERRORS}}", "\n".join(f"- {e}" for e in errors)).replace(
        "{{PREVIOUS}}", json.dumps(previous, ensure_ascii=False, indent=2)
    )
    raw = llm.complete(llm.load_prompt("system-satiricar.md"), user)
    return llm.parse_json_object(raw)


def _writer_user(idea: str, nearby: list[dict]) -> str:
    lines = ["OPERATOR IDEA:", idea, ""]
    if nearby:
        lines.append("NEARBY_ARTICLES (do not repeat title rhythm or punchline):")
        for item in nearby:
            lines.append(f"- {item.get('title')} | {item.get('category')} | {item.get('summary')}")
        lines.append("")
    lines.append("Write the article JSON now.")
    return "\n".join(lines)


def setup_logging() -> None:
    from satira.config import settings

    Path(settings.log_file).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(settings.log_file),
            logging.StreamHandler(),
        ],
    )
