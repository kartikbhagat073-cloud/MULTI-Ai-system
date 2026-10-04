# System Architecture — MVP

```text
React + Tailwind/UI
        |
        | POST /api/compare
        v
FastAPI API
        |
        v
Orchestrator
        |
        +---- ModelAdapter -> GPT
        +---- ModelAdapter -> Gemini
        +---- ModelAdapter -> Claude
        +---- ModelAdapter -> Ollama
        |
        v
Normalized ModelResponse[]
        |
        v
Comparison UI
        |
        v
User selects output
        |
        v
Continuation context
```

## Design rule

Every provider implements the same adapter contract. Provider-specific authentication, request formats, retries, and response parsing stay inside that provider adapter.
