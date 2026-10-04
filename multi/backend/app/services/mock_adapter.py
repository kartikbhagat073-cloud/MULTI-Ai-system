from .model_adapter import ModelAdapter


class MockAdapter(ModelAdapter):
    """Temporary adapter used while building the UI and orchestration layer."""

    def __init__(self, name: str):
        self.name = name

    async def generate(self, prompt: str) -> str:
        return f"[{self.name} mock response]\n\nPrompt received: {prompt}"
