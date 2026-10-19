"""Genera los SVG del perfil a partir de content/profile.toml.

Cada recurso se emite en dos variantes, dark y light, para que el README
pueda elegir según el tema de GitHub con <picture>. Solo usa la biblioteca
estándar: python3 scripts/build_assets.py
"""

from __future__ import annotations

import math
import textwrap
import tomllib
from collections.abc import Callable
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "profile.toml"
ASSETS = ROOT / "assets"

THEMES = {
    "dark": {
        "bg": "#0D1117",
        "surface": "#111820",
        "raised": "#161F2A",
        "border": "#232E3B",
        "text": "#E6EDF3",
        "muted": "#8B98A5",
        "faint": "#2A3644",
        "accent": "#22D3EE",
        "accent2": "#818CF8",
        "chip": "#0F2530",
    },
    "light": {
        "bg": "#FFFFFF",
        "surface": "#FBFCFD",
        "raised": "#F3F6F9",
        "border": "#D8DEE4",
        "text": "#1F2328",
        "muted": "#59636E",
        "faint": "#E3E8ED",
        "accent": "#0E7490",
        "accent2": "#4F46E5",
        "chip": "#E8F6F9",
    },
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

# Ancho medio de un carácter monoespaciado respecto al tamaño de fuente.
MONO_RATIO = 0.61

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def e(value: str) -> str:
    return escape(value, {'"': "&quot;"})


def svg(width: int, height: int, body: str, title: str, style: str = "") -> str:
    css = f"<style>{style}{REDUCED_MOTION}</style>" if style else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{e(title)}" fill="none">'
        f"<title>{e(title)}</title>{css}{body}</svg>\n"
    )


def text(x: float, y: float, value: str, *, size: int, fill: str, font: str = SANS,
         weight: int = 400, spacing: float = 0, anchor: str = "start", extra: str = "") -> str:
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{ls}{extra}>{e(value)}</text>'
    )


def mono_width(value: str, size: int, spacing: float = 0) -> float:
    return len(value) * (size * MONO_RATIO + spacing)


def chip(x: float, y: float, label: str, t: dict, *, size: int = 13, pad: int = 12,
         height: int = 30) -> tuple[str, float]:
    width = mono_width(label, size) + pad * 2
    body = (
        f'<rect x="{x}" y="{y}" width="{width:.1f}" height="{height}" rx="{height / 2}" '
        f'fill="{t["chip"]}" stroke="{t["border"]}"/>'
        + text(x + pad, y + height / 2 + size * 0.36, label, size=size, fill=t["text"], font=MONO)
    )
    return body, width


def hexagon(cx: float, cy: float, r: float, rotation: float = 30) -> str:
    points = []
    for i in range(6):
        angle = math.radians(60 * i + rotation)
        points.append(f"{cx + r * math.cos(angle):.1f},{cy + r * math.sin(angle):.1f}")
    return " ".join(points)


def hex_vertices(cx: float, cy: float, r: float, rotation: float = 30) -> list[tuple[float, float]]:
    return [
        (cx + r * math.cos(math.radians(60 * i + rotation)), cy + r * math.sin(math.radians(60 * i + rotation)))
        for i in range(6)
    ]


def gradient(gid: str, t: dict) -> str:
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/>'
        "</linearGradient>"
    )


# --------------------------------------------------------------------------- hero

