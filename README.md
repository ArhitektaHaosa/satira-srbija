# Satira Srbija

WordPress editorial pipeline for **clearly labeled** satire and parody.

AI writes **drafts**. A human publishes. Never the other way around.

Site content must be impossible to reasonably confuse with a real news report.

Visible label on every surface: **SATIRA / PARODIJA**

Disclaimer page: **O sajtu / Disclaimer**

Reference concept (not a copy): [reinformisanje.rs](https://reinformisanje.rs/) — this project aims at a tighter editorial architecture, cleaner WordPress output, and a machine-readable satire contract.

## What this repository is

| Layer | Role |
| --- | --- |
| `plugin/satira-srbija` | WordPress plugin: labels, meta, schema, REST extras, seed pages, admin desk |
| `middleware/` | Python pipeline: idea → LLM JSON → validate → WordPress **draft** |
| `schemas/` | Contract the model must obey |
| `prompts/` | System prompt for the satirist, plus correction pass |
| `docs/` | Information architecture, model choice, policy, MVP / phase 2 |

WordPress stays the CMS. The model never gets a shell, never gets `publish`, never talks to the public internet without an application password and a human review.

## Hard rules

1. Default post status is `draft`.
2. `satire_label` is a constant: `Satira / Parodija`.
3. Schema.org uses `Article` with `genre: Satire`. Not `NewsArticle`.
4. Secrets live in `.env`. Nothing is hardcoded.
5. Failed validation = no WordPress write. Correction pass first.
6. Real people and companies may appear only inside an already-labeled parody. No fabricated “exclusive quotes” dressed as reporting.
7. SEO does not hide the satire. Titles and descriptions say what the piece is.

## WordPress map

**Categories:** Politika, Tehnologija, AI, Internet, Društvo, Biznis, Kultura, Sport, Svet, Srbija, Apsurd dana

**Permalink:** `/%category%/%postname%/`

**Pages:** `/o-sajtu/` (disclaimer), `/satira-parodija/` (what the label means)

**Required post fields:** title, slug, excerpt, content, category, tags, author, featured image, alt text, satire label, SEO title, meta description, social title, social description, optional inspiration URL.

## Pipeline

```
IDEA  (CLI / HTTP / email / later Telegram)
  →  MEMORY LOOKUP (near-duplicate titles and punchlines)
  →  AI DRAFT (strict JSON)
  →  VALIDATOR (JSON + HTML allowlist + category + slug + label)
  →  CORRECTION PASS if needed
  →  WORDPRESS REST  POST /wp-json/wp/v2/posts  status=draft
  →  EDITOR REVIEW
  →  PUBLISH  (human only)
```

## Quick start (MVP)

1. WordPress 6.6+ with pretty permalinks and Application Passwords.
2. Copy `plugin/satira-srbija` into `wp-content/plugins/` and activate.
3. Create an Application Password for an Editor (not Administrator if you can avoid it).
4. Install a local model runner and pull **Gemma 2 9B Instruct** (or the 2B Instruct build on an 8 GB box).
5. Python 3.11+:

```bash
cd middleware
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
# edit ../.env
python -m satira.cli draft "Windows Update zatražio godišnji odmor."
```

The CLI prints the validated JSON and the WordPress draft URL. It does not publish.

HTTP desk (localhost only):

```bash
python -m satira.app
# POST /v1/draft  Authorization: Bearer $API_TOKEN
```

## Model choice (short)

On a constrained box, start with **Gemma 2 Instruct**. It follows JSON instructions cleanly, handles Serbian plus English, and stays cheap to run locally. Details and hardware table: [`docs/02-ai-models.md`](docs/02-ai-models.md).

## Security

See [`SECURITY.md`](SECURITY.md). The middleware binds to `127.0.0.1`. The plugin checks capabilities and nonces. HTML is sanitized on both sides. Logs never store tokens.

## License

GPL-2.0-or-later, same family as WordPress.
