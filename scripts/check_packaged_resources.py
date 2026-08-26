from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_RESOURCES = ROOT / "src" / "image_reverse_prompt" / "resources"

RESOURCE_GROUPS = {
    "prompts": "*.md",
    "adapters": "*.md",
    "schemas": "*.json",
}


def main() -> None:
    errors: list[str] = []

    for group, pattern in RESOURCE_GROUPS.items():
        source_dir = ROOT / group
        packaged_dir = PACKAGE_RESOURCES / group

        source_names = {p.name for p in source_dir.glob(pattern)}
        packaged_names = {p.name for p in packaged_dir.glob(pattern)}

        if source_names != packaged_names:
            errors.append(
                f"{group}: file sets differ; source={sorted(source_names)}, packaged={sorted(packaged_names)}"
            )
            continue

        for name in sorted(source_names):
            source = (source_dir / name).read_text(encoding="utf-8")
            packaged = (packaged_dir / name).read_text(encoding="utf-8")
            if source != packaged:
                errors.append(f"{group}/{name}: packaged copy differs from repository source")

    if errors:
        raise SystemExit("Packaged resource check failed:\n- " + "\n- ".join(errors))

    print("Packaged resources match repository sources.")


if __name__ == "__main__":
    main()
