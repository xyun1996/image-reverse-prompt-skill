from pathlib import Path

from .analyzer import analyze_image_to_schema
from .compiler import compile_schema_obj
from .palette import extract_palette


def reverse_image(
    image_path: Path,
    target: str,
    provider_name: str,
    model: str | None = None,
    schema_type: str = "general",
    num_colors: int = 6,
    verify: bool = True,
) -> dict:
    palette = extract_palette(image_path, num_colors=num_colors)
    schema = analyze_image_to_schema(
        image_path=image_path,
        provider_name=provider_name,
        model=model,
        schema_type=schema_type,
        verify=verify,
    )
    schema.setdefault("color", {})["palette"] = [c["hex"] for c in palette["colors"]]
    prompt = compile_schema_obj(schema, target, provider_name, model=model)
    return {
        "image": str(image_path),
        "provider": provider_name,
        "model": model,
        "schema_type": schema_type,
        "target": target,
        "palette": palette,
        "schema": schema,
        "prompt": prompt,
    }
