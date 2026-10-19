"""CH 05 — Contacto: botones enlazables y franja de cierre."""

from __future__ import annotations

from .kit import MONO, SCREEN, channel, device, mono_width, screen_defs, screen_overlay, svg, text

ICONS = {
    "linkedin": lambda x, y, c: (
        f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="4" fill="{c}"/>'
        + text(x, y + 5, "in", size=13, fill=SCREEN["bg"], weight=800, anchor="middle")
    ),
    "globe": lambda x, y, c: (
        f'<circle cx="{x}" cy="{y}" r="9.5" stroke="{c}" stroke-width="1.7"/>'
        f'<ellipse cx="{x}" cy="{y}" rx="4" ry="9.5" stroke="{c}" stroke-width="1.5"/>'
        f'<path d="M{x - 9.5} {y} H{x + 9.5}" stroke="{c}" stroke-width="1.5"/>'
    ),
    "instagram": lambda x, y, c: (
        f'<rect x="{x - 10}" y="{y - 10}" width="20" height="20" rx="6" stroke="{c}" stroke-width="1.7"/>'
        f'<circle cx="{x}" cy="{y}" r="4.6" stroke="{c}" stroke-width="1.7"/>'
        f'<circle cx="{x + 5.6}" cy="{y - 5.6}" r="1.3" fill="{c}"/>'
    ),
}


def button(c: dict, theme: dict) -> str:
    s = SCREEN
    h = 56
    w = int(64 + mono_width(c["label"], 15) + 26)
    body = (
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" fill="{s["bg"]}" '
        f'stroke="{theme["edge"]}"/>'
        f'<rect x="4.5" y="4.5" width="{w - 9}" height="{h - 9}" rx="{(h - 9) / 2}" fill="url(#scan)" '
        f'stroke="{s["line"]}"/>'
        + ICONS[c["icon"]](34, h / 2, s["cyan"])
        + text(58, h / 2 + 5.5, c["label"], size=15, fill=s["text"], font=MONO, weight=600)
    )
    return svg(w, h, screen_defs(), body, c["label"])


def outro(data: dict, theme: dict) -> str:
    s = SCREEN
    w, h = 1200, 96
    frame, box = device(0, 0, w, h, theme, r=18, pad=8)
    ix, iy, iw, ih = box
    sep = "   ✦   "
    run = sep.join(["GRACIAS POR SINTONIZAR", "ZEMZYSTEM", "SOFTWARE QUE VIVE EN PANTALLAS REALES",
                    "HECHO EN COLOMBIA"]) + sep
    run_w = mono_width(run, 15, 2)
    body = (
        frame + '<g clip-path="url(#scr)">'
        + channel(ix + 26, iy + ih / 2 + 5, 5, "Fin")
        + f'<path d="M{ix + 170} {iy} V{iy + ih}" stroke="{s["line"]}"/>'
        + '<g clip-path="url(#crawl)"><g class="tick">'
        + text(ix + 190, iy + ih / 2 + 5.5, run + run, size=15, fill=s["text"], font=MONO, weight=500, spacing=2)
        + "</g></g>" + screen_overlay(box, 10) + "</g>"
    )
    defs = (
        screen_defs()
        + f'<clipPath id="scr"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="10"/></clipPath>'
        + f'<clipPath id="crawl"><rect x="{ix + 171}" y="{iy}" width="{iw - 171}" height="{ih}"/></clipPath>'
    )
    style = (f".tick{{animation:tick {run_w / 50:.1f}s linear infinite}}"
             f"@keyframes tick{{to{{transform:translateX(-{run_w:.1f}px)}}}}")
    return svg(w, h, defs, body, "Gracias por sintonizar — ZemZysteM", style)
