# WordPress information architecture

## Content types

Use native `post` for articles. Do not invent a custom post type in MVP. Editors already know Posts. Archives, feeds, and plugins expect `post`.

Pages:

- `O sajtu / Disclaimer` → slug `o-sajtu`
- `Šta znači SATIRA / PARODIJA` → slug `satira-parodija`

## Categories (closed set)

| Slug | Name |
| --- | --- |
| politika | Politika |
| tehnologija | Tehnologija |
| ai | AI |
| internet | Internet |
| drustvo | Društvo |
| biznis | Biznis |
| kultura | Kultura |
| sport | Sport |
| svet | Svet |
| srbija | Srbija |
| apsurd-dana | Apsurd dana |

One primary category per article. Tags carry the long tail (`windows-update`, `mirc`, `uprava`).

## URLs

Permalink structure: `/%category%/%postname%/`

Examples:

- `/tehnologija/windows-update-trazio-godisnji-odmor/`
- `/politika/ministarstvo-uvodi-captcha-za-upravu/`

Keep slugs ASCII, hyphenated, Serbian latin without diacritics.

## Templates the theme must support

The plugin adds badges and JSON-LD. The theme still needs:

- front page: featured row + latest + “Apsurd dana”
- single post
- category archive
- tag archive
- author archive
- search
- 404

Related posts: same category, exclude current, 3 items, plugin query.
Trending: last 7 days by comment count, fallback to last published.
Featured: sticky posts. Editors pin. AI does not pin.

## Single article chrome

Order of visible elements:

1. SATIRA / PARODIJA badge (link to `/satira-parodija/`)
2. Category
3. Headline (`h1`)
4. Standfirst (excerpt)
5. Featured image + alt
6. Body (semantic HTML from the pipeline)
7. Inspiration box if `inspiration_url` exists
8. Footer line: “Ovaj tekst je satira/parodija.”
9. Author + date
10. Tags
11. Related

## Author pages

One house author is enough for MVP (`Redakcija`). Individual bylines later. Do not invent biographies for fictional staff.

## Search

Default `/?s=` is fine. Exclude the disclaimer page from “related” modules only.

## Structured data

`Article` + `genre: Satire` + `isFamilyFriendly` as the editor decides + `speakable` omitted.

Do not emit `NewsArticle`, `ReportageNewsArticle`, or `ClaimReview`.
