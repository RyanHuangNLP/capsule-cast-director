#!/usr/bin/env python3
"""Check a shot ledger and expand its shared definitions. No media API is called."""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from decimal import Decimal

LOOKS = (
    "mono-light", "mono-dark", "modern-studio", "modern-story",
    "prehistoric", "cozy", "heritage",
)
MODES = ("silent", "environment", "scored", "spoken")


class PackageError(ValueError):
    """An invalid package, with a location suitable for a human-readable error."""


def require(condition, where, message):
    if not condition:
        raise PackageError(f"{where}: {message}")


def fields(value, where, required, optional=()):
    require(isinstance(value, dict), where, "expected an object")
    missing = set(required) - value.keys()
    extra = value.keys() - set(required) - set(optional)
    require(not missing, where, f"missing fields: {', '.join(sorted(missing))}")
    require(not extra, where, f"unknown fields: {', '.join(sorted(extra))}")


def text(value, where, empty=False):
    require(isinstance(value, str), where, "expected text")
    require(empty or bool(value.strip()), where, "text must not be empty")


def number(value, where, zero=False):
    require(type(value) in (int, float), where, "expected a number, not a boolean")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    require(finite, where, "number must be finite")
    require(value >= 0 if zero else value > 0, where, "number is outside the allowed range")


def close(left, right):
    return math.isclose(left, right, rel_tol=0, abs_tol=0.000001)


def identifier(value, where):
    text(value, where)
    require(re.fullmatch(r"[a-z][a-z0-9_-]*", value) is not None,
            where, "use a lowercase identifier starting with a letter")


def register(value, where):
    require(isinstance(value, dict), where, "expected an identifier-to-description object")
    for key, description in value.items():
        identifier(key, where)
        text(description, f"{where}.{key}")


def selection(value, where, known, kind):
    require(isinstance(value, list), where, "expected a list")
    require(all(isinstance(key, str) for key in value), where, f"{kind} identifiers must be text")
    require(len(value) == len(set(value)), where, f"{kind} identifier appears twice")
    require(all(key in known for key in value), where, f"unknown {kind} identifier")


def state(value, where, props, cast):
    fields(value, where, props)
    for prop, placement in value.items():
        location = f"{where}.{prop}"
        fields(placement, location, ("holder", "place"))
        text(placement["holder"], f"{location}.holder")
        require(placement["holder"] in cast or placement["holder"] == "set",
                location, "holder must be a cast identifier or 'set'")
        text(placement["place"], f"{location}.place")


def validate(data):
    """Validate declared timing, references and transitions; return the input."""
    fields(data, "package", (
        "schema", "title", "context", "look", "aspect", "duration", "drawing",
        "cast", "props", "voices", "audio", "exclude", "shots",
    ))
    require(type(data["schema"]) is int and data["schema"] == 1,
            "schema", "supported version is 1")
    for key in ("title", "context", "drawing", "exclude", "look", "aspect"):
        text(data[key], key)
    require(data["look"] in LOOKS, "look", f"choose one of {', '.join(LOOKS)}")
    ratio = re.fullmatch(r"\s*([0-9]+(?:\.[0-9]+)?)\s*:\s*([0-9]+(?:\.[0-9]+)?)\s*", data["aspect"])
    require(ratio is not None, "aspect", "use a width:height ratio, such as 4:5 or 2.39:1")
    require(all(Decimal(part) > 0 for part in ratio.groups()), "aspect", "both ratio values must be positive")
    number(data["duration"], "duration")
    for key in ("cast", "props", "voices"):
        register(data[key], key)
    require("set" not in data["cast"], "cast", "'set' is reserved for scenery support")

    audio = data["audio"]
    fields(audio, "audio", ("mode", "music"))
    text(audio["mode"], "audio.mode")
    require(audio["mode"] in MODES, "audio.mode", f"choose one of {', '.join(MODES)}")
    text(audio["music"], "audio.music", empty=True)
    if audio["mode"] in ("silent", "environment"):
        require(not audio["music"].strip(), "audio.music", "this mode excludes music")
    if audio["mode"] == "scored":
        require(bool(audio["music"].strip()), "audio.music", "scored mode needs a score description")
    if audio["mode"] != "spoken":
        require(not data["voices"], "voices", "non-spoken modes have no speakers")

    shots = data["shots"]
    require(isinstance(shots, list) and bool(shots), "shots", "expected a nonempty list")
    ids = set()
    previous = None
    has_speech = False
    for index, shot in enumerate(shots):
        where = f"shots[{index}]"
        fields(shot, where, (
            "id", "seconds", "setting", "cast", "start", "beats", "end",
            "transition", "offscreen", "lines", "sound",
        ), optional=("visible_props",))
        identifier(shot["id"], f"{where}.id")
        require(shot["id"] not in ids, where, "duplicate shot identifier")
        ids.add(shot["id"])
        number(shot["seconds"], f"{where}.seconds")
        text(shot["setting"], f"{where}.setting")
        selection(shot["cast"], f"{where}.cast", data["cast"], "cast")
        if "visible_props" in shot:
            selection(shot["visible_props"], f"{where}.visible_props", data["props"], "prop")
        state(shot["start"], f"{where}.start", data["props"], data["cast"])
        state(shot["end"], f"{where}.end", data["props"], data["cast"])

        transition = shot["transition"]
        require(transition in ("opening", "continuous", "cut"), where, "unknown transition")
        require((index == 0) == (transition == "opening"), where,
                "only the first shot uses the opening transition")
        offscreen = shot["offscreen"]
        register(offscreen, f"{where}.offscreen")
        require(set(offscreen) <= set(data["props"]), where, "offscreen note names an unknown prop")
        changed = set() if previous is None else {
            prop for prop in data["props"] if previous[prop] != shot["start"][prop]
        }
        require(changed == set(offscreen), where,
                "each changed incoming prop state needs exactly one offscreen explanation")
        require(not changed or transition == "cut", where,
                "continuous action cannot skip an object-state change")

        beats = shot["beats"]
        require(isinstance(beats, list) and bool(beats), f"{where}.beats", "expected a nonempty list")
        cursor = 0
        for beat_index, beat in enumerate(beats):
            at = f"{where}.beats[{beat_index}]"
            fields(beat, at, ("from", "to", "action"))
            number(beat["from"], f"{at}.from", zero=True)
            number(beat["to"], f"{at}.to")
            text(beat["action"], f"{at}.action")
            require(close(beat["from"], cursor), at, "timeline has a gap or overlap")
            require(beat["to"] > beat["from"], at, "beat must have positive duration")
            cursor = beat["to"]
        require(close(cursor, shot["seconds"]), where, "beats must end at the shot duration")

        lines = shot["lines"]
        require(isinstance(lines, list), f"{where}.lines", "expected a list")
        require(not lines or audio["mode"] == "spoken", where, "this audio mode excludes speech")
        for line_index, line in enumerate(lines):
            at = f"{where}.lines[{line_index}]"
            fields(line, at, ("speaker", "text"))
            text(line["speaker"], f"{at}.speaker")
            require(line["speaker"] in data["voices"], at, "speaker has no voice description")
            text(line["text"], f"{at}.text")
            has_speech = True
        text(shot["sound"], f"{where}.sound", empty=True)
        if audio["mode"] == "silent":
            require(not shot["sound"].strip(), where, "silent mode excludes sound effects")
        previous = shot["end"]

    try:
        total = math.fsum(shot["seconds"] for shot in shots)
    except OverflowError:
        raise PackageError("duration: summed shot lengths are too large") from None
    require(close(total, data["duration"]), "duration",
            f"shot lengths sum to {total}, expected {data['duration']}")
    require(audio["mode"] != "spoken" or has_speech, "audio.mode",
            "spoken mode needs at least one assigned line")
    return data


