# From brief to shot cards

## Establish the story's commitments

Record the deliverable, look, cast, audience, ratio, duration, spoken language, audio mode and any supplied sources. Infer inexpensive missing choices from context and make them visible in the proposal. If there is no timing guidance, suggest a one-minute story in shots of roughly ten seconds; a user-specified duration takes precedence. Character-only work skips this stage.

Use three compact registers:

- **Cast:** full appearance descriptions, including the outfit actually worn.
- **World:** drawing treatment, location designs, color roles and important historical assumptions.
- **Objects:** one identity per physical item, its appearance and its support at the opening and close of each shot.

Keep changing physical state out of permanent appearance descriptions. A red book can stay red while moving from a shelf to a hand to a table.

## Plan the action before camera decoration

Give each shot a purpose, an opening condition, a short sequence of visible actions and a result. Allocate enough time for reaching, contact, release and a reaction. Keep the object's support clear through a handoff; a transfer via a surface consists of placing, releasing and then picking up one object.

Use the requested total exactly. For example, 35 seconds could be 12 + 9 + 8 + 6 seconds; it does not need rounding to a multiple of ten. Choose lengths compatible with a selected generator when known, or describe them as editorial targets until a provider is selected.

Compose for the aspect ratio. A vertical frame often benefits from depth, staggered characters and upward/downward reveals. A wide frame can hold lateral movement and two-person interaction. Do not treat changing the ratio token as sufficient recomposition.

Use camera moves only when they reveal useful information. Show a hand close-up with enough visible context to identify whose hand it is. An obscured limb remains attached out of sight. Do not duplicate it to make every body part visible.

At each cut, state whether action continues or time/place changes. Preserve identity and item ownership unless the story explicitly accounts for a change. Explain an off-screen move instead of silently resetting the ledger. A camera cut alone is not a reason for an object to change hands.

## Deliver the requested stage

A proposal can be a short cast/world register and a table of shots, including exact dialogue where relevant. Stop there if the user asked to review a concept. When final prompts are already requested or approved, proceed without another approval question.

A final shot card contains:

1. Shot identifier, length, framing ratio and location.
2. The full project drawing description and full descriptions of the visible characters, including current clothes.
3. The visible objects and their opening support/placement; track off-frame items separately for continuity without directing the generator to depict them.
4. Timed action with camera and naturally hidden/cropped parts.
5. Exact speech, applicable speaker descriptions, and the music/effects decision from [sound direction](sound.md).
6. Resulting object state, cut connection and relevant exclusions.

Do not refer to another shot as the only description of a person, voice or style. The [structured package](package-format.md) can store each shared description once and use `scripts/package.py render` to expand it into every applicable card.

Follow the requested language for dialogue and discussion. Production directions may use English if the target tool benefits from it, but that does not authorize translating the spoken line. Put requested subtitles or titles in an editing plan unless the actual generator supports controllable text.

## References and generation

Label each supplied image's purpose: identity, wardrobe, drawing treatment, composition or previous ending frame. An image showing one role does not provide identity for a different role. A previous ending frame helps only when the next shot genuinely continues that situation.

Keep the complete shot card as the reusable specification. If an image-to-video interface expects only movement instructions, adapt the submitted field to that interface while retaining the full card. Verify current provider limits instead of assuming a named duration, reference count, audio mode or transparency feature is available.

For an authorized media trial, start with a character view, then a keyframe and a short action that stresses the relevant movement. Preserve accepted outputs. Do not retry an inaccurate image indefinitely; report the specific mismatch and respect the actual generation scope and budget.

## Editorial handoff

Supply shot order, approximate trim points, planned cuts, optional overlay text and sound assembly notes. A requested transition is a direction for editing, not proof that generated clips will join. Inspect actual usable frames before choosing final trim points.

Text checks establish whether the package is coherent. Rendered-image review establishes appearance in those images. Frame sampling covers the sampled moments. Only playback and listening can assess the corresponding full motion and sound. State the inspected scope plainly.
