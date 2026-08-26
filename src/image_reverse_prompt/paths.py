from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def prompt_path(name: str) -> Path:
    return repo_root() / "prompts" / name


def adapter_path(name: str) -> Path:
    return repo_root() / "adapters" / name


def schema_path_for_type(schema_type: str) -> Path:
    mapping = {
        "general": "visual-schema.json",
        "poster": "poster-schema.json",
        "product": "product-schema.json",
        "ui": "ui-schema.json",
    }
    try:
        filename = mapping[schema_type.lower()]
    except KeyError as exc:
        raise ValueError(f"Unsupported schema type: {schema_type}") from exc
    return repo_root() / "schemas" / filename
