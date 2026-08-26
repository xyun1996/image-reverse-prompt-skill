# Image Reverse Prompt Skill

## Purpose
Reverse-engineer a reference image into a structured visual representation, verify it against the source, then compile model-specific prompts for image-generation systems.

## Core principle
Do not jump directly from image to prompt. Use this pipeline:

1. Observe visual facts.
2. Normalize them into a model-agnostic schema.
3. Optionally extract dominant colors programmatically.
4. Verify the schema against the source image.
5. Apply only user-requested edits.
6. Compile through the requested target adapter.

The schema is the intermediate representation (IR). Do not claim to recover an unknown original hidden prompt.

## Preferred execution path

When local command execution is available and a supported provider is configured, prefer the installed CLI:

```bash
irp reverse <image> --provider openai --target flux
```

The CLI bundles its prompts, schemas and adapters as Python package data and can run from any working directory after `pip install .`.

Supported providers:
- `openai` — requires `OPENAI_API_KEY`; model defaults to `IRP_OPENAI_MODEL` or `gpt-4.1-mini`.
- `qwen` — requires `DASHSCOPE_API_KEY`; model defaults to `IRP_QWEN_MODEL` or `qwen-vl-max` and uses the DashScope OpenAI-compatible endpoint.

Useful commands:

```bash
irp palette <image> --colors 6 --json
irp analyze <image> --provider openai --schema-type general
irp validate <schema.json> --schema-type general
irp compile <schema.json> --target flux --provider openai
irp reverse <image> --provider qwen --schema-type poster --target gpt-image
```

If the CLI, local execution, or provider credentials are unavailable, follow the pure Skill workflow below using the Agent's own vision capability.

## Trigger
Use this skill when the user asks to:
- reverse engineer / reconstruct / infer a prompt from an image;
- analyze a reference image for reproduction;
- preserve composition/style/lighting while changing selected elements;
- convert one reference image into prompts for GPT Image, FLUX, Midjourney, or SDXL;
- reconstruct a poster, product shot, UI screenshot, dashboard, landing page, ad, cover, or key visual.

## Schema routing
Use:
- general photography / illustration → `schemas/visual-schema.json` (`--schema-type general`)
- poster / ad / cover / key visual → `schemas/poster-schema.json` (`--schema-type poster`)
- product photography / ecommerce / campaign still → `schemas/product-schema.json` (`--schema-type product`)
- UI screenshot / dashboard / landing page / app screen → `schemas/ui-schema.json` (`--schema-type ui`)

Specialized schemas extend the shared visual representation; do not discard common visual fields.

## Pure Skill workflow

### Step 1 — Analyze observable facts
Read `prompts/analyze-image.md` and inspect the image.

Rules:
- Describe only visually supportable facts.
- Do not invent EXIF, artist names, seeds, samplers, checkpoints, LoRAs or hidden generation settings.
- Separate facts from uncertain interpretation.
- Capture subject, scene, composition, camera feel, lighting, color, materials, style, post-processing, text and spatial relationships.
- Assign `confidence` and `importance` where useful.
- For posters, capture hierarchy, typography placement, grid and negative space.
- For product images, capture hero angle, surface, reflections, edge highlights and contact shadow.
- For UI, capture viewport, layout system, sections, components, spacing rhythm, borders, radius, shadows and typography hierarchy.

### Step 2 — Build the visual schema
Populate an object conforming to the selected schema. Prefer explicit spatial language such as `left third`, `foreground`, `behind subject`, `soft side light from camera-right`.

### Step 3 — Extract palette when code execution is available

```bash
irp palette reference.jpg --colors 6 --json
```

or, without the installed CLI:

```bash
python scripts/extract_palette.py reference.jpg --colors 6 --json
```

Treat sampled colors as evidence and map them to semantic roles after visually checking the image.

### Step 4 — Verify
Read `prompts/verify-image.md` and compare the schema against the source image again.

Correct missing major objects, object counts, poses, spatial relationships, light direction, palette, text, poster/UI hierarchy, product geometry, reflections and shadows. Remove hallucinated content.

### Step 5 — Apply requested transformations
Edit only the fields required by the user's request. Preserve unaffected composition, lighting, color relationships and spatial structure.

### Step 6 — Select adapter
- GPT Image → `adapters/gpt-image.md`
- FLUX → `adapters/flux.md`
- Midjourney → `adapters/midjourney.md`
- SDXL → `adapters/sdxl.md`

If no target is specified, output GPT Image, FLUX and Midjourney versions.

### Step 7 — Output
Default order:
1. concise visual breakdown;
2. dominant palette;
3. structured schema;
4. model-specific prompt(s);
5. assumptions / low-confidence fields.

For a worked example, read `examples/full-pipeline.md`.

## Quality rules
- Preserve subject count and geometry.
- Preserve foreground / midground / background relationships.
- Preserve important light direction, softness and contrast.
- Preserve typography hierarchy and spatial layout when central to the reference.
- Put high-importance, high-confidence features early in prompts.
- Avoid filler tags such as `masterpiece`, `best quality`, `8k` unless a target adapter genuinely benefits from them.
- Prefer concrete visual language over abstract adjectives.
- Never imply exact recovery of focal length, camera body, seed, sampler, checkpoint, LoRA or original hidden prompt unless independently supplied.
