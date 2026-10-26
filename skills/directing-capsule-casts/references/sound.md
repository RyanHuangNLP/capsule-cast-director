# Sound belongs to the story

Resolve three independent choices: spoken words, music and physical sound. Do not infer a narrator from a video request. Keep the user's requested language and mode:

| Mode | Speech | Music | Effects |
|---|---|---|---|
| Silent | None | None | None |
| Environment only | None | None | Requested room, weather and action sounds |
| Scored without speech | None | Chosen score | Optional effects |
| Spoken | Exact assigned lines | Optional score | Optional effects |

An explicitly silent brief has no ambient track. “No narration, only footsteps and rain” is environment-only rather than silent. These distinctions also apply in the optional JSON package.

## Describe speakers once

Choose a voice from the brief, not from a character's clothing or visual style. A useful description covers language/accent, perceived age and register, tone/texture, pace, phrasing and recording space. Do not assign a masculine low register to a voice the user described as light and youthful. Give multiple requested speakers their own identities and assign each line.

Repeat the complete applicable speaker description in every independent shot prompt. Delivery can follow punctuation and pauses without changing the speaker's identity. Use visuals, sound effects and score to carry a major emotional turn when the narrator is meant to remain measured. A new setting need not add room reverb to an off-screen narrator.

The standard characters have no mouth. Spoken content can be an off-screen narrator or explicitly assigned off-screen dialogue; it must not silently introduce lip animation.

## Fit speech to time

Read the actual line aloud or use a relevant timing estimate before accepting it. Include pauses and actions that need quiet. If the line does not fit, shorten it or redistribute it while retaining the total duration; do not quietly speed up an established speaker. Word-count heuristics differ by language and cannot certify timing.

## Keep the score separate

Describe instrumentation, pulse, density and recording character when a score is requested. Use scene-specific dynamics without replacing the musical identity in every shot. Silence and an environmental-only request override a suggested soundtrack.

Independent generations may still produce different voices or music from identical text. When the user needs stronger control, propose a continuous recorded narration/score assembled in editing or supported reference audio. Do not claim that any speaker, track or provider has been tested unless the current work includes actual listening evidence.