def build_hero(data: dict, t: dict) -> str:
    w, h = 1200, 420
    hero = data["hero"]
    cx, cy = 968, 206

    defs = (
        "<defs>"
        + gradient("g", t)
        + f'<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1.5" cy="1.5" r="1.2" fill="{t["faint"]}"/></pattern>'
        f'<radialGradient id="fade" cx="{cx / w:.3f}" cy="{cy / h:.3f}" r="0.55">'
        '<stop offset="0" stop-color="#fff" stop-opacity="1"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
        '<mask id="m"><rect width="100%" height="100%" fill="url(#fade)"/></mask>'
        f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">'
        f'<stop offset="0" stop-color="{t["accent"]}" stop-opacity="0.22"/>'
        f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="panel"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20"/></clipPath>'
        "</defs>"
    )

    panel = (
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20" fill="{t["surface"]}" stroke="{t["border"]}"/>'
        f'<g clip-path="url(#panel)"><rect width="{w}" height="{h}" fill="url(#dots)" mask="url(#m)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="230" fill="url(#glow)"/>'
        f'<rect x="0" y="0" width="{w}" height="3" fill="url(#g)"/></g>'
    )

    # Columna izquierda: identidad.
    x = 68
    kicker = hero["kicker"].upper()
    kw = mono_width(kicker, 12, 2) + 44
    left = (
        f'<rect x="{x}" y="64" width="{kw:.1f}" height="32" rx="16" fill="{t["chip"]}" stroke="{t["border"]}"/>'
        f'<circle class="pulse" cx="{x + 18}" cy="80" r="4" fill="{t["accent"]}"/>'
        + text(x + 32, 84.5, kicker, size=12, fill=t["accent"], font=MONO, weight=600, spacing=2)
        + text(x - 3, 172, hero["name"], size=58, fill=t["text"], weight=700, spacing=-1.2)
        + text(x, 216, hero["role"], size=20, fill=t["muted"], font=MONO)
        + f'<rect class="caret" x="{x + mono_width(hero["role"], 20) + 6:.1f}" y="200" width="10" height="20" '
        f'fill="{t["accent"]}"/>'
    )
    for i, line in enumerate(hero["tagline"]):
        left += text(x, 268 + i * 28, line, size=19, fill=t["text"], extra=' opacity="0.86"')

    cxp = x
    for label in hero["chips"]:
        body, width = chip(cxp, 334, label, t, size=12, pad=12, height=28)
        left += body
        cxp += width + 10

    # Columna derecha: diagrama hexagonal (dominio, puertos, adaptadores).
    outer, middle, inner = 150, 102, 56
    connectors = ""
    for (x1, y1), (x2, y2) in zip(hex_vertices(cx, cy, inner), hex_vertices(cx, cy, outer)):
        connectors += (
            f'<line class="flow" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{t["accent"]}" stroke-opacity="0.55" stroke-width="1.4" stroke-dasharray="4 6"/>'
        )
    nodes = ""
    for i, (nx, ny) in enumerate(hex_vertices(cx, cy, outer)):
        nodes += (
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="6" fill="{t["surface"]}" stroke="url(#g)" stroke-width="2"/>'
            f'<circle class="node n{i}" cx="{nx:.1f}" cy="{ny:.1f}" r="2.4" fill="{t["accent"]}"/>'
        )
    diagram = (
        f'<g class="spin"><polygon points="{hexagon(cx, cy, outer + 22)}" stroke="{t["border"]}" '
        f'stroke-width="1" stroke-dasharray="2 8"/></g>'
        f'<polygon points="{hexagon(cx, cy, outer)}" stroke="{t["border"]}" stroke-width="1.2"/>'
        f'<polygon points="{hexagon(cx, cy, middle)}" fill="{t["raised"]}" stroke="{t["border"]}" stroke-width="1.2"/>'
        + connectors
        + f'<polygon points="{hexagon(cx, cy, inner)}" fill="url(#g)"/>'
        + text(cx, cy + 10, "ZG", size=30, fill=t["bg"], weight=800, anchor="middle", spacing=1)
        + nodes
        + text(cx, cy - inner - 16, "domain", size=11, fill=t["muted"], font=MONO, anchor="middle", spacing=1)
        + text(cx, cy + middle + 22, "ports", size=11, fill=t["muted"], font=MONO, anchor="middle", spacing=1)
        + text(cx - outer - 26, cy + 4, "adapters", size=11, fill=t["muted"], font=MONO, anchor="end", spacing=1)
    )

    style = (
        ".pulse{animation:pulse 2.4s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
        "@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.35;transform:scale(.7)}}"
        ".caret{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
        ".spin{animation:spin 90s linear infinite;transform-box:fill-box;transform-origin:center}"
        "@keyframes spin{to{transform:rotate(360deg)}}"
        ".flow{animation:flow 2.6s linear infinite}@keyframes flow{to{stroke-dashoffset:-20}}"
        ".node{animation:node 3.6s ease-in-out infinite;opacity:.3}"
        "@keyframes node{0%,100%{opacity:.3}40%{opacity:1}}"
        + "".join(f".n{i}{{animation-delay:{i * 0.6:.1f}s}}" for i in range(6))
    )
    title = f'{hero["name"]} — {hero["kicker"]}. {hero["role"]}.'
    return svg(w, h, defs + panel + left + diagram, title, style)


