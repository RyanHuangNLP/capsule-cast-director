---
name: directing-capsule-casts
description: Design rounded, capsule-eyed cartoon casts and write coherent shot prompts in monochrome, modern, prehistoric, cozy, or historical settings. Use for character briefs, reference-image prompts, storyboards, and short animated stories; the skill does not itself render media.
---

# Capsule Cast Director

Turn a story idea into a recognizable cast and a set of usable shots. The five looks share volumetric silhouettes drawn as flat color shapes; wardrobe and world design distinguish them.

## Start with the requested deliverable

Read [the drawing and look guide](references/looks.md). Use the user's selected look, clothes, colors, setting, language and output format. When a choice is missing, make a reasonable proposal and state the assumption. Avoid reopening settled choices.

- **A character or image prompt:** deliver a resolved character description and the requested image directions. A written description is enough to invent an original character. Inspect a supplied reference before claiming to preserve it. Do not ask for video duration or narration.
- **A storyboard:** read [shot planning](references/shot-planning.md) and deliver the plan at the requested level of detail. A proposal-only request stops before final generator prompts.
- **Final video prompts:** use the shot guide to deliver complete, independent shot cards. Ask for approval only when the brief calls for a review step or an unresolved choice materially changes the outcome. Authorization to deliver final prompts already covers that step.
- **Actual images or video:** use available generation tools only within the user's requested scope. This skill has no provider connection. State which files were actually generated and inspected.

Read [historical grounding](references/historical-grounding.md) for period-specific or factual material. Read [sound direction](references/sound.md) only when a video needs audio decisions. Use [the package format](references/package-format.md) and `scripts/package.py` when a structured multi-shot package would help; ordinary prose output does not require JSON.

## Design decisions that persist

Resolve a cast register before writing shots: each person's build, face color, hair/headwear, garments, limb colors and distinguishing details. Treat these as story-wide decisions. Pose, cropping and lighting belong to individual shots. An intentional costume change gets its own named description.

The standard face uses two dark upright pill-shaped eyes. Its mood comes from timing and body language. Head tilt rotates the eyes with the head; perspective and occlusion may hide one. Clothing conceals a filled body, never a wire skeleton. Do not expose hidden limbs through sleeves or scenery.

Preserve the five looks' recognizable features. Historical subjects keep the chosen skin tone and period dress; the white face used by some other looks is not a universal requirement. A user's explicit anatomical or facial redesign is a custom variant: identify the change instead of calling it the standard design.

Keep a separate ledger for important objects: what each object is, how many exist, who supports it and where it ends a shot. At a handoff, establish the next support before removing the previous one. A change of camera does not teleport a prop.

## Deliver and check

Each standalone shot must contain enough information to recreate its visible cast, drawing treatment, setting, physical action and sound without access to another prompt. The optional renderer expands shared definitions automatically. Its checks cover timing and declared state, not visual quality or historical truth.

Before delivery, compare the result with the user's brief. Check duration arithmetic, wardrobe and palette, readable blocking, object support, requested language, and silence where required. Separate image-sheet requirements from scene requirements: a transparent full-body cutout does not prohibit a later scene's background, ground contact or close-up.

For generated media, report the evidence actually inspected: images, sampled frames, full playback and/or audio. Do not describe text review as a successful film test. Keep voice and image references, source claims and tool capabilities specific to the current work.
