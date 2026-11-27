"""Genera los SVG del perfil a partir de content/profile.toml y data/github.json.

Cada recurso se emite en variante dark y light para que el README elija
según el tema de GitHub con <picture>. Solo usa la biblioteca estándar:

    python3 scripts/build_assets.py
"""

from __future__ import annotations

import json
import shutil
import tomllib
from collections.abc import Callable
from pathlib import Path

from render import activity, contact, hero, products, system
from render.kit import THEMES

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "profile.toml"
GITHUB = ROOT / "data" / "github.json"
ASSETS = ROOT / "assets"


def load() -> dict:
    data = tomllib.loads(CONTENT.read_text(encoding="utf-8"))
    data["github"] = json.loads(GITHUB.read_text(encoding="utf-8")) if GITHUB.exists() else None
    return data


def build_all(data: dict) -> dict[str, str]:
    """Devuelve {ruta relativa a assets/: contenido SVG} para todos los temas."""
    outputs: dict[str, Callable[[dict], str]] = {
        "hero": lambda t: hero.build(data, t),
        "system": lambda t: system.build(data, t),
        "activity": lambda t: activity.build(data, t),
        "products": lambda t: products.build(data, t),
        "outro": lambda t: contact.outro(data, t),
    }
    for c in data["contact"]:
        outputs[f'contact/{c["slug"]}'] = lambda t, c=c: contact.button(c, t)
    return {
        f"{name}-{theme}.svg": build(tokens)
        for name, build in outputs.items()
        for theme, tokens in THEMES.items()
    }


def main() -> None:
    files = build_all(load())
    shutil.rmtree(ASSETS, ignore_errors=True)
    for relative, svg in files.items():
        path = ASSETS / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        # Bytes explícitos: en Windows write_text() escribiría CRLF y ensuciaría el diff.
        path.write_bytes(svg.encode("utf-8"))
    print(f"{len(files)} SVG generados en {ASSETS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
