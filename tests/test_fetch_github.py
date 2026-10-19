import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from fetch_github import parse_calendar  # noqa: E402

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


if __name__ == "__main__":
    unittest.main()