def placements(value):
    if not value:
        return "No tracked objects."
    return "; ".join(
        f"{key}: supported by {place['holder']}, {place['place']}"
        for key, place in value.items()
    )


def render(data):
    """Return independent Markdown shot cards with expanded shared definitions."""
    validate(data)
    cards = [f"# {data['title']}", "", data["context"], ""]
    for shot in data["shots"]:
        content = [
            f"Length {shot['seconds']} seconds. Frame {data['aspect']}. Look: {data['look']}.",
            f"Story context: {data['context']}",
            f"Drawing: {data['drawing']}", f"Setting: {shot['setting']}",
        ]
        content.extend(f"Person {role}: {data['cast'][role]}" for role in shot["cast"])
        visible_props = shot.get("visible_props", list(data["props"]))
        content.extend(f"Object {key}: {data['props'][key]}" for key in visible_props)
        hidden_props = [key for key in data["props"] if key not in visible_props]
        if hidden_props:
            content.append("Tracked objects outside the frame (continuity only; do not depict): "
                           + ", ".join(hidden_props) + ".")
        content.append(f"Opening ledger: {placements(shot['start'])}")
        content.append(f"Incoming transition: {shot['transition']}.")
        content.extend(f"Off-screen change for {key}: {value}" for key, value in shot["offscreen"].items())
        content.extend(
            f"{beat['from']}–{beat['to']}s: {beat['action']}" for beat in shot["beats"]
        )
        used_voices = dict.fromkeys(line["speaker"] for line in shot["lines"])
        content.extend(f"Voice {key}: {data['voices'][key]}" for key in used_voices)
        content.extend(
            f"Exact speech ({line['speaker']}): {line['text']}" for line in shot["lines"]
        )
        if not shot["lines"]:
            content.append("Speech: none in this shot.")
        if data["audio"]["mode"] == "silent":
            content.append("Audio: fully silent; no voice, music or effects.")
        else:
            content.append(f"Music: {data['audio']['music'].strip() or 'none' }.")
            content.append(f"Effects: {shot['sound'].strip() or 'none'}.")
        content.append(f"Closing ledger: {placements(shot['end'])}")
        content.append(f"Exclude: {data['exclude']}")
        body = "\n\n".join(content)
        longest = max((len(run) for run in re.findall(r"`+", body)), default=0)
        fence = "`" * max(3, longest + 1)
        cards.extend([f"## {shot['id']}", "", fence + "text", body, fence, ""])
    return "\n".join(cards)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PackageError(f"JSON: repeated key {key!r}")
        result[key] = value
    return result


def nonfinite_constant(value):
    raise PackageError(f"JSON: {value} is not a finite number")


def read_package(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object, parse_constant=nonfinite_constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "render"))
    parser.add_argument("package", type=Path)
    args = parser.parse_args(argv)
    try:
        data = read_package(args.package)
        validate(data)
        if args.command == "render":
            print(render(data), end="")
        else:
            print(f"OK: {len(data['shots'])} shots, {data['duration']}s, {data['look']}")
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"{args.package}: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
