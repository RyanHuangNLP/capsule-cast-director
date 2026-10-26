import importlib.util
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/directing-capsule-casts"
spec = importlib.util.spec_from_file_location("capsule_install", ROOT / "tools/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class DistributionTests(unittest.TestCase):
    def test_markdown_file_links_resolve(self):
        checked = 0
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                target = target.strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-z][a-z0-9+.-]*:", target):
                    continue
                with self.subTest(file=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue((path.parent / unquote(target)).exists())
                checked += 1
        self.assertGreater(checked, 20)

    def test_skill_contains_its_license(self):
        self.assertEqual((ROOT / "LICENSE").read_bytes(), (SKILL / "LICENSE").read_bytes())

    def test_install_is_self_contained_and_executable(self):
        with tempfile.TemporaryDirectory() as directory:
            target = installer.install(directory)
            self.assertTrue((target / "SKILL.md").is_file())
            self.assertTrue((target / "LICENSE").is_file())
            for source in SKILL.rglob("*"):
                if source.is_file() and "__pycache__" not in source.parts:
                    self.assertEqual(source.read_bytes(), (target / source.relative_to(SKILL)).read_bytes())
            result = subprocess.run([
                sys.executable, str(target / "scripts/package.py"), "check",
                str(ROOT / "examples/lantern-home.json"),
            ], cwd=directory, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("4 shots, 35s", result.stdout)

    def test_install_does_not_replace_an_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / installer.NAME
            target.mkdir()
            marker = target / "user-file.txt"
            marker.write_text("Keep this edited file.")
            with self.assertRaises(FileExistsError):
                installer.install(directory)
            self.assertEqual(marker.read_text(), "Keep this edited file.")
            self.assertEqual(list(target.iterdir()), [marker])

    def test_install_does_not_replace_a_broken_link(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / installer.NAME
            target.symlink_to(Path(directory) / "not-present")
            with self.assertRaises(FileExistsError):
                installer.install(directory)
            self.assertTrue(target.is_symlink())

    def test_failed_or_interrupted_copy_can_be_retried(self):
        for error in (OSError, KeyboardInterrupt):
            with self.subTest(error=error.__name__), tempfile.TemporaryDirectory() as directory:
                def fail_copy(source, target, **kwargs):
                    (Path(target) / "SKILL.md").write_text("Incomplete copy.")
                    raise error("Simulated interruption")

                with patch.object(installer.shutil, "copytree", side_effect=fail_copy):
                    with self.assertRaises(error):
                        installer.install(directory)
                self.assertFalse((Path(directory) / installer.NAME).exists())
                target = installer.install(directory)
                self.assertEqual((target / "SKILL.md").read_bytes(), (SKILL / "SKILL.md").read_bytes())

    def test_install_rejects_copying_source_into_itself(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("Source instructions.")
            (source / "LICENSE").write_text("Source license.")
            alias = Path(directory) / "alias"
            alias.symlink_to(source, target_is_directory=True)
            with patch.object(installer, "SOURCE", source):
                for destination in (source, source / "nested", alias / "nested"):
                    with self.subTest(destination=destination):
                        with self.assertRaisesRegex(ValueError, "outside the source"):
                            installer.install(destination)
            self.assertEqual(sorted(path.name for path in source.iterdir()), ["LICENSE", "SKILL.md"])

    def test_target_created_during_setup_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory).resolve() / "skills"
            target = destination / installer.NAME
            original_mkdir = Path.mkdir

            def raced_mkdir(path, *args, **kwargs):
                original_mkdir(path, *args, **kwargs)
                if path == destination:
                    original_mkdir(target)
                    (target / "user-file.txt").write_text("Created by another installer.")

            with patch.object(Path, "mkdir", raced_mkdir):
                with self.assertRaises(FileExistsError):
                    installer.install(destination)
            self.assertEqual([path.name for path in target.iterdir()], ["user-file.txt"])


if __name__ == "__main__":
    unittest.main()
