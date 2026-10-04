# AI Compare

Send one prompt to several AI models, compare outputs side by side, pick one, then edit, copy or refine it.

**Stack:** FastAPI (Python) backend, Tailwind CSS frontend, SQLite for saved choices.

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # add at least two API keys
uvicorn app.main:app --reload
```
Open http://localhost:8000 (interactive API docs at /docs).

## API
| Method | Path | Purpose |
|---|---|---|
| GET | /api/models | Models and whether a key is configured |
| POST | /api/ask | One model, full conversation (used for results and refining) |
| POST | /api/compare | Same prompt to many models in parallel |
| POST | /api/select | Save the chosen output |
| GET | /api/history | Recent choices |

## Add a model
Append a `ModelSpec` to `REGISTRY` in `app/providers.py`. Anything OpenAI-compatible (Groq, Together, OpenRouter, local Ollama) only needs `kind="openai"` and a base URL.

API keys live only in `.env` on the server. Tailwind loads from its CDN for simplicity; for production, build it with the Tailwind CLI.