# --------------------------------------------------------------------------- secciones

def build_section(index: int, section: dict, t: dict) -> str:
    w, h = 1200, 64
    number = f"{index:02d}"
    label = section["title"]
    x_label = 66
    line_start = x_label + len(label) * 15 + 28
    body = (
        "<defs>" + gradient("g", t) + "</defs>"
        + text(0, 42, number, size=15, fill=t["accent"], font=MONO, weight=600, spacing=1)
        + f'<rect x="34" y="31" width="18" height="2" rx="1" fill="url(#g)"/>'
        + text(x_label, 43, label, size=26, fill=t["text"], weight=700, spacing=-0.3)
        + f'<line x1="{line_start}" y1="35" x2="{w}" y2="35" stroke="{t["border"]}"/>'
    )
    return svg(w, h, body, f"{number} — {label}")


# --------------------------------------------------------------------------- pilares

ICONS = {
    "hex": lambda x, y, c: (
        f'<polygon points="{hexagon(x, y, 13)}" stroke="{c}" stroke-width="1.8"/>'
        f'<polygon points="{hexagon(x, y, 5.5)}" fill="{c}"/>'
    ),
    "layers": lambda x, y, c: (
        f'<path d="M{x - 13} {y - 4} L{x} {y - 11} L{x + 13} {y - 4} L{x} {y + 3} Z" stroke="{c}" stroke-width="1.8" '
        f'stroke-linejoin="round"/>'
        f'<path d="M{x - 13} {y + 3} L{x} {y + 10} L{x + 13} {y + 3}" stroke="{c}" stroke-width="1.8" '
        f'stroke-linejoin="round" stroke-linecap="round"/>'
    ),
    "pulse": lambda x, y, c: (
        f'<path d="M{x - 14} {y} H{x - 7} L{x - 3} {y - 10} L{x + 2} {y + 10} L{x + 6} {y} H{x + 14}" '
        f'stroke="{c}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>'
    ),
    "bot": lambda x, y, c: (
        f'<rect x="{x - 12}" y="{y - 8}" width="24" height="18" rx="5" stroke="{c}" stroke-width="1.8"/>'
        f'<circle cx="{x - 5}" cy="{y + 1}" r="2.2" fill="{c}"/><circle cx="{x + 5}" cy="{y + 1}" r="2.2" fill="{c}"/>'
        f'<path d="M{x} {y - 8} V{y - 13}" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>'
        f'<circle cx="{x}" cy="{y - 14}" r="2" fill="{c}"/>'
    ),
}


def build_pillars(data: dict, t: dict) -> str:
    pillars = data["pillars"]
    gap, w = 16, 1200
    cw = (w - gap * (len(pillars) - 1)) / len(pillars)
    h = 236
    body = "<defs>" + gradient("g", t) + "</defs>"
    for i, p in enumerate(pillars):
        x = i * (cw + gap)
        body += (
            f'<rect x="{x + 0.5:.1f}" y="0.5" width="{cw - 1:.1f}" height="{h - 1}" rx="14" '
            f'fill="{t["surface"]}" stroke="{t["border"]}"/>'
            f'<rect x="{x + 24:.1f}" y="24" width="44" height="44" rx="12" fill="{t["chip"]}" stroke="{t["border"]}"/>'
            + ICONS[p["icon"]](x + 46, 46, t["accent"])
            + text(x + 84, 54, p["title"], size=21, fill=t["text"], weight=650)
        )
        for j, line in enumerate(textwrap.wrap(p["text"], 28)):
            body += text(x + 24, 108 + j * 26, line, size=17, fill=t["muted"])
    return svg(w, h, body, " · ".join(p["title"] for p in pillars))


