from pathlib import Path

from .io_utils import dump_json, load_json
from .paths import adapter_text
from .providers import get_provider

SUPPORTED_TARGETS = {"gpt-image", "flux", "midjourney", "sdxl"}


def compile_schema_obj(schema: dict, target: str, provider_name: str, model: str | None = None) -> str:
    target = target.lower()
    if target not in SUPPORTED_TARGETS:
        raise ValueError(f"Unsupported target: {target}. Supported: {', '.join(sorted(SUPPORTED_TARGETS))}")
    provider = get_provider(provider_name, model=model)
    adapter = adapter_text(f"{target}.md")
    schema_json = dump_json(schema)
    instruction = (
        f"{adapter}\n\nInput visual schema:\n{schema_json}\n\n"
        "Compile the target prompt. Return only the final prompt text unless the adapter explicitly requires multiple labeled fields."
    )
    return provider.compile_prompt(schema_json, instruction)


def compile_from_schema(schema_file: Path, target: str, provider_name: str, model: str | None = None) -> str:
    return compile_schema_obj(load_json(schema_file), target, provider_name, model=model)
