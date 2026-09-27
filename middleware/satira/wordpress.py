from __future__ import annotations

from typing import Any

import httpx

from satira.config import settings

CATEGORY_SLUGS = {
    "Politika": "politika",
    "Tehnologija": "tehnologija",
    "AI": "ai",
    "Internet": "internet",
    "Društvo": "drustvo",
    "Biznis": "biznis",
    "Kultura": "kultura",
    "Sport": "sport",
    "Svet": "svet",
    "Srbija": "srbija",
    "Apsurd dana": "apsurd-dana",
}


class WordPressError(RuntimeError):
    pass


def _client() -> httpx.Client:
    if not settings.wp_app_password:
        raise WordPressError("WP_APP_PASSWORD missing")
    if settings.wp_default_status != "draft":
        raise WordPressError("refusing to run unless WP_DEFAULT_STATUS=draft")
    auth = (settings.wp_username, settings.wp_app_password)
    return httpx.Client(
        base_url=settings.wp_base_url.rstrip("/") + "/wp-json/wp/v2",
        auth=auth,
        timeout=settings.wp_timeout,
        headers={"User-Agent": "satira-srbija-middleware/0.1"},
    )


def create_draft(article: dict) -> dict[str, Any]:
    with _client() as client:
        category_id = _category_id(client, article["category"])
        tag_ids = [_tag_id(client, tag) for tag in article.get("tags") or []]
        body = {
            "title": article["title"],
            "slug": article["slug"],
            "status": "draft",
            "author": settings.wp_author_id,
            "excerpt": article["excerpt"],
            "content": article["content_html"],
            "categories": [category_id],
            "tags": tag_ids,
            "satira_label": article["satire_label"],
            "satira_seo_title": article["seo_title"],
            "satira_meta_description": article["meta_description"],
            "satira_social_title": article["social_title"],
            "satira_social_description": article["social_description"],
            "satira_image_prompt": article["featured_image_prompt"],
            "satira_alt_text": article["alt_text"],
            "satira_inspiration_url": article.get("inspiration_url") or "",
            "satira_inspiration_note": article.get("inspiration_note") or "",
        }
        response = client.post("/posts", json=body)
        if response.status_code >= 400:
            raise WordPressError(f"POST /posts {response.status_code}: {response.text[:400]}")
        data = response.json()
        return {
            "id": data.get("id"),
            "link": data.get("link"),
            "edit": _edit_link(data.get("id")),
            "status": data.get("status"),
        }


def _category_id(client: httpx.Client, name: str) -> int:
    slug = CATEGORY_SLUGS[name]
    found = client.get("/categories", params={"slug": slug})
    found.raise_for_status()
    items = found.json()
    if items:
        return int(items[0]["id"])
    created = client.post("/categories", json={"name": name, "slug": slug})
    if created.status_code >= 400:
        raise WordPressError(f"category {name}: {created.text[:200]}")
    return int(created.json()["id"])


def _tag_id(client: httpx.Client, name: str) -> int:
    found = client.get("/tags", params={"search": name})
    found.raise_for_status()
    for item in found.json():
        if item.get("name", "").lower() == name.lower():
            return int(item["id"])
    created = client.post("/tags", json={"name": name})
    if created.status_code >= 400:
        raise WordPressError(f"tag {name}: {created.text[:200]}")
    return int(created.json()["id"])


def _edit_link(post_id: int | None) -> str:
    if not post_id:
        return ""
    return settings.wp_base_url.rstrip("/") + f"/wp-admin/post.php?post={post_id}&action=edit"
