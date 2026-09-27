from __future__ import annotations

import re
from collections import Counter

from bs4 import BeautifulSoup, NavigableString

from satira.schema import DISCLAIMER_SNIPPET, SATIRE_LABEL, schema_errors

ALLOWED = {"h2", "h3", "p", "blockquote", "strong", "em", "ul", "ol", "li", "figure", "figcaption", "footer"}
FORBIDDEN_ATTR_PREFIX = ("on",)
MAX_PARAGRAPH = 900
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_article(payload: dict) -> list[str]:
    errors = schema_errors(payload)
    errors.extend(_html_errors(payload.get("content_html", "")))
    title = (payload.get("title") or "").strip()
    if title and title.lower() == (payload.get("slug") or "").replace("-", " "):
        errors.append("title: looks identical to slug; write a headline")
    if payload.get("satire_label") != SATIRE_LABEL:
        errors.append("satire_label: must be exactly 'Satira / Parodija'")
    slug = payload.get("slug") or ""
    if slug and not SLUG_RE.match(slug):
        errors.append("slug: ASCII hyphens only")
    excerpt = payload.get("excerpt") or ""
    if excerpt and "satir" not in excerpt.lower() and "parod" not in excerpt.lower():
        errors.append("excerpt: mention satira or parodija so cards stay honest")
    seo = (payload.get("seo_title") or "") + " " + (payload.get("meta_description") or "")
    if "satir" not in seo.lower() and "parod" not in seo.lower():
        errors.append("seo: title or description must keep the genre word")
    return errors


def _html_errors(html: str) -> list[str]:
    errors: list[str] = []
    if not html or not html.strip():
        return ["content_html: empty"]
    soup = BeautifulSoup(html, "lxml")
    body = soup.body or soup
    for tag in body.find_all(True):
        name = tag.name.lower()
        if name in {"html", "body"}:
            continue
        if name not in ALLOWED:
            errors.append(f"content_html: tag <{name}> not allowed")
        if tag.has_attr("style") or tag.has_attr("class") or tag.has_attr("id"):
            errors.append(f"content_html: <{name}> has presentational attributes")
        for attr in list(tag.attrs):
            if attr.lower().startswith(FORBIDDEN_ATTR_PREFIX):
                errors.append(f"content_html: event handler {attr}")
    text = body.get_text(" ", strip=True)
    if DISCLAIMER_SNIPPET.lower() not in text.lower():
        errors.append("content_html: missing footer disclaimer")
    headings = [t.get_text(" ", strip=True) for t in body.find_all(["h2", "h3"])]
    if any(not h for h in headings):
        errors.append("content_html: empty heading")
    dupes = [h for h, n in Counter(headings).items() if n > 1 and h]
    if dupes:
        errors.append(f"content_html: duplicated heading {dupes[0]!r}")
    if len(headings) < 2:
        errors.append("content_html: need at least two h2/h3 breaks")
    for p in body.find_all("p"):
        chunk = p.get_text(" ", strip=True)
        if len(chunk) > MAX_PARAGRAPH:
            errors.append("content_html: paragraph over 900 characters")
            break
    if not body.find("blockquote"):
        errors.append("content_html: missing parody blockquote")
    scripts = body.find_all(["script", "iframe", "form", "style"])
    if scripts:
        errors.append("content_html: dangerous tag present")
    if _looks_unbalanced(html):
        errors.append("content_html: unbalanced tags")
    _ = NavigableString
    return errors


def _looks_unbalanced(html: str) -> bool:
    soup = BeautifulSoup(html, "lxml")
    return bool(BeautifulSoup(str(soup), "lxml").find_all("parsererror"))
