import json
from pathlib import Path

from jsonschema import Draft202012Validator

from .io_utils import load_json
from .paths import schema_text_for_type


def load_schema_for_type(schema_type: str = "general") -> dict:
    schema = json.loads(schema_text_for_type(schema_type))
    if schema_type.lower() != "general":
        base_schema = json.loads(schema_text_for_type("general"))
        all_of = schema.get("allOf", [])
        if all_of and all_of[0].get("$ref") == "./visual-schema.json":
            all_of[0] = base_schema
    return schema


def validate_schema_instance(data: dict, schema_type: str = "general") -> None:
    schema = load_schema_for_type(schema_type)
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(data)


def validate_json_file(path: Path, schema_type: str = "general") -> None:
    validate_schema_instance(load_json(path), schema_type=schema_type)
