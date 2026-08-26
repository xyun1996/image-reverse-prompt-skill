# Refine Visual Schema

Normalize an already analyzed visual schema before prompt compilation.

## Goals
- remove duplicate descriptions;
- make spatial relations explicit;
- keep high-impact visual features concise;
- preserve uncertain fields with confidence rather than guessing;
- ensure user-requested edits affect only intended fields;
- preserve locked fields such as composition, lighting, palette, or subject identity when the user explicitly asks to keep them.

## Priority
When resolving conflicts, prefer:
1. verified image evidence;
2. explicit user modifications;
3. high-confidence schema fields;
4. concise neutral wording.

Return the complete normalized schema only.