# --------------------------------------------------------------------------- stack

def build_stack(data: dict, t: dict) -> str:
    w = 1200
    x0, x_max = 214, 1176
    row_h, chip_h, gap = 34, 34, 10
    body, y = "", 24
    rows = []
    for group in data["stack"]:
        x, line_y, chips = x0, y, ""
        for item in group["items"]:
            width = mono_width(item, 15) + 28
            if x + width > x_max:
                x, line_y = x0, line_y + chip_h + gap
            part, width = chip(x, line_y, item, t, size=15, pad=14, height=chip_h)
            chips += part
            x += width + 8
        rows.append((y, group["label"], chips))
        y = line_y + row_h + 22
    h = y + 2
    body += f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["surface"]}" stroke="{t["border"]}"/>'
    for i, (ry, label, chips) in enumerate(rows):
        if i:
            body += f'<line x1="24" y1="{ry - 11}" x2="{w - 24}" y2="{ry - 11}" stroke="{t["faint"]}"/>'
        body += (
            f'<rect x="24" y="{ry + 13}" width="8" height="8" rx="2" fill="{t["accent"]}"/>'
            + text(44, ry + 22, label.upper(), size=13, fill=t["muted"], font=MONO, weight=600, spacing=1.6)
            + chips
        )
    return svg(w, h, body, "Stack: " + "; ".join(f'{g["label"]}: {", ".join(g["items"])}' for g in data["stack"]))


# --------------------------------------------------------------------------- proyectos

def build_project(index: int, p: dict, t: dict) -> str:
    w, h = 590, 300
    body = (
        "<defs>" + gradient("g", t) + "</defs>"
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{t["surface"]}" stroke="{t["border"]}"/>'
        f'<rect x="28" y="0" width="64" height="3" rx="1.5" fill="url(#g)"/>'
        + text(28, 46, f'{index:02d} · {p["category"].upper()}', size=13, fill=t["accent"], font=MONO,
               weight=600, spacing=1.5)
    )
    badge = "PRIVADO"
    bw = mono_width(badge, 11, 1.2) + 34
    bx = w - 28 - bw
    body += (
        f'<rect x="{bx:.1f}" y="27" width="{bw:.1f}" height="26" rx="13" fill="{t["raised"]}" stroke="{t["border"]}"/>'
        f'<rect x="{bx + 12:.1f}" y="39" width="9" height="7" rx="1.5" fill="{t["muted"]}"/>'
        f'<path d="M{bx + 14:.1f} 39 v-2.2 a2.5 2.5 0 0 1 5 0 V39" stroke="{t["muted"]}" stroke-width="1.4"/>'
        + text(bx + 27, 44.5, badge, size=11, fill=t["muted"], font=MONO, weight=600, spacing=1.2)
        + text(28, 94, p["title"], size=29, fill=t["text"], weight=700, spacing=-0.4)
    )
    for j, line in enumerate(textwrap.wrap(p["text"], 54)):
        body += text(28, 134 + j * 27, line, size=18, fill=t["muted"])
    x = 28
    for tag in p["tags"]:
        part, width = chip(x, h - 60, tag, t, size=14, pad=12, height=32)
        body += part
        x += width + 8
    return svg(w, h, body, f'{p["title"]} — {p["category"]}. {p["text"]}')


# --------------------------------------------------------------------------- contacto

