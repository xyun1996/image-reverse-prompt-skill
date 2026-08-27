---
name: image-reverse-prompt
description: Reverse-engineer reference images into structured visual schemas and model-specific prompts for reproducible image generation.
---

# Image Reverse Prompt Skill

## Purpose
Reverse-engineer a reference image into a structured visual representation, verify it against the source image, then compile model-specific prompts for image-generation systems.

## Core principle
Do not jump directly from image to prompt. Use this pipeline:

1. Observe visual facts.
2. Normalize them into a model-agnostic schema.
3. Verify the schema against the source image.
4. Apply only user-requested edits.
5. Compile through the requested target adapter.

The schema is the intermediate representation (IR). Never claim to recover an unknown original hidden prompt exactly.

## Trigger
Use this skill when the user asks to:
- reverse engineer / reconstruct / infer a prompt from an image;
- analyze a reference image for visual reproduction;
- preserve composition, style, lighting, layout, or palette while changing selected elements;
- convert a reference image into prompts for GPT Image, FLUX, Midjourney, or SDXL;
- reconstruct a poster, product shot, UI screenshot, dashboard, landing page, ad, cover, or key visual.

## Schema routing
Use:
- general photography / illustration → `schemas/visual-schema.json`
- poster / ad / cover / key visual → `schemas/poster-schema.json`
- product photography / ecommerce / campaign still → `schemas/product-schema.json`
- UI screenshot / dashboard / landing page / app screen → `schemas/ui-schema.json`

Specialized schemas extend the common visual representation. Preserve the shared fields.

## Workflow

### Step 1 — Analyze observable facts
Read `prompts/analyze-image.md` and inspect the reference image.

Rules:
- Describe only visually supportable facts.
- Do not invent EXIF, exact focal length, artist names, seeds, samplers, checkpoints, LoRAs, or hidden generation settings.
- Separate facts from uncertain interpretation.
- Capture subject, scene, composition, camera feel, lighting, color, materials, style, post-processing, text, and spatial relationships.
- Assign `confidence` and `importance` where useful.
- For posters, capture hierarchy, typography placement, grid, CTA, graphic devices, and negative space.
- For product images, capture hero angle, surface finish, reflections, edge highlights, support surface, and contact shadow.
- For UI, capture viewport, layout system, navigation, sections, components, spacing rhythm, borders, radius, shadows, and typography hierarchy.

### Step 2 — Build the visual schema
Populate an object conforming to the selected schema.

Prefer explicit spatial language such as `left third`, `foreground`, `behind subject`, `camera-right`, `soft side light from camera-left`, and `negative space above headline`.

### Step 3 — Verify against the source image
Read `prompts/verify-image.md` and inspect the image again.

Correct:
- missing major objects;
- wrong subject or object counts;
- incorrect pose, orientation, gaze, or spatial relations;
- incorrect crop, framing, perspective, or depth;
- wrong light direction, softness, contrast, or rim light;
- wrong dominant color relationships;
- hallucinated text, objects, materials, or style labels;
- incorrect poster/UI hierarchy;
- incorrect product geometry, reflections, or shadows.

Move uncertain interpretation into `uncertainties` rather than presenting it as fact.

### Step 4 — Apply requested transformations
Edit only the schema fields required by the user's request.

Examples:
- change the subject while preserving composition and lighting;
- change the environment while preserving pose and camera feel;
- replace a product while preserving campaign lighting and background treatment;
- preserve UI layout while changing brand palette and typography;
- preserve poster hierarchy while replacing headline copy and hero object.

### Step 5 — Refine
When useful, read `prompts/refine-schema.md` and normalize the verified schema before compilation. Remove duplicate language and keep high-impact features concise.

### Step 6 — Select adapter
- GPT Image → `adapters/gpt-image.md`
- FLUX → `adapters/flux.md`
- Midjourney → `adapters/midjourney.md`
- SDXL → `adapters/sdxl.md`

If no target is specified, output GPT Image, FLUX, and Midjourney versions.

### Step 7 — Output
Default response order:
1. concise visual breakdown;
2. dominant palette described semantically;
3. structured schema;
4. model-specific prompt(s);
5. assumptions or low-confidence fields.

## Quality rules
- Preserve subject count and geometry.
- Preserve foreground / midground / background relationships.
- Preserve important light direction, softness, and contrast.
- Preserve typography hierarchy and spatial layout when central to the reference.
- Put high-importance, high-confidence features early in prompts.
- Avoid filler quality tags such as `masterpiece`, `best quality`, or `8k` unless a target adapter genuinely benefits from them.
- Prefer concrete visual language over abstract adjectives.
- Never imply exact recovery of focal length, camera body, seed, sampler, checkpoint, LoRA, or the original hidden prompt unless independently supplied.
