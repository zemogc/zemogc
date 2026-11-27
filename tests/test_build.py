import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from build_assets import ASSETS, build_all, load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load()
        cls.files = build_all(cls.data)

    def test_every_asset_has_both_themes(self):
        names = set(self.files)
        for name in names:
            if name.endswith("-dark.svg"):
                self.assertIn(name.replace("-dark.svg", "-light.svg"), names)
        self.assertEqual(len(names), 2 * (5 + len(self.data["contact"])))

    def test_svgs_are_well_formed(self):
        for name, svg in self.files.items():
            with self.subTest(name=name):
                self.assertEqual(ET.fromstring(svg).tag, "{http://www.w3.org/2000/svg}svg")

    def test_build_is_deterministic(self):
        self.assertEqual(self.files, build_all(self.data))

    def test_committed_assets_match_content(self):
        for name, svg in self.files.items():
            with self.subTest(name=name):
                committed = (ASSETS / name).read_bytes().decode("utf-8")
                self.assertEqual(committed, svg, "ejecuta: python3 scripts/build_assets.py")


class ContentTest(unittest.TestCase):
    def test_required_sections(self):
        data = load()
        for key in ("login", "identity", "system", "products", "contact", "ticker"):
            self.assertIn(key, data)
        self.assertTrue(data["products"])

    def test_contact_slugs_are_unique(self):
        slugs = [c["slug"] for c in load()["contact"]]
        self.assertEqual(len(slugs), len(set(slugs)))


if __name__ == "__main__":
    unittest.main()
