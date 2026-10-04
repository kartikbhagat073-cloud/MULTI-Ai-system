import asyncio
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()
from . import db  # noqa: E402
from .providers import BY_ID, REGISTRY, ProviderError, generate  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.client = httpx.AsyncClient(timeout=httpx.Timeout(120.0, connect=10.0))
    yield
    await app.state.client.aclose()


app = FastAPI(title="AI Compare", lifespan=lifespan)


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=50_000)


class AskRequest(BaseModel):
    model: str
    messages: list[Message] = Field(min_length=1)


class CompareRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=50_000)
    models: list[str] = Field(min_length=2)


class SelectRequest(BaseModel):
    prompt: str
    model: str
    output: str
    outputs: dict[str, str] = {}


async def _run(model_id: str, messages: list[dict]) -> dict:
    spec = BY_ID.get(model_id)
    if not spec:
        return {"model": model_id, "text": None, "error": "Unknown model", "ms": 0}
    t0 = time.perf_counter()
    try:
        text = await generate(spec, messages, app.state.client)
        return {"model": model_id, "text": text, "error": None, "ms": int((time.perf_counter() - t0) * 1000)}
    except ProviderError as e:
        return {"model": model_id, "text": None, "error": str(e), "ms": int((time.perf_counter() - t0) * 1000)}


@app.get("/api/models")
def list_models():
    return [{"id": s.id, "label": s.label, "model": s.model, "ready": s.ready} for s in REGISTRY]


@app.post("/api/ask")
async def ask(req: AskRequest):
    """One model, full conversation. Used for per-model results and for refining a chosen output."""
    if req.model not in BY_ID:
        raise HTTPException(404, "Unknown model")
    return await _run(req.model, [m.model_dump() for m in req.messages])


@app.post("/api/compare")
async def compare(req: CompareRequest):
    """Same prompt to many models at once; one failure never blocks the others."""
    ids = list(dict.fromkeys(req.models))
    if len(ids) < 2:
        raise HTTPException(422, "Choose at least two different models")
    msgs = [{"role": "user", "content": req.prompt}]
    return {"results": await asyncio.gather(*(_run(i, msgs) for i in ids))}


@app.post("/api/select")
def select(req: SelectRequest):
    return {"id": db.save(req.prompt, req.model, req.output, req.outputs)}


@app.get("/api/history")
def history(limit: int = 20):
    return db.recent(max(1, min(limit, 100)))


app.mount("/", StaticFiles(directory=Path(__file__).resolve().parent.parent / "static", html=True), name="static")
