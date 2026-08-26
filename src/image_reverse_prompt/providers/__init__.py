import os

from .base import VisionProvider
from .openai_provider import OpenAIProvider
from .qwen_provider import QwenProvider


def get_provider(name: str, model: str | None = None) -> VisionProvider:
    name = name.lower()
    if name == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for --provider openai")
        return OpenAIProvider(
            api_key=api_key,
            model=model or os.environ.get("IRP_OPENAI_MODEL", "gpt-4.1-mini"),
            base_url=os.environ.get("IRP_OPENAI_BASE_URL") or None,
        )
    if name == "qwen":
        if not os.environ.get("DASHSCOPE_API_KEY"):
            raise RuntimeError("DASHSCOPE_API_KEY is required for --provider qwen")
        return QwenProvider(model=model)
    raise ValueError(f"Unsupported provider: {name}. Supported: openai, qwen")


__all__ = ["VisionProvider", "OpenAIProvider", "QwenProvider", "get_provider"]
