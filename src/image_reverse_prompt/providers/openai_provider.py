import base64
import mimetypes
from pathlib import Path

from openai import OpenAI

from .base import VisionProvider


def image_to_data_url(image_path: Path) -> str:
    mime = mimetypes.guess_type(image_path.name)[0] or "image/jpeg"
    data = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"


class OpenAIProvider(VisionProvider):
    def __init__(self, api_key: str, model: str, base_url: str | None = None):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def _vision(self, image_path: Path, instruction: str, system: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": instruction},
                        {"type": "image_url", "image_url": {"url": image_to_data_url(image_path)}},
                    ],
                },
            ],
            temperature=0.1,
        )
        return response.choices[0].message.content or ""

    def analyze_image(self, image_path: Path, instruction: str) -> str:
        return self._vision(image_path, instruction, "You are a careful visual analyst. Output valid JSON only.")

    def verify_schema(self, image_path: Path, schema_json: str, instruction: str) -> str:
        return self._vision(image_path, instruction, "You verify image schemas against references. Output corrected valid JSON only.")

    def compile_prompt(self, schema_json: str, instruction: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an image prompt compiler. Follow the target adapter exactly."},
                {"role": "user", "content": instruction},
            ],
            temperature=0.2,
        )
        return (response.choices[0].message.content or "").strip()
