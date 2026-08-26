from abc import ABC, abstractmethod
from pathlib import Path


class VisionProvider(ABC):
    @abstractmethod
    def analyze_image(self, image_path: Path, instruction: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_schema(self, image_path: Path, schema_json: str, instruction: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def compile_prompt(self, schema_json: str, instruction: str) -> str:
        raise NotImplementedError
