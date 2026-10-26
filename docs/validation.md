# Validation scope

Reviewed 2026-10-27 for the 0.1.1 update. Initial release checks were recorded on 2026-10-26. The release is an instruction-and-tool package for prompt authoring; it is not a tested media-generation service.

## Automated checks

| Check | Observed result |
|---|---|
| Unit suite under Python 3.10 | 38 tests passed |
| Unit suite under Python 3.13 | 38 tests passed |
| Skill metadata validator | Passed |
| Seven visual variants and one 35-second story | All eight JSON packages validate and render |
| Published lantern prompt cards | Match the renderer output from the editable JSON |
| Installation isolation | Installed checker runs outside the repository; existing directories, broken links and targets created during setup are not replaced; failed/interrupted copies can be retried; recursive destinations are rejected |
| Local skill discovery | A fresh Codex app-server scan found exactly one `directing-capsule-casts`, enabled, with no errors for that skill |

Discovery was tested after installing to the documented user skill directory. This establishes that the local runtime can discover the skill; it is not a screenshot-based check of a particular client's skill menu.

## Independent forward use

An evaluator read the new skill and its supporting resources without the authoring conversation, an expected answer or previous evaluation reports. It completed [requests A–F](../tests/forward-requests.md) in a temporary workspace for the initial release. The inspected outputs are retained here as evidence, not as media examples.

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

A separate evaluator used the updated skill for requests G and H without prior answers or review findings. Both complete responses were inspected. A temporary JSON-file link and terminal blank lines were removed from the retained copies; the prompts, package and proposal text were preserved.

| Request | Inspected output | Observation |
|---|---|---|
| G: cropped props in 4:5 | [Output G](trials/G-cropped-props.md) | Two six-second silent shots retain one blue-cardigan character, a key in the right hand and a red book on its shelf. The close-up expands only the key's appearance while retaining both objects in the ledger. The embedded JSON matches the separately checked package, and the written cards equal the renderer output |
| H: fixed words, pace and duration | [Output H](trials/H-fixed-voice-timing.md) | All 80 supplied Chinese characters are preserved. The response identifies that about 3 characters/second requires about 26.7 seconds before pauses, supplies a separately labeled five-second visual proposal, and does not claim a complete five-second narration is feasible |

## Follow-up corrections

| Observed issue | Change and evidence |
|---|---|
| A valid `4:5` frame was rejected | Positive integer/decimal ratios now validate; invalid and zero-valued ratios still fail. Trial G uses `4:5` successfully |
| Accepted `12.3456789` seconds was exported as `12.3457` | Export preserves the numeric value for both shot lengths and beat boundaries; a round-trip regression checks both |
| Every registered object's visual description appeared in every shot | Optional `visible_props` separates framing from continuity. Hidden objects still need valid states and cannot teleport; earlier packages retain their default behavior |
| A failed copy left an incomplete skill that blocked retry | A failed copy or keyboard interrupt removes the newly created target. Existing installations are preserved, including a target created during setup. Destinations inside the source, including symlink aliases, are rejected before copying |
| Sound guidance allowed shortening an overlong line without distinguishing fixed wording | Verbatim speech must remain intact; timing conflicts are stated explicitly. Trial H exercises the conflict without changing the words or pretending they fit |

## Source separation

At the initial 0.1.0 release, a comparison covered 65 text/code files in the earlier working tree and 34 in this project, including the then-retained trials. The included extensions were `.md`, `.py`, `.sh`, `.json`, `.yml` and `.yaml`; Git metadata, caches, distribution archives and standard license files were outside this comparison. It found no byte-identical files and no shared sequence of 18 consecutive English word tokens. This is a bounded text-reuse check, not a legal determination; [the provenance record](../PROVENANCE.md) describes the authoring context.

The earlier working tree's file fingerprint remained unchanged. The nine installed skill files match the new repository, and the release text/code contains no personal absolute filesystem paths.

## What these checks establish

The package checker validates the declared data, not rendered media. Unit tests exercise duration arithmetic, beat coverage, object-state transitions, speaker references, audio modes, standalone prompt expansion and installation behavior. The examples include every visual variant and one multi-shot Mandarin story.

The installer is tested in temporary directories, including existing-target refusal and executing the installed package checker outside the repository. Local Markdown links are checked as part of the suite. No tests depend on another repository, its Git history, old media assets or a provider account.

Actual image appearance, motion, audio and historical accuracy require their own inspection. This release does not claim successful generation or listening tests. GitHub Actions configuration is included; a local run does not prove a hosted workflow has run.
