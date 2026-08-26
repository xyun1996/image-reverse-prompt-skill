# image-reverse-prompt-skill

A model-agnostic Agent Skill and installable Python CLI for reverse-engineering reference images into structured visual schemas and compiling prompts for GPT Image, FLUX, Midjourney and SDXL.

## Pipeline

```text
Reference image
    ↓
Vision provider (OpenAI / Qwen)
    ↓
visual facts → schema IR
    ↓
optional palette extraction
    ↓
verification pass
    ↓
optional edits
    ↓
model adapter
    ↓
final prompt
```

The goal is reproducible visual reconstruction, not recovery of an unknown original hidden prompt.

## Features

- Agent Skill workflow in `SKILL.md`
- Installable `irp` CLI
- Runtime resources bundled inside the Python package
- OpenAI vision provider
- Qwen vision provider through DashScope OpenAI-compatible API
- General / poster / product / UI schemas
- Second-pass image verification
- Programmatic dominant-color extraction
- GPT Image / FLUX / Midjourney / SDXL prompt adapters
- JSON Schema validation and CI

## Install

Clone and install normally:

```bash
git clone https://github.com/xyun1996/image-reverse-prompt-skill.git
cd image-reverse-prompt-skill
python -m pip install .
```

Editable development installs also work:

```bash
python -m pip install -e .
```

After installation, `irp` can be run from any working directory because prompts, adapters and schemas are bundled as package data.

```bash
cd /tmp
irp --help
```

## Provider configuration

### OpenAI

```bash
export OPENAI_API_KEY=...
export IRP_OPENAI_MODEL=gpt-4.1-mini
```

Optional compatible endpoint:

```bash
export IRP_OPENAI_BASE_URL=https://your-endpoint/v1
```

### Qwen / DashScope

```bash
export DASHSCOPE_API_KEY=...
export IRP_QWEN_MODEL=qwen-vl-max
export IRP_QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

## CLI

### Extract palette

```bash
irp palette reference.jpg --colors 6
irp palette reference.jpg --colors 6 --json
```

### Validate schema

```bash
irp validate examples/portrait.json
irp validate poster.json --schema-type poster
```

### Analyze image into a schema

```bash
irp analyze reference.jpg --provider openai --schema-type general
```

```bash
irp analyze poster.png \
  --provider qwen \
  --schema-type poster \
  --output poster-schema-output.json
```

By default `analyze` performs a second visual verification pass. Skip it only when needed:

```bash
irp analyze reference.jpg --provider openai --no-verify
```

### Compile an existing schema

```bash
irp compile examples/portrait.json --target flux --provider openai
```

Supported targets:

```text
gpt-image
flux
midjourney
sdxl
```

### Full image → prompt pipeline

```bash
irp reverse reference.jpg --provider openai --target flux
```

```bash
irp reverse poster.png \
  --provider qwen \
  --schema-type poster \
  --target gpt-image \
  --output result.json
```

`reverse` returns a JSON object containing the extracted palette, verified schema and final compiled prompt.

## Agent Skill usage

A vision-capable Agent can still use the repository without the CLI by following `SKILL.md` and reading the human-readable root `prompts/`, `schemas/` and `adapters/` files.

When local command execution and provider credentials are available, the preferred execution path is:

```text
irp reverse <image> --provider <provider> --target <target>
```

When command execution or credentials are unavailable, fall back to the pure Skill workflow.

## Schema routing

| Reference type | Schema type | Extra focus |
| --- | --- | --- |
| General photography / illustration | `general` | subject, composition, lighting, color, style |
| Poster / ad / cover / key visual | `poster` | hierarchy, typography, grid, CTA, negative space |
| Product / ecommerce / campaign still | `product` | hero angle, finish, reflections, contact shadow, props |
| UI / dashboard / landing page | `ui` | layout, components, spacing, typography, radius, borders, shadows |

## Package resources

The root resource directories remain easy to read and edit as part of the Skill:

```text
prompts/
schemas/
adapters/
```

The CLI uses bundled copies under:

```text
src/image_reverse_prompt/resources/
├── prompts/
├── schemas/
└── adapters/
```

Runtime loading uses `importlib.resources`, so installed commands do not depend on the repository root or current working directory. `scripts/check_packaged_resources.py` prevents the root resources and packaged copies from drifting apart.

## Repository layout

```text
image-reverse-prompt-skill/
├── .github/workflows/ci.yml
├── SKILL.md
├── pyproject.toml
├── src/image_reverse_prompt/
│   ├── cli.py
│   ├── analyzer.py
│   ├── compiler.py
│   ├── reverse.py
│   ├── palette.py
│   ├── schema_tools.py
│   ├── paths.py
│   ├── providers/
│   │   ├── base.py
│   │   ├── openai_provider.py
│   │   └── qwen_provider.py
│   └── resources/
│       ├── prompts/
│       ├── schemas/
│       └── adapters/
├── schemas/
├── prompts/
├── adapters/
├── scripts/
├── examples/
└── LICENSE
```

## Validation and CI

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python scripts/check_packaged_resources.py
python -m compileall -q scripts src
irp validate examples/portrait.json
```

GitHub Actions performs a non-editable `pip install .`, validates schemas/examples, checks packaged resource synchronization, compiles Python files, smoke-tests the CLI and then changes to `/tmp` to verify packaged resources can be loaded outside the repository.

## Design principles

1. Observation before generation.
2. Schema as a model-agnostic intermediate representation.
3. Verify against the reference before compiling.
4. Apply only requested mutations.
5. Prefer concrete spatial/light/material/color language.
6. Do not invent EXIF, seeds, checkpoints, samplers or the original hidden prompt.
7. Keep high-importance, high-confidence features dominant.

## License

MIT
