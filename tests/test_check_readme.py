import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_readme  # noqa: E402
from build_assets import load  # noqa: E402


class ReadmeTest(unittest.TestCase):
    def test_all_referenced_assets_exist(self):
        self.assertEqual(check_readme.main(), 0)

    def test_every_image_has_alt_text(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for tag in re.findall(r"<img[^>]*>", readme):
            self.assertRegex(tag, r'alt="[^"]+"')

    def test_text_summary_covers_content(self):
        """El resumen en texto debe mencionar cada producto y cada enlace de contacto."""
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        data = load()
        for product in data["products"]:
            self.assertIn(product["name"], readme)
        for contact in data["contact"]:
            self.assertIn(contact["url"], readme)


if __name__ == "__main__":
    unittest.main()
