"""Primitivas compartidas: paleta, texto, marcos de pantalla y logo en pixel art."""

from __future__ import annotations

import math
from xml.sax.saxutils import escape

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"
MONO_RATIO = 0.61

# Las pantallas son oscuras en ambos temas, como un display real.
SCREEN = {
    "bg": "#04070C",
    "panel": "#0A1019",
    "panel2": "#0F1723",
    "line": "#1B2636",
    "text": "#EAF2FA",
    "muted": "#8494A7",
    "dim": "#3B4858",
    "cyan": "#22D3EE",
    "cyan2": "#67E8F9",
    "indigo": "#818CF8",
    "live": "#FB7185",
    "ok": "#34D399",
    "warn": "#FBBF24",
}

# Lo que cambia con el tema de GitHub es el chasis alrededor de las pantallas.
THEMES = {
    "dark": {"bezel": "#121922", "edge": "#253041", "shine": "#3A4658", "ink": "#E6EDF3", "muted": "#8B98A5"},
    "light": {"bezel": "#E4E9EF", "edge": "#C5CED8", "shine": "#FFFFFF", "ink": "#1F2328", "muted": "#59636E"},
}

REDUCED_MOTION = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def e(value: str) -> str:
    return escape(str(value), {'"': "&quot;"})


def svg(width: int, height: int, defs: str, body: str, title: str, style: str = "") -> str:
    css = f"<style>{style}{REDUCED_MOTION}</style>" if style else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{e(title)}" fill="none">'
        f"<title>{e(title)}</title>{css}<defs>{defs}</defs>{body}</svg>\n"
    )


def text(x: float, y: float, value: str, *, size: float, fill: str, font: str = SANS, weight: int = 400,
         spacing: float = 0, anchor: str = "start", attrs: str = "") -> str:
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (
        f'<text x="{x:g}" y="{y:g}" font-family="{font}" font-size="{size:g}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}"{ls}{attrs}>{e(value)}</text>'
    )


def mono_width(value: str, size: float, spacing: float = 0) -> float:
    return len(value) * (size * MONO_RATIO + spacing)


def screen_defs() -> str:
    """Definiciones comunes a toda pantalla: degradado de marca, scanlines y viñeta."""
    s = SCREEN
    return (
        f'<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{s["cyan"]}"/><stop offset="1" stop-color="{s["indigo"]}"/></linearGradient>'
        '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#FFFFFF" fill-opacity="0.025"/></pattern>'
        '<radialGradient id="vignette" cx="0.5" cy="0.45" r="0.75">'
        '<stop offset="0.55" stop-color="#000" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#000" stop-opacity="0.55"/></radialGradient>'
        '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="6" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )


def device(x: float, y: float, w: float, h: float, theme: dict, *, r: float = 22, pad: float = 10) -> tuple[str, tuple]:
    """Chasis + pantalla. Devuelve el SVG y la caja interior (x, y, w, h)."""
    ix, iy, iw, ih = x + pad, y + pad, w - pad * 2, h - pad * 2
    body = (
        f'<rect x="{x + 0.5:g}" y="{y + 0.5:g}" width="{w - 1:g}" height="{h - 1:g}" rx="{r:g}" '
        f'fill="{theme["bezel"]}" stroke="{theme["edge"]}"/>'
        f'<path d="M{x + r:g} {y + 1.5:g} H{x + w - r:g}" stroke="{theme["shine"]}" stroke-opacity="0.6"/>'
        f'<rect x="{ix:g}" y="{iy:g}" width="{iw:g}" height="{ih:g}" rx="{r - pad + 2:g}" fill="{SCREEN["bg"]}"/>'
    )
    return body, (ix, iy, iw, ih)


def screen_overlay(box: tuple, r: float = 14) -> str:
    ix, iy, iw, ih = box
    return (
        f'<rect x="{ix:g}" y="{iy:g}" width="{iw:g}" height="{ih:g}" rx="{r:g}" fill="url(#scan)"/>'
        f'<rect x="{ix:g}" y="{iy:g}" width="{iw:g}" height="{ih:g}" rx="{r:g}" fill="url(#vignette)"/>'
    )


def channel(x: float, y: float, number: int, label: str) -> str:
    """Rótulo de canal en la esquina de una pantalla: ● CH 01 — ETIQUETA."""
    s = SCREEN
    caption = f"CH {number:02d}  ·  {label.upper()}"
    return (
        f'<circle cx="{x + 4:g}" cy="{y - 4:g}" r="3.5" fill="{s["cyan"]}"/>'
        + text(x + 16, y, caption, size=12, fill=s["muted"], font=MONO, weight=600, spacing=2)
    )


def live_badge(right: float, y: float, label: str = "EN VIVO") -> str:
    s = SCREEN
    w = mono_width(label, 12, 2) + 34
    x = right - w
    return (
        f'<rect x="{x:g}" y="{y - 17:g}" width="{w:g}" height="26" rx="13" fill="{s["live"]}" fill-opacity="0.12" '
        f'stroke="{s["live"]}" stroke-opacity="0.5"/>'
        f'<circle class="blink" cx="{x + 15:g}" cy="{y - 4:g}" r="4" fill="{s["live"]}" filter="url(#glow)"/>'
        + text(x + 26, y, label, size=12, fill=s["live"], font=MONO, weight=700, spacing=2)
    )


def lerp_color(a: str, b: str, t: float) -> str:
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb, strict=True))


