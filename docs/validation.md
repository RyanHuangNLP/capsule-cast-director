# Validation scope

Recorded 2026-10-26. The release is an instruction-and-tool package for prompt authoring; it is not a tested media-generation service.

## Automated checks

| Check | Observed result |
|---|---|
| Unit suite under Python 3.10 | 29 tests passed |
| Unit suite under Python 3.13 | 29 tests passed |
| Skill metadata validator | Passed |
| Seven visual variants and one 35-second story | All eight JSON packages validate and render |
| Published lantern prompt cards | Match the renderer output from the editable JSON |
| Installation isolation | Installed checker runs outside the repository; existing directories and broken links are not replaced |
| Local skill discovery | A fresh Codex app-server scan found exactly one `directing-capsule-casts`, enabled, with no errors for that skill |

Discovery was tested after installing to the documented user skill directory. This establishes that the local runtime can discover the skill; it is not a screenshot-based check of a particular client's skill menu.

## Independent forward use

An evaluator read the new skill and its supporting resources without the authoring conversation, an expected answer or previous evaluation reports. It completed the [six requests](../tests/forward-requests.md) in a temporary workspace. The inspected outputs are retained here as evidence, not as media examples.

| Request | Inspected output | Observation |
|---|---|---|
| A: two monochrome image prompts | [Output A](trials/A-image-prompts.md) | Both palettes preserve substantial filled limbs, eye contrast, one purple star and matching composition; no video questionnaire |
| B: studio and scenic modern shots | [Output B](trials/B-two-modern-shots.md) | The cast paragraph is identical; red cap/yellow shirt/dark shorts and right-hand envelope are retained; only the worlds and actions change; no speech or music |
| C: prehistoric proposal | [Output C](trials/C-prehistoric-proposal.md) | Three distinct builds and hide outfits, 30 seconds, nine tracked acorns, explicit fiction and full silence; stops at the requested proposal |
| D: cozy four-shot package | [Output D](trials/D-flower-shop-prompts-and-package.md) | 35 seconds split 12/9/8/6 in one flower shop; green apron, white head/trunk and dark limbs retained; one red can travels shelf → left hand → shelf with support before release; environment only |
| E: imagined boatwoman | [Output E](trials/E-fictional-boatwoman.md) | Warm-brown skin, blue-gray robe, red cord, wooden pin and one paddle retained; transparent full-body prompt without invented historical claims |
| F: exact Mandarin speech | [Output F](trials/F-shoe-shop-prompts-and-package.md) | Two nine-second shots in one shoe shop; the two requested sentences remain exact, with one repeated female voice definition and no music; one boot is placed on the table before the hand releases it |

The outputs were read as actual artifacts, rather than treating an evaluator's pass/fail label as sufficient evidence.

The JSON packages in D and F were extracted from the retained outputs and passed through `scripts/package.py check`. Each written shot card was also compared with its JSON: drawing, cast, prop and voice descriptions, setting, start/end locations, actions, sound and spoken lines all match. The checks cover the supplied text and declared state; they do not establish that a generator will follow it.

## Source separation

A comparison covered 65 text/code files in the earlier working tree and 34 in this project, including the retained trials. The included extensions were `.md`, `.py`, `.sh`, `.json`, `.yml` and `.yaml`; Git metadata, caches, distribution archives and standard license files were outside this comparison. It found no byte-identical files and no shared sequence of 18 consecutive English word tokens. This is a bounded text-reuse check, not a legal determination; [the provenance record](../PROVENANCE.md) describes the authoring context.

The earlier working tree's file fingerprint remained unchanged. The nine installed skill files match the new repository, and the release text/code contains no personal absolute filesystem paths.

## What these checks establish

The package checker validates the declared data, not rendered media. Unit tests exercise duration arithmetic, beat coverage, object-state transitions, speaker references, audio modes, standalone prompt expansion and installation behavior. The examples include every visual variant and one multi-shot Mandarin story.

The installer is tested in temporary directories, including existing-target refusal and executing the installed package checker outside the repository. Local Markdown links are checked as part of the suite. No tests depend on another repository, its Git history, old media assets or a provider account.

Actual image appearance, motion, audio and historical accuracy require their own inspection. This release does not claim successful generation or listening tests. GitHub Actions configuration is included; a local run does not prove a hosted workflow has run.
