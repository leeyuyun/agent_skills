# Object Realism Guidelines

Use this file when decorative objects should look realistic (for example persimmon, produce, tools, or people cutouts).

## Realism Levels

1. `iconic`:
- Flat shape, minimal shading, symbolic usage.

2. `semi-realistic`:
- Directional lighting, edge shading, highlights, cast shadow.
- Required when users ask for "more real" object feel but still want deterministic generation.

3. `photo-real`:
- Real photo assets or high-fidelity renders.
- Use when the user explicitly asks for realistic photography quality.

## Semi-Realistic Object Checklist

1. Form:
- Keep object silhouette consistent with real anatomy.
- Avoid perfect circles when natural objects are slightly irregular.

2. Light:
- Add at least one primary highlight and one shadow region.
- Keep light direction consistent across same slide.

3. Material cues:
- Add subtle texture/noise and edge falloff.
- Keep saturation realistic; avoid glow-like clipping.

4. Context:
- Add short cast shadow for grounding.
- Keep object count low near text lanes.

5. Placement:
- Respect text-safe zones and callout lanes.
- Use corner anchoring for decorative objects by default.

## QA Hints

1. If objects look like stickers, increase shadow softness and reduce saturation.
2. If objects look like lights, reduce highlight alpha and add darker edge ring.
3. If objects steal focus from text, reduce count and increase minimum gap to text shapes.
