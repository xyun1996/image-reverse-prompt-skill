# image-reverse-prompt-skill

A model-agnostic Agent Skill for reverse-engineering a reference image into a structured visual schema, verifying it against the source image, and compiling production-ready prompts for multiple image-generation models.

## Why this exists

Direct `image → prompt` generation tends to mix observation, guessing and model-specific prompt habits. This project separates the process into stages:

```text
Reference image
    ↓
Visual fact analysis
    ↓
Base or specialized schema (model-agnostic IR)
    ↓
optional programmatic palette extraction
    ↓
verification pass
    ↓
optional user edits
    ↓
model adapter
    ├── GPT Image
    ├── FLUX
    ├── Midjourney
    └── SDXL
```

The goal is not to claim recovery of the original hidden prompt. The goal is reproducible visual reconstruction.

## Features

- Image → structured visual schema
- Explicit subject / scene / composition / camera / lighting / color / materials / style analysis
- Confidence and importance signals
- Second-pass visual verification to reduce hallucinations
- Selective edits while preserving locked reference properties
- Specialized poster / product photography / UI schemas
- Programmatic dominant-color extraction helper
- GPT Image, FLUX, Midjourney and SDXL adapters
- End-to-end worked example
- JSON Schema + example validation in CI
- Python syntax checks on every push / pull request
- Model-agnostic: use any sufficiently capable vision model or vision-enabled Agent

## Repository layout

```text
image-reverse-prompt-skill/
├── .github/workflows/ci.yml
├── SKILL.md
├── schemas/
│   ├── visual-schema.json
│   ├── poster-schema.json
│   ├── product-schema.json
│   └── ui-schema.json
├── prompts/
│   ├── analyze-image.md
│   ├── verify-image.md
│   └── refine-schema.md
├── adapters/
│   ├── gpt-image.md
│   ├── flux.md
│   ├── midjourney.md
│   └── sdxl.md
├── scripts/
│   ├── extract_palette.py
│   └── validate_repo.py
├── examples/
│   ├── portrait.json
│   └── full-pipeline.md
├── requirements.txt
├── requirements-dev.txt
└── LICENSE
```

## Quick start

Give a vision-capable Agent a reference image and ask it to use this skill.

```text
Reverse engineer this image and give me GPT Image, FLUX and Midjourney prompts.
```

```text
Analyze this reference image. Keep composition and lighting, change the subject to a man, and compile a FLUX prompt.
```

```text
Reverse engineer this poster. Preserve typography hierarchy and layout, but replace the product with a black mechanical keyboard.
```

```text
Reconstruct this dashboard screenshot. Keep layout and component hierarchy but change the brand palette to monochrome.
```

## Schema routing

| Reference type | Schema | Extra focus |
| --- | --- | --- |
| General photography / illustration | `visual-schema.json` | subject, composition, lighting, color, style |
| Poster / ad / cover / key visual | `poster-schema.json` | hierarchy, typography, grid, CTA, negative space |
| Product / ecommerce / campaign still | `product-schema.json` | hero angle, finish, reflections, contact shadow, props |
| UI / dashboard / landing page | `ui-schema.json` | layout, components, spacing, typography, radius, borders, shadows |

The specialized schemas extend the common visual representation instead of replacing it.

## Workflow

### 1. Observe

Use `prompts/analyze-image.md` to extract visual facts only. Do not guess hidden generation settings, EXIF values, seeds, samplers, LoRAs, checkpoints or artist names.

### 2. Normalize

Map observations into the selected schema. Treat the schema as an intermediate representation (IR) between vision analysis and model-specific prompt generation.

### 3. Extract palette (optional)

```bash
python -m pip install -r requirements.txt
python scripts/extract_palette.py reference.jpg --colors 6 --json
```

### 4. Verify

Use `prompts/verify-image.md` for a second inspection of the original image. Remove hallucinations and correct object count, geometry, light direction, palette, text and spatial relationships.

### 5. Transform

Apply user-requested changes only to affected schema fields. Unmodified fields remain reference-locked.

### 6. Compile

Choose an adapter from `adapters/` and compile the verified schema into the target model's preferred prompt style.

## Validation and CI

Install validation dependencies and run the same checks used by GitHub Actions:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python -m py_compile scripts/*.py
```

`validate_repo.py` checks that:

- every JSON file under `schemas/` is a valid Draft 2020-12 JSON Schema;
- every JSON example under `examples/` parses correctly;
- JSON examples conform to `schemas/visual-schema.json`.

GitHub Actions runs these checks automatically on pushes to `main` and on pull requests.

## Worked example

See [`examples/full-pipeline.md`](examples/full-pipeline.md).

It demonstrates:

```text
reference observations
  ↓
extracted palette
  ↓
verified visual schema
  ↓
GPT Image prompt
FLUX prompt
Midjourney prompt
```

## Design principles

1. **Observation before generation** — visual facts come first.
2. **Schema as IR** — the analysis is independent of the image-generation backend.
3. **Verify before compiling** — the second visual pass catches hallucinations.
4. **Selective mutation** — user edits should not accidentally destroy composition or lighting.
5. **Concrete language** — prefer spatial, lighting, material and palette descriptions over vague style adjectives.
6. **No fake precision** — do not invent focal lengths, camera bodies, hidden seeds or original prompts.
7. **Importance over verbosity** — high-impact visual features should dominate the final prompt.
8. **Specialize only where useful** — domain schemas add poster/product/UI semantics while preserving the shared IR.

## Vision backends

This Skill intentionally does not depend on one VLM. Possible backends include:

- an Agent with built-in image understanding;
- Qwen-VL family models;
- JoyCaption;
- other local or hosted VLMs capable of structured visual analysis.

## Roadmap

- optional OCR-aware typography analysis
- reference-image similarity evaluation loop
- ComfyUI integration
- optional provider adapters for local VLM execution

## License

MIT
