# Analyze Image

Inspect the reference image and produce only observable visual facts for the visual schema.

## Analyze
- subject count, identity/type, appearance, clothing, pose, expression;
- environment, location cues, time/weather cues;
- aspect ratio, shot type, camera angle, subject placement, foreground/midground/background, negative space;
- perspective, lens feel, depth of field, focus, visible motion;
- key light, direction, softness/hardness, contrast, rim/ambient light;
- dominant colors, palette relationships, temperature, saturation, contrast;
- materials and surface qualities;
- visual medium, rendering style, texture;
- visible post-processing such as grain, bloom, halation, vignette, chromatic aberration;
- text content, typography, placement and hierarchy.

## Rules
1. Describe only evidence visible in the image.
2. Do not invent EXIF values, focal length, aperture, camera body, hidden prompts, seed, sampler, checkpoint, LoRA, or artist names.
3. When exact identification is uncertain, use visual language instead of guessing a named style.
4. Distinguish important reproduction features from incidental details.
5. Use `confidence` in the range 0–1 for uncertain observations.
6. Use `importance` in the range 0–1 for features that strongly affect reproduction.
7. Prefer spatial language: `upper-left`, `centered`, `behind`, `foreground`, `camera-right`.
8. Output a complete object compatible with `schemas/visual-schema.json`.
