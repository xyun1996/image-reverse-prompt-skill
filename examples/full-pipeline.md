# End-to-end example

This is a worked example showing how the Skill should move from reference-image observations to a verified visual schema and then to model-specific prompts.

> The example image is hypothetical so the repository can remain text-only. Replace the observation block with facts from the user's real reference image.

## 1. Reference-image observations

Observed facts:

- One woman, waist-up, slightly left of center.
- She is standing beside a rain-covered window at night.
- Dark shoulder-length hair, neutral expression, looking past camera-right.
- Black wool coat over a muted cream top.
- Outside the window: defocused cyan and warm amber city lights.
- Main illumination is soft, cool window light from camera-right.
- A weaker warm practical light brushes the left side of the background.
- Shallow depth of field; face and upper torso are sharp, city lights are strongly blurred.
- Overall palette: charcoal, cool cyan, muted cream, small amber accents.
- Fine film grain and restrained highlight bloom.

Uncertain:

- Exact focal length cannot be known from the image.
- The location is urban, but the city is not identifiable.

## 2. Extracted palette

Example output from `scripts/extract_palette.py`:

```json
{
  "palette": [
    {"hex": "#171B20", "share": 0.31},
    {"hex": "#2C3B43", "share": 0.24},
    {"hex": "#789BA1", "share": 0.16},
    {"hex": "#D4C6AF", "share": 0.12},
    {"hex": "#B36D3D", "share": 0.09},
    {"hex": "#E7DED0", "share": 0.08}
  ]
}
```

Semantic mapping:

- background/shadows: `#171B20`
- cool environment: `#2C3B43`, `#789BA1`
- skin/top highlights: `#D4C6AF`, `#E7DED0`
- warm city accent: `#B36D3D`

## 3. Verified visual schema

```json
{
  "subject": {
    "type": "adult woman",
    "appearance": "dark shoulder-length hair",
    "clothing": "black wool coat over muted cream top",
    "pose": "standing, torso angled slightly toward camera-left",
    "expression": "neutral and contemplative"
  },
  "scene": {
    "location": "interior beside a large city window",
    "environment": "rain on glass, blurred urban lights outside",
    "time": "night",
    "weather": "rain"
  },
  "composition": {
    "shot_type": "waist-up portrait",
    "camera_angle": "near eye level",
    "subject_position": "slightly left of center",
    "foreground": "subtle out-of-focus window edge",
    "midground": "subject",
    "background": "rain-streaked glass and city bokeh"
  },
  "camera": {
    "lens_feel": "natural portrait perspective",
    "perspective": "compressed enough to isolate subject without obvious telephoto distortion",
    "depth_of_field": "shallow",
    "focus": "eyes and face"
  },
  "lighting": {
    "key_light": "soft cool window light",
    "direction": "camera-right toward subject",
    "quality": "broad and diffused",
    "contrast": "medium-low",
    "rim_light": "very subtle cool separation on hair",
    "ambient_light": "weak warm city/practical contamination in background"
  },
  "color": {
    "dominant_colors": ["charcoal", "cool cyan-gray", "muted cream", "small amber accents"],
    "palette": ["#171B20", "#2C3B43", "#789BA1", "#D4C6AF", "#B36D3D", "#E7DED0"],
    "temperature": "cool overall with warm accent contrast",
    "saturation": "low to moderate",
    "contrast": "restrained"
  },
  "materials": ["wet glass", "wool coat", "soft knit fabric"],
  "style": {
    "medium": "cinematic photography",
    "visual_style": "quiet urban portrait",
    "texture": "fine film grain",
    "rendering": "naturalistic skin and restrained highlights"
  },
  "post_processing": {
    "grain": "fine",
    "bloom": "subtle around distant lights",
    "halation": "minimal",
    "vignette": "very light",
    "chromatic_aberration": "none visible"
  },
  "text": {
    "present": false,
    "content": [],
    "font_style": "",
    "layout": ""
  },
  "uncertainties": [
    "exact city is unknown",
    "exact focal length is not inferable"
  ]
}
```

## 4. GPT Image prompt

A cinematic waist-up portrait of an adult woman standing beside a large rain-covered city window at night. Place her slightly left of center, with her torso angled subtly toward camera-left while she looks past camera-right with a neutral, contemplative expression. She has dark shoulder-length hair and wears a black wool coat over a muted cream top. Keep the face and upper torso sharply focused while the rain-streaked glass and distant city lights fall into strong soft bokeh. Light her primarily with broad, diffused cool window light coming from camera-right, with only a faint warm amber contamination in the distant background. Use a restrained charcoal, cyan-gray and muted cream palette with sparse amber accents. Preserve natural skin texture, fine film grain, subtle bloom around distant lights, and a quiet cinematic mood. Avoid adding extra people, signage, props, or identifiable city landmarks.

## 5. FLUX prompt

cinematic waist-up urban portrait, one adult woman slightly left of center beside a rain-covered window at night, dark shoulder-length hair, black wool coat over muted cream top, neutral contemplative expression, gaze past camera-right, natural portrait perspective, shallow depth of field, eyes and face sharply focused, rain-streaked glass, strongly blurred cyan-gray and amber city bokeh, broad soft cool key light from camera-right, subtle cool hair separation, weak warm background contamination, charcoal and cool cyan-gray dominant palette, muted cream skin and clothing highlights, sparse amber accents, naturalistic skin texture, fine film grain, restrained highlight bloom, quiet moody atmosphere, preserve subject count and composition, no extra objects or text

## 6. Midjourney prompt

cinematic waist-up portrait of one woman beside a rain-covered city window at night, slightly left of center, dark shoulder-length hair, black wool coat, muted cream top, contemplative neutral expression, looking past camera-right, shallow depth of field, rain-streaked glass, cyan-gray and amber city bokeh, broad diffused cool window light from camera-right, restrained charcoal and cyan palette with sparse warm amber accents, natural skin texture, fine film grain, subtle bloom, quiet urban mood --ar 4:5 --stylize 100

## 7. Why the prompts differ

- **GPT Image** gets explicit natural-language constraints and relational instructions.
- **FLUX** gets a dense visual description with important features front-loaded.
- **Midjourney** gets a compact visual phrase plus generation parameters.

The visual schema remains unchanged across all three outputs.
