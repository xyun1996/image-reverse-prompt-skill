import os

from .openai_provider import OpenAIProvider


class QwenProvider(OpenAIProvider):
    def __init__(self, api_key: str | None = None, model: str | None = None, base_url: str | None = None):
        super().__init__(
            api_key=api_key or os.environ["DASHSCOPE_API_KEY"],
            model=model or os.environ.get("IRP_QWEN_MODEL", "qwen-vl-max"),
            base_url=base_url
            or os.environ.get(
                "IRP_QWEN_BASE_URL",
                "https://dashscope.aliyuncs.com/compatible-mode/v1",
            ),
        )
