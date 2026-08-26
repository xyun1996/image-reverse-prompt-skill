from importlib.resources import files


_SCHEMA_FILES = {
    "general": "visual-schema.json",
    "poster": "poster-schema.json",
    "product": "product-schema.json",
    "ui": "ui-schema.json",
}


def resource_text(category: str, name: str) -> str:
    """Read a UTF-8 resource bundled inside the installed Python package."""
    resource = files("image_reverse_prompt").joinpath("resources", category, name)
    return resource.read_text(encoding="utf-8")


def prompt_text(name: str) -> str:
    return resource_text("prompts", name)


def adapter_text(name: str) -> str:
    return resource_text("adapters", name)


def schema_text_for_type(schema_type: str) -> str:
    try:
        filename = _SCHEMA_FILES[schema_type.lower()]
    except KeyError as exc:
        supported = ", ".join(sorted(_SCHEMA_FILES))
        raise ValueError(f"Unsupported schema type: {schema_type}. Supported: {supported}") from exc
    return resource_text("schemas", filename)


def schema_filename_for_type(schema_type: str) -> str:
    try:
        return _SCHEMA_FILES[schema_type.lower()]
    except KeyError as exc:
        supported = ", ".join(sorted(_SCHEMA_FILES))
        raise ValueError(f"Unsupported schema type: {schema_type}. Supported: {supported}") from exc
