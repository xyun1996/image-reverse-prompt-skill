from pathlib import Path

from .io_utils import dump_json, load_text, parse_json_block
from .paths import prompt_path, schema_path_for_type
from .providers import get_provider
from .schema_tools import validate_schema_instance


def analyze_image_to_schema(
    image_path: Path,
    provider_name: str,
    model: str | None = None,
    schema_type: str = "general",
    verify: bool = True,
) -> dict:
    provider = get_provider(provider_name, model=model)
    analyze_prompt = load_text(prompt_path("analyze-image.md"))
    schema_guide = load_text(schema_path_for_type(schema_type))
    instruction = (
        f"{analyze_prompt}\n\n"
        "Return only valid JSON. Use this JSON Schema as structural guidance:\n"
        f"{schema_guide}"
    )
    schema = parse_json_block(provider.analyze_image(image_path, instruction))

    if verify:
        verify_prompt = load_text(prompt_path("verify-image.md"))
        verify_instruction = (
            f"{verify_prompt}\n\nCurrent schema:\n{dump_json(schema)}\n\n"
            "Return the corrected complete JSON object only."
        )
        schema = parse_json_block(
            provider.verify_schema(image_path, dump_json(schema), verify_instruction)
        )

    validate_schema_instance(schema, schema_type=schema_type)
    return schema
