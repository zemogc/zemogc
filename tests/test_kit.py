import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from render.kit import e, lerp_color, mono_width, svg, text  # noqa: E402

SVG_NS = "{http://www.w3.org/2000/svg}"


class EscapeTest(unittest.TestCase):
    def test_escapes_xml_special_characters(self):
        self.assertEqual(e('Datos & "Pantallas" <ZG>'), "Datos &amp; &quot;Pantallas&quot; &lt;ZG&gt;")

    def test_text_content_is_escaped(self):
        node = ET.fromstring(text(0, 0, "Diseño & código", size=12, fill="#FFFFFF"))
        self.assertEqual(node.text, "Diseño & código")

    def test_title_with_quotes_keeps_the_svg_well_formed(self):
        root = ET.fromstring(svg(10, 10, "", "", 'Zemog "ZG" & ZemZysteM'))
        self.assertEqual(root.get("aria-label"), 'Zemog "ZG" & ZemZysteM')
        self.assertEqual(root.find(f"{SVG_NS}title").text, 'Zemog "ZG" & ZemZysteM')


class LerpColorTest(unittest.TestCase):
    def test_endpoints(self):
        self.assertEqual(lerp_color("#000000", "#FFFFFF", 0), "#000000")
        self.assertEqual(lerp_color("#000000", "#FFFFFF", 1), "#FFFFFF")

    def test_midpoint_per_channel(self):
        self.assertEqual(lerp_color("#000000", "#FF8040", 0.5), "#804020")


class MonoWidthTest(unittest.TestCase):
    def test_grows_with_characters_and_spacing(self):
        self.assertAlmostEqual(mono_width("abcd", 10), 4 * 6.1)
        self.assertAlmostEqual(mono_width("abcd", 10, spacing=2), 4 * 8.1)
        self.assertEqual(mono_width("", 14), 0)


if __name__ == "__main__":
    unittest.main()
