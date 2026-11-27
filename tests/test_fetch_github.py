import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import fetch_github  # noqa: E402
from fetch_github import parse_calendar, readable  # noqa: E402

# Fragmento con la forma de https://github.com/users/<login>/contributions.
HTML = """
<h2 class="f4 text-normal mb-2">
  1,207
  contributions
  in the last year
</h2>
<td tabindex="0" data-ix="0" style="width: 10px" data-date="2026-10-17" id="contribution-day-component-6-0"
    data-level="0" role="gridcell" class="ContributionCalendar-day"></td>
<td tabindex="0" data-ix="1" data-date="2026-10-18" id="contribution-day-component-0-1" data-level="4"
    role="gridcell" class="ContributionCalendar-day"></td>
<td data-date="2026-10-19" id="contribution-day-component-1-1" data-level="1" class="ContributionCalendar-day"></td>
<td class="ContributionCalendar-label">Mon</td>
<tool-tip id="tooltip-a" for="contribution-day-component-6-0" popover="manual">No contributions on October 17th.</tool-tip>
<tool-tip id="tooltip-b" for="contribution-day-component-0-1" popover="manual">1,206 contributions on October 18th.</tool-tip>
<tool-tip id="tooltip-c" for="contribution-day-component-1-1" popover="manual">1 contribution on October 19th.</tool-tip>
"""


class ParseCalendarTest(unittest.TestCase):
    def test_counts_days_and_total(self):
        weeks, total = parse_calendar(HTML)
        self.assertEqual(total, 1207)
        days = [d for week in weeks for d in week]
        self.assertEqual([d["count"] for d in days], [0, 1206, 1])
        self.assertEqual(sum(d["count"] for d in days), total)

    def test_sunday_starts_a_week(self):
        weeks, _ = parse_calendar(HTML)
        self.assertEqual([[d["date"] for d in w] for w in weeks], [["2026-10-17"], ["2026-10-18", "2026-10-19"]])

    def test_unreadable_page(self):
        weeks, total = parse_calendar("<html></html>")
        self.assertEqual((weeks, total), ([], None))


class ReadableTest(unittest.TestCase):
    def test_small_drift_is_tolerated(self):
        # La página puede sumar una contribución del día entre la cabecera y las celdas.
        self.assertTrue(readable(933, 934, [[{}]]))

    def test_broken_format_is_rejected(self):
        self.assertFalse(readable(0, 934, [[{}]]))
        self.assertFalse(readable(934, None, [[{}]]))
        self.assertFalse(readable(0, 0, []))


class _Response:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return b"ok"


class GetRetryTest(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.object(fetch_github.time, "sleep")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_retries_transient_errors(self):
        errors = [urllib.error.HTTPError("u", 503, "x", {}, None), _Response()]
        with mock.patch.object(fetch_github.urllib.request, "urlopen", side_effect=errors) as urlopen:
            self.assertEqual(fetch_github.get("https://example.test"), "ok")
        self.assertEqual(urlopen.call_count, 2)

    def test_does_not_retry_client_errors(self):
        error = urllib.error.HTTPError("u", 404, "x", {}, None)
        with mock.patch.object(fetch_github.urllib.request, "urlopen", side_effect=error) as urlopen:
            with self.assertRaises(urllib.error.HTTPError):
                fetch_github.get("https://example.test")
        self.assertEqual(urlopen.call_count, 1)


if __name__ == "__main__":
    unittest.main()
