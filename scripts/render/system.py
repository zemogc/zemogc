"""CH 02 — Ficha del sistema al estilo neofetch."""

from __future__ import annotations

from .kit import MONO, SCREEN, TWINKLE_CSS, mono_width, pixel_logo, screen_defs, screen_overlay, svg, text

W = 1200
ROW = 29


def build(data: dict, theme: dict) -> str:
    s = SCREEN
    rows = data["system"]
    h = 240 + len(rows) * ROW
    login = data["login"]

    chrome = (
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="16" fill="{s["bg"]}" stroke="{theme["edge"]}"/>'
        f'<path d="M1 46 V16.5 A15.5 15.5 0 0 1 16.5 1 H{W - 16.5} A15.5 15.5 0 0 1 {W - 1} 16.5 V46 Z" '
        f'fill="{s["panel2"]}"/>'
        f'<path d="M1 46 H{W - 1}" stroke="{s["line"]}"/>'
        + "".join(f'<circle cx="{26 + i * 22}" cy="23.5" r="6.5" fill="{c}" fill-opacity="0.85"/>'
                  for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
        + text(W / 2, 28, f"{login}@zemzystem: ~ — CH 02 · SISTEMA", size=13, fill=s["muted"], font=MONO,
               anchor="middle")
    )

    logo = pixel_logo(212, 128 + (h - 128) / 2 - 10, 13.5)

    x = 420
    prompt = (
        text(x, 92, f"{login}@zemzystem", size=16, fill=s["ok"], font=MONO, weight=700)
        + text(x + mono_width(f"{login}@zemzystem", 16), 92, " ~ $ neofetch --perfil", size=16, fill=s["muted"],
               font=MONO)
    )
    head = "zemog@zemzystem"
    header = (
        text(x, 138, "zemog", size=24, fill=s["cyan"], font=MONO, weight=800)
        + text(x + mono_width("zemog", 24), 138, "@", size=24, fill=s["text"], font=MONO, weight=800)
        + text(x + mono_width("zemog@", 24), 138, "zemzystem", size=24, fill=s["indigo"], font=MONO, weight=800)
        + f'<path d="M{x} 156 H{x + mono_width(head, 24):.0f}" stroke="{s["dim"]}" stroke-dasharray="7 4" '
        'stroke-width="2"/>'
    )
    lines = ""
    for i, row in enumerate(rows):
        y = 196 + i * ROW
        lines += (
            f'<g class="row" style="animation-delay:{0.15 + i * 0.07:.2f}s">'
            + text(x, y, f'{row["label"]}', size=16, fill=s["cyan"], font=MONO, weight=700)
            + text(x + 160, y, row["value"], size=16, fill=s["text"], font=MONO)
            + "</g>"
        )
    swatches = "".join(
        f'<rect x="{x + i * 34}" y="{h - 52}" width="30" height="16" rx="3" fill="{c}"/>'
        for i, c in enumerate((s["dim"], s["live"], s["ok"], s["warn"], s["cyan"], s["indigo"], "#A78BFA", s["text"]))
    )

    box = (1, 47, W - 2, h - 48)
    body = (
        chrome + f'<g clip-path="url(#win)">{logo}{prompt}{header}{lines}{swatches}'
        + screen_overlay(box, 0) + "</g>"
    )
    defs = screen_defs() + f'<clipPath id="win"><rect x="1" y="47" width="{W - 2}" height="{h - 48}" rx="15"/></clipPath>'
    style = (
        ".row{animation:row .5s ease-out both}"
        "@keyframes row{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}"
        + TWINKLE_CSS
    )
    title = "Ficha del sistema: " + "; ".join(f'{r["label"]}: {r["value"]}' for r in rows)
    return svg(W, h, defs, body, title, style)
