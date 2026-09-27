# Workflows

## REST (primary)

```
middleware
  → validate
  → POST /wp-json/wp/v2/tags
  → GET  /wp-json/wp/v2/categories?slug=
  → POST /wp-json/wp/v2/posts
       status: draft
       categories: [id]
       tags: [ids]
       excerpt
       slug
       featured_media: 0 in MVP unless a file was uploaded by a human
       meta / registered fields: satire_label, seo_*, social_*, inspiration_*
```

Auth: `Authorization: Basic base64(user:application_password)`

Never log that header.

## Email (optional)

Subject may start with `[SATIRA]`.

Body may be free text or:

```
TITLE:
CATEGORY:
TAGS:
TEXT:
IMAGE:
NOTES:
```

Parser fills what it can. Missing fields go to the model. The model still returns the full JSON contract. WordPress still receives a draft.

Disable IMAP until the mailbox is a dedicated inbox. Do not point this at a personal mailbox that also receives bank mail.

## Phone-sized inlet (Phase 2)

Telegram or Discord: two sentences → same `pipeline.run(idea)`. The bot answers with the draft permalink in `wp-admin`. That path is specified so the HTTP API stays stable. It is not in MVP on purpose.

## Human desk inside WordPress

Plugin page **Satira**:

- New idea
- Generate (calls middleware if `SATIRA_MIDDLEWARE_URL` is set)
- Preview
- Open draft in the block editor

Regenerate / funnier / subtler / shorten / expand are Phase 2 buttons on stored versions. MVP keeps version rows in SQLite so those buttons have somewhere to land.
