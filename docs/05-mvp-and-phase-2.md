# MVP and Phase 2

## MVP (this repository)

Ships:

- plugin that forces the satire contract on the site
- disclaimer pages on activation
- category seed
- REST field registration
- Python pipeline: idea → Gemma JSON → validate → correction → WP draft
- CLI
- localhost HTTP API with bearer token
- SQLite editorial memory with embedding-or-trigram fallback
- email parser module (no daemon until enabled)
- JSON schema and system prompt

Does not ship:

- automatic image generation
- automatic publish
- public API
- Telegram / Discord bots
- multi-author workflow
- ads, newsletters, comments policy

Success test:

> Operator types `python -m satira.cli draft "Windows Update zatražio godišnji odmor."`
> WordPress shows a draft with badge, excerpt, headings, footer, SEO meta, image prompt, and status Draft.

## Phase 2

- Versioned regenerate actions on the admin desk
- Featured image generation from `featured_image_prompt` into the Media Library, still as a draft attachment
- IMAP worker under systemd
- Telegram inlet
- Related / trending widgets with caching
- Optional PHP-only worker for hosts that will not run Python
- Human evaluation sheet: would a hurried reader forward this as news? If yes, kill the piece

Phase 2 still does not auto-publish.
