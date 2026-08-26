#!/usr/bin/env python3
"""Build a ChatGPT-uploadable Skill directory and ZIP archive.

The repository root files are the canonical Skill sources. This script copies only
ChatGPT-relevant files into ``chatgpt-skill/`` and creates
``dist/image-reverse-prompt-chatgpt-skill.zip``.
"""

from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "chatgpt-skill"
DEFAULT_ZIP = ROOT / "dist" / "image-reverse-prompt-chatgpt-skill.zip"

INCLUDE = {
    "SKILL.md": None,
    "schemas": ("*.json",),
    "prompts": ("*.md",),
    "adapters": ("*.md",),
    "examples": ("*.json", "*.md"),
}


def _copy_selected(source: Path, destination: Path, patterns: tuple[str, ...]) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for pattern in patterns:
        for path in sorted(source.glob(pattern)):
            if path.is_file():
                shutil.copy2(path, destination / path.name)


def build(output_dir: Path = DEFAULT_OUTPUT, zip_path: Path = DEFAULT_ZIP) -> tuple[Path, Path]:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(ROOT / "SKILL.md", output_dir / "SKILL.md")
    for directory, patterns in INCLUDE.items():
        if patterns is None:
            continue
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
