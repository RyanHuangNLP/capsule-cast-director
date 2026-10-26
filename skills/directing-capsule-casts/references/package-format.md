# Optional shot package, version 1

This format helps check time and declared continuity and expands shared descriptions into independent prompts. It does not select a model, generate media, estimate speech duration or prove physical plausibility. A prose-only request does not need conversion to JSON.

Run with Python 3.10 or later. No third-party Python packages are required:

```sh
python3 scripts/package.py check /path/to/story.json
python3 scripts/package.py render /path/to/story.json
```

The commands are relative to the skill directory. Rendering writes Markdown to standard output. It makes no network calls and does not modify the package. Redirect the output to a new file when needed.

## Root object

| Field | Value |
|---|---|
| `schema` | Integer `1` |
| `title`, `context` | Title and factual/fictional framing, both nonempty text |
| `look` | One look key from [looks.md](looks.md) |
| `aspect` | Positive width:height ratio, such as `16:9`, `4:5`, `21:9` or `2.39:1` |
| `duration` | Positive finite total seconds |
| `drawing` | Complete project drawing description |
| `cast` | Object mapping each character ID to a complete appearance description |
| `props` | Object mapping each physical item ID to its appearance; use distinct IDs for distinct items |
| `voices` | Object mapping speaker IDs to complete voice descriptions; empty outside spoken mode |
| `audio` | Object with `mode` and `music`; music is a description or an empty string |
| `exclude` | Relevant negative directions, without contradicting chosen clothes, colors or staging |
| `shots` | Nonempty ordered array of shot objects |

Identifiers start with a lowercase letter and then use lowercase letters, digits, hyphens or underscores. `set` is reserved and cannot be a cast ID. All fields are required except a shot's `visible_props`; empty arrays/objects/text are used only as described here. Unknown fields are rejected to catch misspellings. Ratio components may be integers or decimals, but must be greater than zero.

Audio modes are `silent`, `environment`, `scored` and `spoken`. Silent mode requires empty music, effects, voices and lines. Environment mode allows effects only. Scored mode requires music and forbids speech. Spoken mode requires at least one assigned line in the story and permits optional music/effects; a particular shot may contain a pause with no lines.

## Each shot

| Field | Value |
|---|---|
| `id`, `seconds`, `setting` | Unique shot ID, positive duration and complete setting description |
| `cast` | Array of visible character IDs; no duplicates |
| `visible_props` (optional) | Array of prop IDs visible in this shot; no duplicates. Omit to show all registered props, or use `[]` to show none |
| `start`, `end` | State of every tracked prop before/after the shot |
| `beats` | Array of `{ "from": 0, "to": 3, "action": "..." }` objects |
| `transition` | `opening` for the first shot only, otherwise `continuous` or `cut` |
| `offscreen` | Object mapping changed incoming prop IDs to explicit explanations, otherwise `{}` |
| `lines` | Array of `{ "speaker": "reader", "text": "Exact spoken words." }`, otherwise `[]` |
| `sound` | Shot-specific effects description, or `""` |

Beats must cover the shot from zero to its end without overlaps or gaps. Shot lengths must sum to the requested duration. Decimal seconds are accepted with a one-microsecond arithmetic tolerance. This tolerance is not a claim about frame accuracy.

A prop state is `{ "holder": "character-id", "place": "left hand, against the chest" }` or `{ "holder": "set", "place": "on the low stone bench" }`. Every registered prop appears once in each state. An object outside the camera view still has a physical holder/place; record that instead of deleting it. Use `visible_props` to control framing separately: a hand close-up may show a key while a book stays out of frame on its shelf. The ledger retains both items, but only the key's appearance is expanded into that shot. During a two-hand transfer, the action text describes shared contact; the opening/closing ledger records the settled states.

The next `start` must equal the previous `end`. If time or place skips a change, use `cut` and give exactly one `offscreen` explanation for each changed prop. An off-screen note does not make an implausible action valid; a human or agent must review it. For uninterrupted action, no off-screen state changes are allowed.

The renderer repeats the drawing paragraph, visible character and object definitions, and the applicable speaker definitions. Hidden objects are labeled as continuity records to keep outside the frame. It retains exact lines and the numeric precision supplied for timings. Existing packages without `visible_props` retain their original behavior. Shared data prevents accidental abbreviation; contradictory natural language still needs review.

For executable examples, see the repository's `examples/` directory. The installed skill remains usable without those examples.
