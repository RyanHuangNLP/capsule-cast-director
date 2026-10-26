# Capsule Cast Director

[简体中文](README.zh-CN.md)

A portable agent skill for designing rounded cartoon casts and planning short animated stories. Five visual families share solid bodies, substantial limbs and capsule-shaped eyes while keeping their own clothes, colors and environments.

The deliverables are character briefs, image prompts, storyboards and independent shot prompts. Generation uses whichever tools the host actually provides. This repository contains no image/video service integration and no generated-media gallery.

## Five looks, seven variants

| Family | Variants | What stays recognizable |
|---|---|---|
| Classic monochrome | Light / dark | Black-and-white people, flat canvas and simple graphic props |
| Modern | Studio / scenic | Red cap, yellow tee, charcoal shorts; either cyan studio UI or colorful locations |
| Prehistoric | One family | Hide clothing, dark hair/limbs, earthy worlds and optional deadpan humor |
| Cozy | One family | White head/trunk, dark limbs, requested everyday outfits and warm ordinary spaces |
| Heritage | One family | Story-specific skin tones, period clothing, tools and architecture |

See the [drawing guide](skills/directing-capsule-casts/references/looks.md) and [seven complete visual prompts](examples/visual-prompts.md). User-specified clothes and colors take precedence over defaults.

## Install and use

Download this repository and open a terminal in its root. The helper requires Python 3.10+ and uses only the standard library:

```sh
python3 tools/install.py
```

This copies the complete skill, including its license, to `~/.agents/skills/directing-capsule-casts`. It refuses to overwrite an existing installation. For a client configured to read a different skill directory, use `--dest /path/to/skills`. See [Codex's skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills); reload the client if the new skill does not appear.

Invoke the skill in a supporting agent, for example:

```text
Use $directing-capsule-casts to write final prompts for a 35-second,
9:16 cozy story in one bakery. The lead wears a green apron and carries
one cream paper bag. Use environmental sound only. Deliver directly.
```

For an instruction-only host, point it at [SKILL.md](skills/directing-capsule-casts/SKILL.md). Python is optional for using the written workflow; it is required only for the helpers. Character-only requests do not trigger a video setup questionnaire.

## A package you can check

The optional JSON format stores shared appearance and voice definitions once, plus shot timings and an object ledger. The renderer expands the definitions into every applicable prompt.

```sh
python3 skills/directing-capsule-casts/scripts/package.py check examples/lantern-home.json
python3 skills/directing-capsule-casts/scripts/package.py render examples/lantern-home.json
```

The [35-second lantern story](examples/lantern-home.json) includes Mandarin narration, two characters, an object transfer and a close-up. Read its [expanded shot prompts](examples/lantern-home.md) without running Python. Its four shot lengths are 12, 9, 8 and 6 seconds. These are editorial targets, not claims about any provider's generation limits. Each look also has a separate ten-second example in [examples/](examples/).

The checker rejects duration mismatches, gaps/overlaps, unresolved character or speaker IDs, incompatible audio modes and unexplained incoming prop-state changes. It cannot judge anatomy, hand contact, factual accuracy, speech pacing or rendered quality. See the [format specification](skills/directing-capsule-casts/references/package-format.md).

## Verify and contribute

```sh
python3 -m unittest discover -s tests -v
```

Tests use temporary directories and make no media or network calls. GitHub Actions runs the same suite on pushes and pull requests. The [validation record](docs/validation.md) distinguishes local checks, independent text trials and untested media output. Contribution guidance is in [CONTRIBUTING.md](CONTRIBUTING.md).

## License and provenance

The newly authored project is released under [MIT](LICENSE), copyright 2026 Capsule Cast Director contributors. It has a fresh implementation, new examples and its own identity. [PROVENANCE.md](PROVENANCE.md) explains the earlier research and visual influences, what is absent from this distribution, and the boundaries for third-party material. No association with xAI or the referenced creators is implied.
