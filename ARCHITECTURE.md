# Architecture

## Goal

A satirical WordPress portal where one sentence of an idea becomes a professionally formatted **draft**. A person reads it. A person clicks Publish.

## Components

```
                    ┌───────────────────────────┐
  idea / email      │  middleware (Python)     │
  later Telegram ───│  pipeline + validator    │───│ WordPress REST
                    │  editorial SQLite        │    status = draft
                    │  local LLM (Gemma)       │
                    └───────────────────────────┘
                                 │
                                 ▼
                    ┌───────────────────────────┐
                    │  plugin satira-srbija    │
                    │  labels, meta, schema    │
                    │  disclaimer pages        │
                    │  admin desk              │
                    └───────────────────────────┘
```

No separate public frontend framework. WordPress renders the site. A block theme or a thin classic theme is enough. The plugin injects the satire contract regardless of theme.

## Why not “AI inside WordPress only”

A PHP-only path is possible later (Phase 2 plugin worker). MVP keeps generation in a small Python process because:

- JSON schema validation is stricter
- local model runners speak HTTP already
- embeddings for editorial memory are ordinary Python
- the WordPress process never holds model weights
- blast radius stays small: compromise of the model box is not shell on WordPress

The plugin still owns presentation, meta, REST field registration, and the human desk.

## Data stores

| Store | What |
| --- | --- |
| WordPress MySQL | posts, terms, media, users |
| `data/editorial.sqlite` | generation versions, titles, entities, summaries, embeddings |
| `.env` | credentials |

SQLite is enough until the archive is large. Phase 2 can move embeddings to a dedicated vector table. Do not introduce a second product database in MVP.

## WordPress REST writes

Authenticated with Application Passwords over HTTPS.

Created objects:

- tags (get-or-create by name)
- category (map from the closed enum)
- post with `status=draft`
- post meta via registered REST fields
- featured media only when a real file exists (MVP stores the image *prompt*, not a generated bitmap)

Default author comes from `WP_AUTHOR_ID`.

## Validation gate

The model output is not trusted. `satira.validator` checks:

- JSON against `schemas/article.schema.json`
- HTML allowlist
- no inline style / script / iframe
- heading hygiene
- paragraph length
- required satire label
- known category
- slug shape
- excerpt and ALT present
- footer disclaimer present in HTML

Fail → correction prompt with the error list → second attempt → still fail → stop. Nothing reaches WordPress.

## Editorial memory

Before generation, the pipeline embeds the idea and retrieves the nearest prior titles and summaries. Those rows go into the prompt as “do not repeat”. After a successful draft, a new row is stored even if the WordPress write later fails, so retries do not loop the same joke.

## Inlets

| Inlet | MVP | Phase 2 |
| --- | --- | --- |
| CLI one-liner | yes | yes |
| HTTP `POST /v1/draft` | yes, token, localhost | same + reverse proxy |
| Plugin admin form | yes (stores idea, calls middleware if configured) | richer desk |
| Email IMAP | parser present, disabled by default | cron worker |
| Telegram / Discord | specified, not shipped | bot → same pipeline |

Every inlet produces the same JSON contract.

## Trust boundary

```
public web  →  WordPress (theme + plugin)
editor desk →  WordPress admin + optional localhost middleware
model       →  only the middleware process
secrets     →  .env, never the prompt, never the logs
```

The model cannot call WordPress directly. The middleware is the only writer, and it can only create drafts.
