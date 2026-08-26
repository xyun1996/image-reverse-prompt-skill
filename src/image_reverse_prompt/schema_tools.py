from pathlib import Path

from jsonschema import Draft202012Validator

from .io_utils import load_json
from .paths import schema_path_for_type


def validate_schema_instance(data: dict, schema_type: str = "general") -> None:
    schema = load_json(schema_path_for_type(schema_type))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(data)


def validate_json_file(path: Path, schema_type: str = "general") -> None:
    validate_schema_instance(load_json(path), schema_type=schema_type)
