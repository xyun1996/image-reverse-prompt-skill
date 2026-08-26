#!/usr/bin/env python3
"""Validate repository JSON Schemas and JSON examples."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
EXAMPLE_DIR = ROOT / "examples"
BASE_SCHEMA_PATH = SCHEMA_DIR / "visual-schema.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema_documents() -> list[str]:
    errors: list[str] = []
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            schema = load_json(path)
            Draft202012Validator.check_schema(schema)
            print(f"[ok] schema: {path.relative_to(ROOT)}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
    return errors


def validate_examples() -> list[str]:
    errors: list[str] = []
    base_schema = load_json(BASE_SCHEMA_PATH)
    validator = Draft202012Validator(base_schema)

    for path in sorted(EXAMPLE_DIR.glob("*.json")):
        try:
            instance = load_json(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue

        instance_errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if instance_errors:
            for err in instance_errors:
                loc = ".".join(str(p) for p in err.path) or "<root>"
                errors.append(f"{path.relative_to(ROOT)} @ {loc}: {err.message}")
        else:
            print(f"[ok] example: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    errors = []
    errors.extend(validate_schema_documents())
    errors.extend(validate_examples())

    if errors:
        print("\nValidation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print("\nAll schema and example validation checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
