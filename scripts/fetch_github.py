"""Descarga el calendario de contribuciones y escribe data/github.json.

Pensado para GitHub Actions: usa GITHUB_TOKEN y el login de content/profile.toml.

    GITHUB_TOKEN=... python3 scripts/fetch_github.py
"""

from __future__ import annotations

import json
import os
import tomllib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "github.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def main() -> None:
    login = tomllib.loads((ROOT / "content" / "profile.toml").read_text(encoding="utf-8"))["login"]
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if payload.get("errors"):
        raise SystemExit(f"GraphQL: {payload['errors']}")

    user = payload["data"]["user"]
    calendar = user["contributionsCollection"]["contributionCalendar"]
    snapshot = {
        "login": login,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "created_at": user["createdAt"],
        "public_repos": user["repositories"]["totalCount"],
        "total_contributions": calendar["totalContributions"],
        "weeks": [
            [{"date": d["date"], "count": d["contributionCount"]} for d in week["contributionDays"]]
            for week in calendar["weeks"]
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{snapshot['total_contributions']} contribuciones · {len(snapshot['weeks'])} semanas")


if __name__ == "__main__":
    main()
