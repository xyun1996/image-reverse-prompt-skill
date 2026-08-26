# Image Reverse Prompt Skill

## Purpose
Reverse-engineer a reference image into a structured visual representation, verify the representation against the image, then compile model-specific prompts for image generation systems.

## Core principle
Do not jump directly from image to prompt. Use this pipeline:

1. Observe visual facts.
2. Normalize them into `schemas/visual-schema.json`.
3. Verify the schema against the source image.
4. Apply only user-requested edits.
5. Compile the result through a target adapter.

The schema is the intermediate representation (IR). It should remain model-agnostic.

## Trigger
Use this skill when the user asks to:
- reverse engineer / reconstruct / infer a prompt from an image;
- analyze a reference image for reproduction;
- preserve composition/style/lighting while changing selected elements;
- convert one reference image into prompts for GPT Image, FLUX, Midjourney, or SDXL.

## Workflow

### Step 1 — Analyze observable facts
Read `prompts/analyze-image.md` and inspect the image.

Rules:
- Describe what is visually observable.
- Do not invent camera EXIF, artist names, model names, or hidden generation settings.
- Separate facts from uncertain interpretation.
- Capture subject, scene, composition, camera feel, lighting, color, materials, style, post-processing, text, and spatial relationships.
- Assign `confidence` and `importance` where useful.

### Step 2 — Build the visual schema
Populate an object conforming to `schemas/visual-schema.json`.

Keep fields concise and composable. Prefer explicit spatial relations such as `left third`, `centered`, `foreground`, `behind subject`, `soft rim light from camera-right` over vague prose.

### Step 3 — Verify
Read `prompts/verify-image.md` and compare the schema with the source image again.

Correct:
- missing major objects;
- wrong object counts;
- wrong poses or spatial relationships;
- wrong light direction or quality;
- wrong dominant colors;
- hallucinated text or objects;
- contradictions between fields.

### Step 4 — Apply requested transformations
If the user asks to modify the reference, edit only the necessary schema fields.

Examples:
- `change woman to man` → edit subject attributes while preserving composition/lighting unless requested otherwise;
- `make it Tokyo at night` → edit scene/environment/time while preserving unaffected fields;
- `keep layout exactly` → lock composition fields.

### Step 5 — Select adapter
Use the requested target:
- GPT Image → `adapters/gpt-image.md`
- FLUX → `adapters/flux.md`
- Midjourney → `adapters/midjourney.md`
- SDXL → `adapters/sdxl.md`

If no target is specified, output GPT Image, FLUX, and Midjourney versions.

### Step 6 — Output
Default response order:
1. concise visual breakdown;
2. dominant palette;
3. structured schema;
4. model-specific prompt(s);
5. assumptions or low-confidence fields, if any.

## Quality rules
- Preserve subject count and geometry.
- Preserve foreground / midground / background relationships.
- Preserve important light direction, softness, and contrast.
- Put high-importance, high-confidence features early in prompts.
- Avoid filler quality tags such as `masterpiece`, `best quality`, `8k`, unless the adapter explicitly benefits from them.
- Do not claim to recover the original hidden prompt. The goal is reproducible visual reconstruction.
- Prefer concrete visual language over abstract adjectives.

## Optional color extraction
When code execution is available, dominant colors may be sampled programmatically instead of guessed. Use extracted colors as evidence, then map them to semantic roles such as background, skin, accent, highlight, shadow.

## Expected files
- `schemas/visual-schema.json`
- `prompts/analyze-image.md`
- `prompts/verify-image.md`
- `prompts/refine-schema.md`
- `adapters/gpt-image.md`
- `adapters/flux.md`
- `adapters/midjourney.md`
- `adapters/sdxl.md`
