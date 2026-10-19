"""CH 01 — Pantalla principal: escenas rotativas, ficha lateral y rótulo de noticias."""

from __future__ import annotations

import textwrap

from .kit import (
    MONO,
    SCREEN,
    TWINKLE_CSS,
    channel,
    device,
    live_badge,
    mono_width,
    pixel_logo,
    screen_defs,
    screen_overlay,
    svg,
    text,
)

W, H = 1200, 580
CYCLE = 21  # segundos por vuelta completa de las tres escenas


def build(data: dict, theme: dict) -> str:
    s = SCREEN
    me = data["identity"]
    frame, box = device(0, 0, W, H, theme)
    ix, iy, iw, ih = box
    x0 = ix + 44

    top = (
        channel(x0, iy + 40, 1, "Presentación")
        + live_badge(ix + iw - 28, iy + 40)
        + f'<path d="M{ix:g} {iy + 62:g} H{ix + iw:g}" stroke="{s["line"]}"/>'
    )

    # Escena 1: identidad.
    tagline = textwrap.wrap(me["tagline"], 58)
    scene1 = (
        text(x0, 150, me["kicker"].upper(), size=14, fill=s["cyan"], font=MONO, weight=600, spacing=3)
        + text(x0 - 4, 242, me["first_name"], size=92, fill=s["text"], weight=800, spacing=-3)
        + text(x0 - 4, 334, me["last_name"], size=92, fill="url(#brand)", weight=800, spacing=-3)
        + text(x0, 382, me["role"], size=20, fill=s["muted"], font=MONO)
        + f'<rect class="caret" x="{x0 + mono_width(me["role"], 20) + 8:.1f}" y="366" width="11" height="20" '
        f'fill="{s["cyan"]}"/>'
        + "".join(text(x0, 422 + i * 26, line, size=18, fill=s["text"], attrs=' fill-opacity="0.82"')
                  for i, line in enumerate(tagline))
    )

    # Escena 2: estado de los productos, como una consola.
    lines = [("$", "zemzystem status --productos", s["cyan"], s["text"])]
    for p in data["products"]:
        live = p["status"] == "live"
        name = p["name"].lower().replace(" ", "-")
        state = "producción" if live else "en desarrollo"
        lines.append(("●", f"{name:<16}{'.' * 6}  {state}", s["ok"] if live else s["warn"], s["text"]))
    term = ""
    for i, (glyph, body, gc, tc) in enumerate(lines):
        y = 150 + i * 40
        term += (
            f'<g class="ln ln{i}">'
            + text(x0, y, glyph, size=19, fill=gc, font=MONO, weight=700)
            + text(x0 + 30, y, body, size=19, fill=tc, font=MONO)
            + "</g>"
        )
    y_prompt = 150 + len(lines) * 40
    term += (
        f'<g class="ln ln{len(lines)}">' + text(x0, y_prompt, "$", size=19, fill=s["cyan"], font=MONO, weight=700)
        + f'<rect class="caret" x="{x0 + 30}" y="{y_prompt - 17}" width="11" height="21" fill="{s["cyan"]}"/></g>'
    )
    scene2 = term

    # Escena 3: declaración.
    first, second = me["statement"]
    scene3 = (
        text(x0, 150, "MANIFIESTO", size=14, fill=s["cyan"], font=MONO, weight=600, spacing=3)
        + text(x0 - 3, 250, first, size=70, fill=s["text"], weight=800, spacing=-2)
        + text(x0 - 3, 336, second, size=70, fill="url(#brand)", weight=800, spacing=-2)
        + text(x0, 398, "  ·  ".join(me["verticals"]), size=16, fill=s["muted"], font=MONO)
    )

    # Progreso de escenas, al estilo de un carrusel de cartelería.
    progress = ""
    for k in range(3):
        bx = x0 + k * 96
        progress += (
            f'<rect x="{bx}" y="482" width="84" height="3" rx="1.5" fill="{s["line"]}"/>'
            f'<rect class="pg pg{k}" x="{bx}" y="482" width="84" height="3" rx="1.5" fill="url(#brand)"/>'
        )

    # Ficha lateral.
    px, py, pw, ph = 852, 92, 304, 400
    side = (
        f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="16" fill="{s["panel"]}" stroke="{s["line"]}"/>'
        + text(px + 22, py + 32, "NODO · ZG-01", size=11, fill=s["muted"], font=MONO, weight=600, spacing=2)
        + f'<circle class="blink" cx="{px + pw - 26}" cy="{py + 28}" r="4" fill="{s["ok"]}"/>'
        + pixel_logo(px + pw / 2, py + 150, 8.2)
    )
    for i, spec in enumerate(me["specs"]):
        y = py + 282 + i * 30
        side += (
            f'<path d="M{px + 22} {y + 10} H{px + pw - 22}" stroke="{s["line"]}" stroke-dasharray="2 4"/>'
            + text(px + 22, y, spec["label"], size=11, fill=s["dim"], font=MONO, weight=700, spacing=2)
            + text(px + pw - 22, y, spec["value"], size=14, fill=s["text"], font=MONO, anchor="end")
        )

    # Rótulo inferior en movimiento.
    ty = iy + ih - 58
    item_sep = "   ◆   "
    run = item_sep.join(i.upper() for i in data["ticker"]["items"]) + item_sep
    run_w = mono_width(run, 15, 1.5)
    ticker = (
        f'<rect x="{ix}" y="{ty}" width="{iw}" height="58" fill="{s["panel2"]}"/>'
        f'<path d="M{ix} {ty} H{ix + iw}" stroke="{s["line"]}"/>'
        f'<g clip-path="url(#crawl)"><g class="tick">'
        + text(ix + 150, ty + 35, run + run, size=15, fill=s["text"], font=MONO, weight=500, spacing=1.5)
        + "</g></g>"
        f'<rect x="{ix}" y="{ty}" width="130" height="58" fill="url(#brand)"/>'
        + text(ix + 65, ty + 35, "AHORA", size=14, fill=s["bg"], font=MONO, weight=800, spacing=3, anchor="middle")
    )

    defs = (
        screen_defs()
        + f'<clipPath id="scr"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="14"/></clipPath>'
        + f'<clipPath id="crawl"><rect x="{ix + 130}" y="{ty}" width="{iw - 130}" height="58"/></clipPath>'
        + f'<radialGradient id="aura" cx="0.3" cy="0.4" r="0.6"><stop offset="0" stop-color="{s["indigo"]}" '
        'stop-opacity="0.16"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>'
    )
    body = (
        frame
        + f'<g clip-path="url(#scr)"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" fill="url(#aura)"/>'
        + top
        + f'<g class="sc s1">{scene1}</g><g class="sc s2">{scene2}</g><g class="sc s3">{scene3}</g>'
        + progress + side + ticker + screen_overlay(box) + "</g>"
    )

    c = CYCLE
    n_lines = len(lines) + 1
    line_css = "".join(
        f".ln{i}{{animation:ln{i} {c}s steps(1) infinite}}"
        f"@keyframes ln{i}{{0%,{34 + i * 2.2:.1f}%{{opacity:0}}{34 + i * 2.2 + 0.1:.1f}%,100%{{opacity:1}}}}"
        for i in range(n_lines)
    )
    style = (
        f".s2,.s3{{opacity:0}}"
        f".s1{{animation:s1 {c}s infinite}}@keyframes s1{{0%,29%{{opacity:1}}33%,96%{{opacity:0}}100%{{opacity:1}}}}"
        f".s2{{animation:s2 {c}s infinite}}@keyframes s2{{0%,29%{{opacity:0}}33%,62%{{opacity:1}}66%,100%{{opacity:0}}}}"
        f".s3{{animation:s3 {c}s infinite}}@keyframes s3{{0%,62%{{opacity:0}}66%,96%{{opacity:1}}100%{{opacity:0}}}}"
        + line_css
        + ".pg{transform-box:fill-box;transform-origin:left center}.pg1,.pg2{transform:scaleX(0)}"
        + "".join(
            f".pg{k}{{animation:pg{k} {c}s linear infinite}}"
            f"@keyframes pg{k}{{0%,{k * 33.3:.1f}%{{transform:scaleX(0)}}{k * 33.3 + 32:.1f}%{{transform:scaleX(1)}}"
            f"{k * 33.3 + 33:.1f}%,100%{{transform:scaleX(0)}}}}"
            for k in range(3)
        )
        + ".caret{animation:caret 1.1s steps(1) infinite}@keyframes caret{50%{opacity:0}}"
        + f".tick{{animation:tick {run_w / 55:.1f}s linear infinite}}"
        f"@keyframes tick{{to{{transform:translateX(-{run_w:.1f}px)}}}}"
        + TWINKLE_CSS
    )
    title = f'{me["first_name"]} {me["last_name"]} — {me["kicker"]}. {me["role"]}. {me["tagline"]}'
    return svg(W, H, defs, body, title, style)


