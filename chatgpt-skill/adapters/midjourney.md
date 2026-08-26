# Midjourney Adapter

Compile the verified visual schema into a concise Midjourney prompt.

## Style
- Start with subject + scene + composition.
- Add lighting, palette, material, mood, and rendering cues.
- Keep wording visual and compact.
- Preserve important spatial relationships.
- Append only parameters justified by the user or schema.

## Parameters
- `--ar` may be derived from the reference aspect ratio.
- Do not invent stylize, chaos, seed, or model-version parameters unless requested.
- If the user provides desired parameters, append them unchanged unless invalid.

## Output
```text
PROMPT:
<Midjourney prompt> --ar <ratio>
```

Optional user-requested transformations should replace only the relevant schema fields before compilation.
