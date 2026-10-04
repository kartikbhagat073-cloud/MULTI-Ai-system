from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models.schemas import CompareRequest, CompareResponse
from .services.orchestrator import compare_models

app = FastAPI(title="AI Model Arena API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/compare", response_model=CompareResponse)
async def compare(request: CompareRequest):
    responses = await compare_models(request.prompt, request.models)
    return CompareResponse(prompt=request.prompt, responses=responses)
