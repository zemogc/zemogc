import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_readme  # noqa: E402


class ReadmeTest(unittest.TestCase):
    def test_all_referenced_assets_exist(self):
        self.assertEqual(check_readme.main(), 0)

    def test_every_image_has_alt_text(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for tag in re.findall(r"<img[^>]*>", readme):
            self.assertRegex(tag, r'alt="[^"]+"')


if __name__ == "__main__":
    unittest.main()
