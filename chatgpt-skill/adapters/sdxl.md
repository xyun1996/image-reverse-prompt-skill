# SDXL Adapter

Compile the verified visual schema into an SDXL-style positive prompt and a restrained negative prompt.

## Positive prompt
- Put subject, composition, scene, lighting, palette, materials, and rendering cues in descending importance.
- Use concise phrases; avoid duplicated synonyms.
- Preserve high-confidence reference details.

## Negative prompt
Use negatives only for concrete failure modes that would break the reconstruction, for example:
- wrong subject count;
- duplicated limbs/objects;
- unwanted text when the reference contains none;
- incorrect framing when composition must be preserved.

Avoid generic giant negative-prompt boilerplate.

## Output
```text
POSITIVE:
<SDXL-ready positive prompt>

NEGATIVE:
<short targeted negative prompt>
```