GLYPHS = {
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
}


def pixel_logo(cx: float, cy: float, cell: float, *, radius: int = 10, letters: str = "ZG",
               twinkle: bool = True) -> str:
    """Hexágono de píxeles con las iniciales encendidas, guiño al identicon del avatar."""
    s = SCREEN
    n = radius * 2 + 1
    glyph_w = len(letters) * 6 - 1
    gx0, gy0 = (n - glyph_w) // 2, (n - 7) // 2
    knocked: set[tuple[int, int]] = set()
    for k, ch in enumerate(letters):
        for row, bits in enumerate(GLYPHS[ch]):
            for col, bit in enumerate(bits):
                if bit == "1":
                    knocked.add((gx0 + k * 6 + col, gy0 + row))

    body = ""
    for gy in range(n):
        for gx in range(n):
            px, py = gx - radius, gy - radius
            # Hexágono con vértices arriba y abajo, en coordenadas de rejilla.
            if abs(px) > radius * 0.87 or abs(py) + abs(px) * 0.577 > radius:
                continue
            t = (gx + gy) / (2 * n)
            if (gx, gy) in knocked:
                color, opacity = s["text"], 1
            else:
                color, opacity = lerp_color(s["cyan"], s["indigo"], t), 0.5
            x = cx + px * cell - cell / 2
            y = cy + py * cell - cell / 2
            cls = ""
            if twinkle and opacity < 1 and (gx * 7 + gy * 13) % 11 == 0:
                cls = f' class="tw tw{(gx + gy) % 4}"'
            body += (
                f'<rect{cls} x="{x:.1f}" y="{y:.1f}" width="{cell - 1.5:.1f}" height="{cell - 1.5:.1f}" '
                f'rx="1" fill="{color}" fill-opacity="{opacity}"/>'
            )
    return body


TWINKLE_CSS = (
    ".tw{animation:tw 4s ease-in-out infinite}"
    "@keyframes tw{0%,100%{opacity:1}50%{opacity:.25}}"
    ".tw1{animation-delay:1s}.tw2{animation-delay:2s}.tw3{animation-delay:3s}"
    ".blink{animation:blink 1.4s ease-in-out infinite}@keyframes blink{50%{opacity:.25}}"
)


def hexagon(cx: float, cy: float, r: float, rotation: float = 30) -> str:
    pts = []
    for i in range(6):
        a = math.radians(60 * i + rotation)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)
