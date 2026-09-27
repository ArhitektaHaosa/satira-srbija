# AI models

Priority order: free, open weights, self-hosted, cheap API last.

The writer model must follow a JSON schema, write Serbian that a human editor will not have to rewrite from scratch, and keep a deadpan register. Humor quality is judged by the editor, not by a benchmark.

## Recommendation

**Primary writer: Gemma 2 Instruct**

- 9B Q4 on a 16 GB box
- 2B Instruct Q4 on an 8 GB box
- Strong instruction following and JSON shape
- Usable Serbian and English in the same piece
- Apache-2.0 weights

That is the default in `.env.example`.

A second pass with the same model (correction prompt) is better than a three-model pipeline on a small machine. Add a proofreader model only when the writer consistently breaks HTML.

## Comparison (editorial use, not lab scores)

| Model | Serbian | Humor control | JSON discipline | RAM (Q4) | License note |
| --- | --- | --- | --- | --- | --- |
| Gemma 2 9B Instruct | good | good if prompted dry | strong | ~8–10 GB | Apache-2.0 |
| Gemma 2 2B Instruct | acceptable | thinner jokes | strong | ~3 GB | Apache-2.0 |
| Llama 3.1 8B Instruct | good | variable | good | ~8 GB | community license |
| Mistral 7B Instruct | weaker Serbian | dry possible | good | ~6–8 GB | Apache-2.0 |
| Qwen2.5 7B Instruct | mixed | uneven on Balkan register | strong | ~6–8 GB | Qwen license |

Use one writer. Do not split “ideas / writing / proof” across three models in MVP. Extra hops add latency and drift.

Embeddings for memory: `nomic-embed-text` via the same local runner, or hash+trigram fallback if embeddings are not installed. The code path degrades cleanly.

## What not to do

- Do not send raw Application Passwords to the model.
- Do not fine-tune on scraped news homepages in MVP.
- Do not hide the satire label to “win SEO”.
- Do not call a hosted API from the WordPress server if a local Gemma answers.

## Hardware ladder

| RAM | Model |
| --- | --- |
| 8 GB | Gemma 2 2B Instruct Q4 |
| 16 GB | Gemma 2 9B Instruct Q4 |
| 24 GB+ | Gemma 2 9B Q5/Q8 or a larger instruct build |

Context window: 8k is enough for idea + memory + article + correction.