CONTACT_ICONS = {
    "linkedin": lambda x, y, c, bg: (
        f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="4" fill="{c}"/>'
        + text(x, y + 5, "in", size=13, fill=bg, weight=800, anchor="middle")
    ),
    "globe": lambda x, y, c, bg: (
        f'<circle cx="{x}" cy="{y}" r="9.5" stroke="{c}" stroke-width="1.7"/>'
        f'<ellipse cx="{x}" cy="{y}" rx="4" ry="9.5" stroke="{c}" stroke-width="1.5"/>'
        f'<path d="M{x - 9.5} {y} H{x + 9.5}" stroke="{c}" stroke-width="1.5"/>'
    ),
    "instagram": lambda x, y, c, bg: (
        f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="6" stroke="{c}" stroke-width="1.7"/>'
        f'<circle cx="{x}" cy="{y}" r="4.6" stroke="{c}" stroke-width="1.7"/>'
        f'<circle cx="{x + 5.6}" cy="{y - 5.6}" r="1.3" fill="{c}"/>'
    ),
    "github": lambda x, y, c, bg: (
        f'<g transform="translate({x - 10} {y - 10}) scale(1.25)"><path fill="{c}" fill-rule="evenodd" '
        'd="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49'
        '-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82'
        '.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15'
        '-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 '
        '2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54'
        '.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></g>'
    ),
}


def build_contact(c: dict, t: dict) -> str:
    h = 52
    w = int(56 + mono_width(c["label"], 14) + 22)
    body = (
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" '
        f'fill="{t["surface"]}" stroke="{t["border"]}"/>'
        + CONTACT_ICONS[c["icon"]](30, h / 2, t["accent"], t["bg"])
        + text(52, h / 2 + 5, c["label"], size=14, fill=t["text"], font=MONO, weight=500)
    )
    return svg(w, h, body, c["label"])


# --------------------------------------------------------------------------- footer

def build_footer(t: dict) -> str:
    w, h = 1200, 90
    wave = "M0 45 " + " ".join(
        f"L{x} {45 + (math.sin(x / 34) * 9 if 520 < x < 680 else 0):.1f}" for x in range(0, w + 1, 6)
    )
    body = (
        "<defs>" + gradient("g", t)
        + '<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        '<mask id="m"><rect width="100%" height="100%" fill="url(#fade)"/></mask></defs>'
        f'<path class="wave" d="{wave}" stroke="url(#g)" stroke-width="1.6" mask="url(#m)" '
        'stroke-dasharray="6 6"/>'
        f'<polygon points="{hexagon(600, 45, 13)}" fill="{t["bg"]}" stroke="url(#g)" stroke-width="1.6"/>'
        f'<circle class="pulse" cx="600" cy="45" r="3.5" fill="{t["accent"]}"/>'
    )
    style = (
        ".wave{animation:flow 3s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}"
        ".pulse{animation:pulse 2.4s ease-in-out infinite}@keyframes pulse{50%{opacity:.3}}"
    )
    return svg(w, h, body, "ZemZysteM", style)


# --------------------------------------------------------------------------- main

def main() -> None:
    data = tomllib.loads(CONTENT.read_text(encoding="utf-8"))
    outputs: dict[str, Callable[[dict], str]] = {
        "hero": lambda t: build_hero(data, t),
        "about": lambda t: build_pillars(data, t),
        "stack": lambda t: build_stack(data, t),
        "footer": build_footer,
    }
    for i, section in enumerate(data["sections"], start=1):
        outputs[f'sections/{section["slug"]}'] = lambda t, i=i, s=section: build_section(i, s, t)
    for i, project in enumerate(data["projects"], start=1):
        outputs[f'projects/{project["slug"]}'] = lambda t, i=i, p=project: build_project(i, p, t)
    for contact in data["contact"]:
        outputs[f'contact/{contact["slug"]}'] = lambda t, c=contact: build_contact(c, t)

    for name, build in outputs.items():
        for theme, tokens in THEMES.items():
            path = ASSETS / f"{name}-{theme}.svg"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(build(tokens), encoding="utf-8")
    print(f"{len(outputs) * len(THEMES)} SVG generados en {ASSETS.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
