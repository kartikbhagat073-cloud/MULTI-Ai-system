"""One adapter per API style. Add a model by appending a ModelSpec to REGISTRY."""
import os
from dataclasses import dataclass

import httpx


class ProviderError(Exception):
    pass


@dataclass(frozen=True)
class ModelSpec:
    id: str
    label: str
    kind: str  # "openai" (OpenAI-compatible) | "anthropic" | "gemini"
    key_env: str
    model_env: str
    default_model: str
    base_url: str = ""
    base_url_env: str = ""

    @property
    def api_key(self) -> str:
        return os.getenv(self.key_env, "").strip()

    @property
    def model(self) -> str:
        return os.getenv(self.model_env) or self.default_model

    @property
    def url(self) -> str:
        return (os.getenv(self.base_url_env) if self.base_url_env else "") or self.base_url

    @property
    def ready(self) -> bool:
        return bool(self.api_key)


REGISTRY: list[ModelSpec] = [
    ModelSpec("gpt", "GPT", "openai", "OPENAI_API_KEY", "OPENAI_MODEL", "gpt-4o",
              base_url="https://api.openai.com/v1"),
    ModelSpec("claude", "Claude", "anthropic", "ANTHROPIC_API_KEY", "ANTHROPIC_MODEL", "claude-sonnet-5-5"),
    ModelSpec("gemini", "Gemini", "gemini", "GEMINI_API_KEY", "GEMINI_MODEL", "gemini-2.0-flash"),
    # Llama is served by third parties; default is Groq, but any OpenAI-compatible host works.
    ModelSpec("llama", "Llama", "openai", "LLAMA_API_KEY", "LLAMA_MODEL", "llama-3.3-70b-versatile",
              base_url="https://api.groq.com/openai/v1", base_url_env="LLAMA_BASE_URL"),
    ModelSpec("mistral", "Mistral", "openai", "MISTRAL_API_KEY", "MISTRAL_MODEL", "mistral-large-latest",
              base_url="https://api.mistral.ai/v1"),
]
BY_ID = {s.id: s for s in REGISTRY}


def _raise_for(r: httpx.Response) -> dict:
    try:
        data = r.json()
    except ValueError:
        raise ProviderError(f"HTTP {r.status_code}: {r.text[:200]}")
    if r.status_code >= 400:
        err = data.get("error") if isinstance(data, dict) else None
        msg = err.get("message") if isinstance(err, dict) else (err or r.reason_phrase)
        raise ProviderError(f"HTTP {r.status_code}: {msg}")
    return data


async def generate(spec: ModelSpec, messages: list[dict], client: httpx.AsyncClient) -> str:
    if not spec.ready:
        raise ProviderError(f"{spec.key_env} is not set")
    try:
        if spec.kind == "openai":
            r = await client.post(
                f"{spec.url}/chat/completions",
                headers={"Authorization": f"Bearer {spec.api_key}"},
                json={"model": spec.model, "messages": messages},
            )
            return _raise_for(r)["choices"][0]["message"]["content"] or ""
        if spec.kind == "anthropic":
            r = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": spec.api_key, "anthropic-version": "2023-06-01"},
                json={"model": spec.model, "max_tokens": 2000, "messages": messages},
            )
            return "".join(b.get("text", "") for b in _raise_for(r)["content"] if b.get("type") == "text")
        if spec.kind == "gemini":
            r = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{spec.model}:generateContent",
                headers={"x-goog-api-key": spec.api_key},
                json={"contents": [
                    {"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
                    for m in messages
                ]},
            )
            parts = _raise_for(r)["candidates"][0]["content"]["parts"]
            return "".join(p.get("text", "") for p in parts)
    except httpx.TimeoutException:
        raise ProviderError("The request timed out")
    except httpx.HTTPError as e:
        raise ProviderError(f"Network error: {e}")
    except (KeyError, IndexError):
        raise ProviderError("The provider returned an unexpected response (it may have blocked the request)")
    raise ProviderError(f"Unknown provider type {spec.kind}")
