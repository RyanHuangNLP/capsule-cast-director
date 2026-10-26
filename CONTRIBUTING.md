# Contributing

Keep changes centered on character design, shot planning or the small package tools. Include a realistic request that demonstrates a workflow improvement, and explain which output should change. Prefer a focused correction over adding universal rules for one story.

Run `python3 -m unittest discover -s tests -v` from the repository root. For a change to the package format, update its reference, affected examples and behavioral tests together. Preserve exact spoken text and user choices when changing only the rendering mechanics.

For instruction changes, try the skill against a fresh request without showing the evaluator the intended answer. Store the actual output and distinguish what was observed from what remains untested. A text test is not evidence of successful image or video generation.

Keep examples original and label fictional historical scenes. Do not add another creator's prompt, screenshot, sample film or code without checking its terms and including required attribution. The contribution must be compatible with this repository's MIT release; record third-party material in [PROVENANCE.md](PROVENANCE.md).

Do not commit account credentials, personal paths, private references, generated caches or paid-provider claims that have not been verified. Discussion and contributions should be respectful and specific.
