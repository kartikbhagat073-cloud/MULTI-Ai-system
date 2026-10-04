from abc import ABC, abstractmethod


class ModelAdapter(ABC):
    """Common interface every AI provider must implement."""

    name: str

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError
