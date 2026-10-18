"""Offline checks for the preserved Mixly project sources."""
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = (
    "src/standalone/electrostatic-detection.mix",
    "src/standalone/electrostatic-detection.mil",
    "src/generation-2/transmitter.mix",
    "src/generation-2/receiver.mix",
)
CJK = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")


def decode(text):
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m[1], 16)), text.replace('\\"', '"'))


class SourceTests(unittest.TestCase):
    def test_workspaces(self):
        for name in SOURCES:
            with self.subTest(source=name):
                text = decode((ROOT / name).read_text(encoding="utf-8-sig"))
                self.assertIsNone(CJK.search(text))
                root = ET.fromstring(text)
                self.assertEqual(root.tag.rsplit("}", 1)[-1], "xml")
                blocks = [n for n in root.iter() if n.tag.rsplit("}", 1)[-1] == "block"]
                self.assertGreater(len(blocks), 50)
                definitions, calls = set(), set()
                for block in blocks:
                    kind = block.get("type", "")
                    if kind.startswith("procedures_def"):
                        definitions.update(n.text for n in block if n.get("name") == "NAME")
                    if kind.startswith("procedures_call"):
                        calls.update(n.get("name") for n in block if n.tag.rsplit("}", 1)[-1] == "mutation")
                self.assertTrue(calls <= definitions, calls - definitions)
                if name.endswith(".mix"):
                    self.assertEqual(root.get("version"), "1.2.0")
                    self.assertEqual(root.get("board"), "Arduino Nano[atmega328old]")
                else:
                    self.assertEqual(root.get("board"), "mylib")
                    self.assertTrue(text.startswith('<!-- lib="" -->'))

    def test_infrared_protocol(self):
        for role, kind in (("transmitter", "ir_send_nec"), ("receiver", "ir_recv")):
            with self.subTest(role=role):
                text = decode((ROOT / f"src/generation-2/{role}.mix").read_text())
                self.assertIn(f'type="{kind}"', text)
                self.assertIn(">33333333<", text)

    def test_english_paths_and_text(self):
        files = [ROOT / p for p in (*SOURCES, "README.md", "AGENTS.md", ".gitignore", "LICENSE")]
        files.extend((ROOT / "tests").glob("*.py"))
        for path in files:
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIsNone(CJK.search(path.relative_to(ROOT).as_posix()))
                text = path.read_text(encoding="utf-8-sig")
                if path.suffix in (".mix", ".mil"):
                    text = decode(text)
                self.assertIsNone(CJK.search(text))


if __name__ == "__main__":
    unittest.main()
