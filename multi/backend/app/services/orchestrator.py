import asyncio
import time
from .mock_adapter import MockAdapter
from ..models.schemas import ModelResponse


async def run_model(model: str, prompt: str) -> ModelResponse:
    started = time.perf_counter()
    try:
        adapter = MockAdapter(model)
        output = await adapter.generate(prompt)
        latency = int((time.perf_counter() - started) * 1000)
        return ModelResponse(model=model, output=output, latency_ms=latency)
    except Exception as exc:
        latency = int((time.perf_counter() - started) * 1000)
        return ModelResponse(model=model, error=str(exc), latency_ms=latency)


async def compare_models(prompt: str, models: list[str]) -> list[ModelResponse]:
    # Run providers concurrently so one slow model does not block sequentially.
    return await asyncio.gather(*(run_model(model, prompt) for model in models))
