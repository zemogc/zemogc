"""Descarga la gráfica pública de contribuciones y escribe data/github.json.

Lee la misma gráfica que GitHub muestra en el perfil, así que incluye las
contribuciones privadas cuando el perfil las tiene visibles. No necesita token.

    python3 scripts/fetch_github.py           # escribe data/github.json
    python3 scripts/fetch_github.py --check   # solo valida, no escribe nada
"""

from __future__ import annotations

import json
import os
import re
import sys
import tomllib
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "github.json"
USER_AGENT = "zemogc-profile-refresh"

CELL = re.compile(r"<td\b[^>]*>", re.S)
TIP = re.compile(r"<tool-tip\b([^>]*)>\s*([^<]+?)\s*</tool-tip>", re.S)
TOTAL = re.compile(r"([\d,]+)\s+contributions?\s+in the last year", re.S)


def get(url: str, token: str | None = None) -> str:
    headers = {"User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def attr(tag: str, name: str) -> str | None:
    match = re.search(rf'\b{name}="([^"]*)"', tag)
    return match.group(1) if match else None


def parse_calendar(html: str) -> tuple[list[list[dict]], int | None]:
    """Devuelve las semanas (domingo a sábado) y el total que declara la página."""
    tips = {attr(attrs, "for"): label for attrs, label in TIP.findall(html)}
    days = []
    for tag in CELL.findall(html):
        day, cell = attr(tag, "data-date"), attr(tag, "id")
        if not day or not cell:
            continue
        label = tips.get(cell, "")
        match = re.match(r"([\d,]+)\s+contribution", label)
        days.append({"date": day, "count": int(match.group(1).replace(",", "")) if match else 0})
    days.sort(key=lambda d: d["date"])

    weeks: list[list[dict]] = []
    for d in days:
        if not weeks or date.fromisoformat(d["date"]).isoweekday() == 7:  # domingo abre semana
            weeks.append([])
        weeks[-1].append(d)

    total = TOTAL.search(html)
    return weeks, int(total.group(1).replace(",", "")) if total else None


def readable(counted: int, declared: int | None, weeks: list) -> bool:
    """La página cambia durante el día: se tolera un desfase pequeño, no un formato roto."""
    if not weeks or declared is None:
        return False
    return abs(counted - declared) <= max(5, declared * 0.02)


def profile_info(login: str) -> dict:
    """Datos de la API REST; si falla (p. ej. límite de peticiones), conserva los anteriores."""
    try:
        profile = json.loads(get(f"https://api.github.com/users/{login}", os.environ.get("GITHUB_TOKEN")))
        return {"created_at": profile["created_at"], "public_repos": profile["public_repos"]}
    except (urllib.error.URLError, KeyError, ValueError) as error:
        if not OUT.exists():
            raise
        previous = json.loads(OUT.read_text(encoding="utf-8"))
        print(f"API de perfil no disponible ({error}); se conservan los datos anteriores")
        return {"created_at": previous["created_at"], "public_repos": previous["public_repos"]}


def main() -> None:
    check = "--check" in sys.argv[1:]
    login = tomllib.loads((ROOT / "content" / "profile.toml").read_text(encoding="utf-8"))["login"]

    weeks, declared = parse_calendar(get(f"https://github.com/users/{login}/contributions"))
    counted = sum(d["count"] for week in weeks for d in week)
    if not readable(counted, declared, weeks):
        raise SystemExit(f"La gráfica no se pudo leer: {len(weeks)} semanas, {counted} contadas, {declared} declaradas")
    if counted != declared:
        print(f"Aviso: {counted} contadas frente a {declared} declaradas; se usa la suma de los días")

    snapshot = {
        "login": login,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **profile_info(login),
        "total_contributions": counted,
        "weeks": weeks,
    }
    print(f"{counted} contribuciones · {len(weeks)} semanas · {snapshot['public_repos']} repos públicos")
    if check:
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
