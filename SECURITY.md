# Security

## Non-negotiable

- AI output status is `draft`. There is no publish path in middleware.
- No public unauthenticated generation endpoint.
- No model access to a shell, to `wp-cli`, or to the WordPress filesystem.
- Application passwords live in `.env`. Rotate if a draft log ever prints one.
- HTML from the model is allowlisted, then sanitized again in WordPress with `wp_kses`.

## WordPress

- Capability for the admin desk: `edit_posts`.
- Publish remains `publish_posts`.
- REST registration uses `permission_callback`.
- Forms use nonces.
- Uninstall removes plugin options. It does not bulk-delete posts.

## Middleware

- Bind `127.0.0.1`.
- `API_TOKEN` required when the HTTP server is on.
- Rate limit per token.
- Timeouts on both LLM and WordPress clients.
- Logs at INFO: idea hash, category, slug, WP post ID. Never password, never token, never raw `.env`.

## Satire misuse

Labeling is a product requirement and a legal hygiene requirement. A missing label is a validator failure, not a theme cosmetic. RSS, Open Graph, and JSON-LD must carry the same signal as the article body.

## Abuse of real people

The system prompt forbids authentic-looking exclusive quotes. The validator cannot fully detect that class of harm. The human editor is the last control. Keep it.
