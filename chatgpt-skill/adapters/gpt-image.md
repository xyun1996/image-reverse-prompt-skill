# GPT Image Adapter

Compile the verified visual schema into a natural-language image generation prompt optimized for GPT Image.

## Style
- Use coherent prose rather than tag soup.
- Describe subject and composition first, then environment, lighting, color/materials, and rendering/finish.
- State exact text content and placement when typography is important.
- Express spatial constraints explicitly.
- Keep important reference-preservation constraints in plain language.

## Avoid
- meaningless quality boosters (`masterpiece`, `best quality`, `8k`);
- unsupported camera metadata;
- invented artist names;
- repeating the same adjective in multiple forms.

## Output
Return:

```text
PROMPT:
<single production-ready prompt>
```

If the user requested transformations, clearly describe the modified elements while preserving all locked reference properties.
