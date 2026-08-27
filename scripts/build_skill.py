#!/usr/bin/env python3
"""Build a ChatGPT-uploadable Skill directory and ZIP archive.

The repository root Skill resources remain the canonical shared source. ChatGPT uses
``SKILL.chatgpt.md`` as its dedicated manifest, while schemas/prompts/adapters are
synced from the root directories into ``chatgpt-skill/``.
"""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHATGPT_MANIFEST = ROOT / "SKILL.chatgpt.md"
DEFAULT_OUTPUT = ROOT / "chatgpt-skill"
DEFAULT_ZIP = ROOT / "dist" / "image-reverse-prompt-chatgpt-skill.zip"

RESOURCE_DIRS = {
    "schemas": ("*.json",),
    "prompts": ("*.md",),
    "adapters": ("*.md",),
}

REQUIRED_FRONT_MATTER = ("name", "description")


def _validate_front_matter(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path.name}: SKILL.md must start with YAML front matter delimited by ---")

    try:
        closing_index = next(
            i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"
        )
    except StopIteration as exc:
        raise ValueError(f"{path.name}: YAML front matter is missing the closing --- delimiter") from exc

    metadata: dict[str, str] = {}
    for line in lines[1:closing_index]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            raise ValueError(f"{path.name}: malformed YAML metadata line: {line!r}")
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")

    missing = [key for key in REQUIRED_FRONT_MATTER if not metadata.get(key)]
    if missing:
        raise ValueError(
            f"{path.name}: missing required YAML metadata: {', '.join(missing)}"
        )

    name = metadata["name"]
    if not all(ch.islower() or ch.isdigit() or ch == "-" for ch in name):
        raise ValueError(
            f"{path.name}: name must use lowercase letters, digits, and hyphens only: {name!r}"
        )


def _copy_selected(source: Path, destination: Path, patterns: tuple[str, ...]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for pattern in patterns:
        for path in sorted(source.glob(pattern)):
            if path.is_file():
                shutil.copy2(path, destination / path.name)


def build(output_dir: Path = DEFAULT_OUTPUT, zip_path: Path = DEFAULT_ZIP) -> tuple[Path, Path]:
    _validate_front_matter(CHATGPT_MANIFEST)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(CHATGPT_MANIFEST, output_dir / "SKILL.md")
    _validate_front_matter(output_dir / "SKILL.md")

    for directory, patterns in RESOURCE_DIRS.items():
        _copy_selected(ROOT / directory, output_dir / directory, patterns)

    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(output_dir))

    return output_dir, zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the ChatGPT Skill bundle")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--zip", dest="zip_path", type=Path, default=DEFAULT_ZIP)
    args = parser.parse_args()

    output_dir, zip_path = build(args.output_dir, args.zip_path)
    print(f"Built ChatGPT Skill directory: {output_dir}")
    print(f"Built ChatGPT Skill ZIP: {zip_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
