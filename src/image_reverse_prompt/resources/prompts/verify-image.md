# Verify Image Against Schema

Re-open the source image and audit the current visual schema. This is a correction pass, not a creative pass.

## Check for
- missing major subjects or props;
- wrong subject/object counts;
- incorrect pose, gaze, orientation, or spatial relation;
- incorrect foreground / midground / background placement;
- wrong framing, crop, camera angle, or apparent perspective;
- wrong key-light direction, softness, contrast, or rim light;
- missing dominant colors or incorrect palette relationships;
- invented materials, style labels, text, objects, or scene details;
- contradictions between schema fields;
- low-confidence guesses represented as facts.

## Rules
1. Preserve correct fields.
2. Correct only discrepancies supported by the image.
3. Remove hallucinated information.
4. Move uncertain interpretation to `uncertainties` with a confidence score.
5. Return the full corrected schema, not a patch or commentary.
