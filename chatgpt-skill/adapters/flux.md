# FLUX Adapter

Compile the verified visual schema into a dense, concrete FLUX prompt.

## Style
- Front-load subject, framing, and composition.
- Follow with environment, lighting, palette, materials, and finish.
- Prefer compact comma-separated clauses, but keep natural syntax where relationships matter.
- Preserve geometry and spatial relationships explicitly.
- Include only visually meaningful modifiers.

## Avoid
- unsupported camera specs;
- empty quality tags;
- excessive negative phrasing;
- stylistic names that were not visibly justified.

## Output
```text
PROMPT:
<single FLUX-ready prompt>
```

If a negative prompt is requested, add:
```text
NEGATIVE:
<only failure modes relevant to the requested reconstruction>
```
