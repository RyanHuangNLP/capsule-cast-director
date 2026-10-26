# Drawing language and five looks

## Shared construction

Design people as an assembly of closed silhouettes: a generous rounded head, a compact chest-and-hip mass, broad soft-edged arms and legs, small paddle-like hands and blunt rounded feet. Render this construction in flat 2D, with color boundaries doing most of the work. Keep joints plausible without outlining a skeleton. Four head-heights is a useful starting proportion, not a measurement that overrides a reference or a requested body type.

Give the face two dark vertical pill marks, separated enough to read at thumbnail size. Omit a drawn mouth, nose, eyebrows, pupils and eye sparkle in the standard design. Use shoulder height, pauses, head angle, distance and gesture to convey emotion. A beard or fringe can be a simple mass of color; it does not require new facial features.

Describe these decisions in a complete drawing paragraph for the project. Avoid relying on a brand name as the entire style instruction. Small edge accents and restrained shading are fine; glossy toy materials, heavy contour drawing and hairline limbs are outside the standard treatment. The design is human or humanoid as requested, with no automatic mechanical parts.

## Look selector

Numbers 1–5 are convenient aliases for the five families. The first two have two variants each. They all use the construction above.

| Look key | Alias | Character palette and clothing | World |
|---|---|---|---|
| `mono-light` | 1 / classic light | White face with a narrow dark edge; ink-dark torso, limbs, hands and feet; plain featureless mascot | White flat field and economical diagram-like objects |
| `mono-dark` | 1 / classic dark | White head and filled body; dark eye marks; plain featureless mascot | Black flat field and economical diagram-like objects |
| `modern-studio` | 2A | White face, red knit cap, yellow tee, dark shorts, broad charcoal limbs and dark shoes | Bright studio, light perspective grid, cyan or blue interface shapes |
| `modern-story` | 2B | The same red-cap/yellow-tee cast as 2A | Colored streets, rooms and landscapes with cinematic depth |
| `prehistoric` | 3 | White heads, dark hair masses and filled limbs; ochre/tan hide garments | Earth, stone, plants, campfire light and rough scenic surfaces |
| `cozy` | 4 | White head and trunk, dark filled limbs; a specified everyday outfit may cover the trunk | Welcoming ordinary places, soft light and local color |
| `heritage` | 5 / historical | Story-specific face colors, hair, headwear, layered garments and footwear | A researched or explicitly imagined period setting |

The outfit and setting are separate controls. Switching from studio to scenic modern changes the world, not the hat or shirt. An explicit costume/palette request overrides a default and becomes part of the cast register.

### 1. Monochrome

Keep the canvas optically flat. Do not introduce paper texture, atmospheric illumination, floor shadows or a faux-3D room. Color accents can identify props or explanatory symbols without changing the person's palette. The white face in the light variant keeps the dark eyes legible. An unclothed mascot is a smooth abstract form without anatomical detail.

A transparent-sheet request removes the white/black canvas while retaining the selected body colors. A fine outline can separate the white face from a white background; it must not reduce the body to linework.

### 2. Modern

Keep the red cap smooth and without a bobble by default. The yellow shirt wraps a rounded torso; sleeves and shorts should have clear edges where the substantial dark limbs emerge. Resolve an original character's identity rather than reusing a named mascot from a reference project.

Studio prompts use clean geometry and icon-based glassy cyan panels. Scenic prompts use the story's real locations and can have weather, layered distance and moving light. Do not let studio panels or a mandatory grid migrate into a scenic version. The people retain flat colors even when the scenery has depth.

### 3. Prehistoric

Separate recurring roles through silhouette, hair, clothing cut and an accessory or prop. A tall gatherer and a broad elder should remain distinguishable in grayscale. Hide patches may be irregular, but the body beneath is a mass, not a set of strokes.

Let humor arise from a task, an incentive and an observable consequence. A still reaction can be enough. Label invented social jokes as fiction; a stylized cave story is not evidence about real prehistoric societies. Quiet percussion or natural sound can fit, but neither comedy nor music is compulsory.

### 4. Cozy

Keep a gentle everyday atmosphere while retaining the brief's emotional stakes. A character may be lonely, frustrated or tired without the film becoming artificially cheerful. Honor a supplied cardigan, coat, glasses or bag consistently. Do not import the modern look's cap by default.

Choose locations because an action needs them. A whole story can occur at one kitchen counter. Reuse the room layout for continuous action; a location change should be motivated and explicit. Mouthless staging can lift a cup to face height without inventing lip contact.

### 5. Heritage

Start with period, place and the status of the story's claims. Select clothing silhouettes, fastenings, headwear, tools and built surroundings from that context. No single soldier costume represents all history. Use the [historical grounding note](historical-grounding.md) to distinguish evidence from reconstruction.

Preserve a reference subject's identity cues and skin tone. Changing garments for a requested era should be described independently from the identity. Robes, aprons and armor can cover the filled limbs naturally; do not draw anatomy through them.

## Sheet and scene checks

For a character sheet, resolve the requested pose, view count, margins, background and props. A single full-body three-quarter view is a useful default. Validate the actual alpha channel if transparency was generated.

For a scene, resolve where the character stands, what supports the objects, how the camera sees the action and which body parts are naturally outside the frame. A close-up can crop the feet. Shadows and contact follow the selected world; only the monochrome variants intentionally avoid environmental depth.
