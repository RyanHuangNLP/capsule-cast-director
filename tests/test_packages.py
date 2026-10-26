import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/directing-capsule-casts/scripts/package.py"
spec = importlib.util.spec_from_file_location("capsule_package", SCRIPT)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.story = package.read_package(ROOT / "examples/lantern-home.json")

    def reject(self, part):
        with self.assertRaisesRegex(package.PackageError, part):
            package.validate(self.story)

    def test_examples_cover_every_look_and_render_independent_cards(self):
        looks = set()
        for path in sorted((ROOT / "examples").glob("*.json")):
            with self.subTest(path=path.name):
                data = package.read_package(path)
                package.validate(data)
                looks.add(data["look"])
                output = package.render(data)
                for shot, card in zip(data["shots"], output.split("\n## ")[1:]):
                    self.assertIn(data["drawing"], card)
                    for role in shot["cast"]:
                        self.assertIn(data["cast"][role], card)
                    for line in shot["lines"]:
                        self.assertIn(line["text"], card)
                        self.assertIn(data["voices"][line["speaker"]], card)
                    for item in data["props"].values():
                        self.assertIn(item, card)
                self.assertEqual(len(data["shots"]), len(output.split("\n## ")) - 1)
        self.assertEqual(looks, set(package.LOOKS))

    def test_requested_nonmultiple_duration_is_preserved(self):
        package.validate(self.story)
        self.assertEqual([s["seconds"] for s in self.story["shots"]], [12, 9, 8, 6])
        self.assertEqual(self.story["duration"], 35)
        self.story["duration"] = 30
        self.reject("shot lengths sum")

    def test_fractional_seconds_use_arithmetic_tolerance(self):
        one = copy.deepcopy(self.story["shots"][0])
        two = copy.deepcopy(one)
        one.update(seconds=0.1, beats=[{"from": 0, "to": 0.1, "action": "Hold."}])
        two.update(id="hold", seconds=0.2, transition="continuous", start=one["end"],
                   beats=[{"from": 0, "to": 0.2, "action": "Hold."}])
        self.story.update(duration=0.3, shots=[one, two])
        package.validate(self.story)

    def test_gaps_and_overlaps_fail(self):
        for value in (3.9, 4.1):
            with self.subTest(value=value):
                self.story["shots"][0]["beats"][1]["from"] = value
                self.reject("gap or overlap")

    def test_incomplete_beat_coverage_fails(self):
        self.story["shots"][0]["beats"][-1]["to"] = 11
        self.reject("beats must end")

    def test_zero_length_beat_fails(self):
        self.story["shots"][0]["beats"][1]["to"] = 4
        self.reject("positive duration")

    def test_boolean_negative_and_nonfinite_durations_fail(self):
        for value in (True, 0, -1, float("nan"), float("inf"), 10 ** 400):
            with self.subTest(value=str(value)[:20]):
                self.story["duration"] = value
                self.reject("duration")

    def test_prop_does_not_teleport_between_shots(self):
        self.story["shots"][1]["start"]["lantern"]["holder"] = "bo"
        self.reject("offscreen explanation")

    def test_explained_change_requires_a_cut(self):
        incoming = self.story["shots"][1]
        incoming["start"]["lantern"]["holder"] = "bo"
        incoming["offscreen"] = {"lantern": "During a time skip, Bo received the lantern."}
        self.reject("continuous action")
        incoming["transition"] = "cut"
        package.validate(self.story)

    def test_unneeded_offscreen_note_fails(self):
        self.story["shots"][1]["offscreen"] = {"lantern": "Nothing changed."}
        self.reject("offscreen explanation")

    def test_missing_prop_state_fails(self):
        self.story["shots"][2]["start"] = {}
        self.reject("missing fields: lantern")

    def test_unknown_holder_fails(self):
        self.story["shots"][0]["start"]["lantern"]["holder"] = "someone"
        self.reject("holder must be")

    def test_duplicate_shot_and_cast_ids_fail(self):
        self.story["shots"][1]["id"] = self.story["shots"][0]["id"]
        self.reject("duplicate shot")
        self.story["shots"][1]["id"] = "next"
        self.story["shots"][0]["cast"] = ["jun", "jun"]
        self.reject("appears twice")

    def test_undefined_cast_and_voice_fail(self):
        self.story["shots"][0]["cast"] = ["stranger"]
        self.reject("unknown cast")
        self.story["shots"][0]["cast"] = ["jun"]
        self.story["shots"][0]["lines"][0]["speaker"] = "stranger"
        self.reject("no voice description")

    def test_mode_does_not_leak_music_or_speech(self):
        self.story["audio"]["mode"] = "environment"
        self.reject("excludes music")
        self.story["audio"]["music"] = ""
        self.reject("non-spoken modes")
        self.story["voices"] = {}
        self.reject("excludes speech")

    def test_silent_mode_excludes_effects(self):
        self.story["audio"] = {"mode": "silent", "music": ""}
        self.story["voices"] = {}
        for shot in self.story["shots"]:
            shot["lines"] = []
        self.reject("excludes sound effects")
        for shot in self.story["shots"]:
            shot["sound"] = ""
        output = package.render(self.story)
        self.assertEqual(output.count("fully silent; no voice, music or effects"), 4)
        self.assertNotIn("Voice reader:", output)

    def test_spoken_mode_needs_actual_speech(self):
        for shot in self.story["shots"]:
            shot["lines"] = []
        self.reject("at least one assigned line")

    def test_scored_mode_has_music_without_speech(self):
        self.story["audio"]["mode"] = "scored"
        self.story["voices"] = {}
        for shot in self.story["shots"]:
            shot["lines"] = []
        package.validate(self.story)
        self.story["audio"]["music"] = ""
        self.reject("needs a score description")

    def test_published_lantern_cards_match_the_editable_source(self):
        expected = package.render(self.story)
        self.assertEqual(expected, (ROOT / "examples/lantern-home.md").read_text(encoding="utf-8"))

    def test_typo_and_reserved_id_are_rejected(self):
        self.story["duraton"] = 35
        self.reject("unknown fields: duraton")
        del self.story["duraton"]
        self.story["cast"]["set"] = "A person."
        self.reject("reserved")

    def test_backticks_in_input_cannot_close_the_prompt_fence(self):
        self.story["context"] = "A fictional scene with the literal sequence ``` in a note."
        output = package.render(self.story)
        self.assertEqual(output.count("````text"), 4)
        self.assertEqual(output.count("\n````\n"), 4)

    def test_json_duplicate_keys_and_nonfinite_constants_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            for value in ('{"title":"a","title":"b"}', '{"duration":NaN}'):
                path.write_text(value)
                with self.assertRaises(package.PackageError):
                    package.read_package(path)

    def test_cli_runs_from_an_unrelated_directory_without_mutating_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "story.json"
            path.write_text(json.dumps(self.story, ensure_ascii=False), encoding="utf-8")
            before = path.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), "render", str(path)],
                                    cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            for shot in self.story["shots"]:
                for line in shot["lines"]:
                    self.assertIn(line["text"], result.stdout)
            self.assertEqual(before, path.read_bytes())

    def test_cli_invalid_input_returns_failure_without_partial_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "story.json"
            self.story["duration"] = 99
            path.write_text(json.dumps(self.story), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "render", str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(result.stdout, "")
            self.assertIn("shot lengths sum", result.stderr)
            self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
