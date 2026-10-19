"""CH 04 — Pared de pantallas: un monitor por producto, cada uno con su mini interfaz."""

from __future__ import annotations

from .kit import MONO, SANS, SCREEN, device, hexagon, mono_width, screen_defs, screen_overlay, svg, text

COLS, GAP = 3, 24
CW, CH = (1200 - GAP * (COLS - 1)) / COLS, 372


def scene_playlist(x: float, y: float, w: float, h: float) -> str:
    s = SCREEN
    out = ""
    tw, th = 88, 62
    for i in range(3):
        tx = x + 22 + i * (tw + 14)
        out += (
            f'<rect x="{tx}" y="{y + 22}" width="{tw}" height="{th}" rx="6" fill="{s["panel2"]}" stroke="{s["line"]}"/>'
            f'<rect class="slot sl{i}" x="{tx - 2}" y="{y + 20}" width="{tw + 4}" height="{th + 4}" rx="8" '
            f'stroke="{s["cyan"]}" stroke-width="2"/>'
        )
        if i == 0:
            out += (f'<circle cx="{tx + 26}" cy="{y + 46}" r="9" fill="{s["cyan"]}" fill-opacity="0.8"/>'
                    f'<path d="M{tx + 8} {y + 78} L{tx + 36} {y + 56} L{tx + 56} {y + 70} L{tx + 80} {y + 50} '
                    f'V{y + 78} Z" fill="{s["indigo"]}" fill-opacity="0.7"/>')
        elif i == 1:
            out += (f'<path d="M{tx + 36} {y + 40} L{tx + 56} {y + 53} L{tx + 36} {y + 66} Z" fill="{s["text"]}"/>')
        else:
            out += "".join(f'<rect x="{tx + 12}" y="{y + 36 + k * 11}" width="{64 - k * 16}" height="5" rx="2.5" '
                           f'fill="{s["muted"]}"/>' for k in range(3))
    bar_y = y + h - 32
    out += (
        f'<rect x="{x + 22}" y="{bar_y}" width="{w - 44}" height="4" rx="2" fill="{s["line"]}"/>'
        f'<rect class="play" x="{x + 22}" y="{bar_y}" width="{w - 44}" height="4" rx="2" fill="url(#brand)"/>'
        + text(x + 22, bar_y + 22, "PLAYLIST · LOBBY", size=10, fill=s["muted"], font=MONO, spacing=1.5)
        + text(x + w - 22, bar_y + 22, "AUTO", size=10, fill=s["cyan"], font=MONO, spacing=1.5, anchor="end")
    )
    return out


def scene_route(x: float, y: float, w: float, h: float) -> str:
    s = SCREEN
    rooms = [(18, 16, 92, 52), (118, 16, 70, 52), (196, 16, 108, 52), (18, 80, 70, 46), (196, 80, 108, 46)]
    out = "".join(
        f'<rect x="{x + rx}" y="{y + ry}" width="{rw}" height="{rh}" rx="4" fill="{s["panel2"]}" stroke="{s["line"]}"/>'
        for rx, ry, rw, rh in rooms
    )
    path = f"M{x + 40} {y + 112} H{x + 150} V{y + 74} H{x + 250} V{y + 46}"
    out += (
        f'<path d="{path}" stroke="{s["cyan"]}" stroke-opacity="0.25" stroke-width="6" stroke-linecap="round" '
        'stroke-linejoin="round"/>'
        f'<path class="route" d="{path}" stroke="{s["cyan"]}" stroke-width="2.5" stroke-dasharray="6 7" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle class="here" cx="{x + 40}" cy="{y + 112}" r="7" fill="{s["live"]}"/>'
        f'<circle cx="{x + 40}" cy="{y + 112}" r="3" fill="{s["text"]}"/>'
        f'<path d="M{x + 250} {y + 48} c-8 -10 -8 -22 0 -24 c8 2 8 14 0 24 Z" fill="{s["indigo"]}"/>'
        f'<circle cx="{x + 250}" cy="{y + 33}" r="3" fill="{s["bg"]}"/>'
    )
    qx, qy = x + w - 46, y + h - 40
    bits = "1110111 1010101 1110111 0001000 1011101 0110110 1011011"
    for r, row in enumerate(bits.split()):
        for c, bit in enumerate(row):
            if bit == "1":
                out += f'<rect x="{qx + c * 4}" y="{qy + r * 4}" width="3.4" height="3.4" fill="{s["text"]}"/>'
    out += text(x + 22, y + h - 14, "USTED ESTÁ AQUÍ", size=10, fill=s["muted"], font=MONO, spacing=1.5)
    return out


def scene_agents(x: float, y: float, w: float, h: float) -> str:
    s = SCREEN
    out = ""
    colors = (s["cyan"], s["indigo"], "#A78BFA", s["ok"])
    for i, color in enumerate(colors):
        ax = x + 30 + i * 74
        ay = y + 40
        out += (
            f'<rect x="{ax - 8}" y="{ay + 40}" width="56" height="6" rx="2" fill="{s["line"]}"/>'
            f'<rect x="{ax + 6}" y="{ay + 22}" width="28" height="18" rx="2" fill="{s["panel2"]}" stroke="{s["dim"]}"/>'
            f'<rect x="{ax + 12}" y="{ay}" width="12" height="12" fill="{color}"/>'
            f'<rect x="{ax + 9}" y="{ay + 12}" width="18" height="14" fill="{color}" fill-opacity="0.7"/>'
            f'<g class="bub b{i}"><rect x="{ax + 20}" y="{ay - 24}" width="26" height="16" rx="5" fill="{s["text"]}"/>'
            + "".join(f'<circle cx="{ax + 27 + k * 6}" cy="{ay - 16}" r="1.6" fill="{s["bg"]}"/>' for k in range(3))
            + "</g>"
        )
    out += (
        f'<rect x="{x + 22}" y="{y + h - 40}" width="{w - 44}" height="26" rx="13" fill="{s["ok"]}" '
        f'fill-opacity="0.1" stroke="{s["ok"]}" stroke-opacity="0.4"/>'
        + text(x + w / 2, y + h - 22, "✓ APROBACIÓN HUMANA", size=11, fill=s["ok"], font=MONO, weight=700,
               spacing=1.5, anchor="middle")
    )
    return out


def scene_ticket(x: float, y: float, w: float, h: float) -> str:
    s = SCREEN
    return (
        text(x + 24, y + 34, "TURNO", size=11, fill=s["muted"], font=MONO, weight=600, spacing=2)
        + '<g class="call">' + text(x + 22, y + 92, "A-024", size=54, fill="url(#brand)", font=MONO, weight=800)
        + "</g>"
        + text(x + 24, y + 122, "→ VENTANILLA 3", size=13, fill=s["text"], font=MONO, weight=600, spacing=1)
        + f'<path d="M{x + 218} {y + 18} V{y + h - 18}" stroke="{s["line"]}"/>'
        + text(x + 236, y + 34, "SIGUE", size=11, fill=s["muted"], font=MONO, weight=600, spacing=2)
        + "".join(text(x + 236, y + 66 + i * 28, t, size=16, fill=s["dim"] if i else s["text"], font=MONO, weight=600)
                  for i, t in enumerate(("A-025", "B-011", "A-026")))
    )


def scene_devices(x: float, y: float, w: float, h: float) -> str:
    s = SCREEN
    cx, cy = x + w / 2, y + 52
    out = ""
    targets = [(x + 54, y + 112, "ANDROID"), (x + w / 2, y + 120, "TIZEN"), (x + w - 54, y + 112, "WEBOS")]
    for i, (tx, ty, label) in enumerate(targets):
        out += (
            f'<path class="link" d="M{cx} {cy + 18} L{tx} {ty - 22}" stroke="{s["cyan"]}" stroke-opacity="0.6" '
            f'stroke-width="1.5" stroke-dasharray="4 5"/>'
            f'<rect x="{tx - 34}" y="{ty - 22}" width="68" height="40" rx="5" fill="{s["panel2"]}" stroke="{s["dim"]}"/>'
            f'<rect class="dv d{i}" x="{tx - 28}" y="{ty - 16}" width="56" height="28" rx="2" fill="url(#brand)" '
            'fill-opacity="0.55"/>'
            + text(tx, ty + 34, label, size=10, fill=s["muted"], font=MONO, spacing=1.5, anchor="middle")
        )
    out += (
        f'<polygon points="{hexagon(cx, cy, 26)}" fill="{s["bg"]}" stroke="url(#brand)" stroke-width="2"/>'
        + text(cx, cy + 4, "API", size=12, fill=s["text"], font=MONO, weight=800, anchor="middle", spacing=1)
    )
    return out


def scene_pulse(x: float, y: float, w: float, h: float) -> str:
    s = SCREEN
    base = y + 62
    pts = [(0, 0), (40, 0), (52, -6), (62, 0), (92, 0), (102, 18), (114, -40), (126, 26), (136, 0), (170, 0),
           (182, -8), (194, 0), (210, 0)]
    path = "M" + " L".join(f"{x + 18 + px:.0f} {base + py:.0f}" for px, py in pts)
    out = (
        f'<path d="{path}" stroke="{s["ok"]}" stroke-opacity="0.18" stroke-width="5" stroke-linejoin="round"/>'
        f'<path class="beat" d="{path}" stroke="{s["ok"]}" stroke-width="2" stroke-linejoin="round" '
        'stroke-dasharray="260" pathLength="260"/>'
    )
    services = [("app", s["ok"]), ("api", s["ok"]), ("vps", s["ok"])]
    for i, (name, color) in enumerate(services):
        sy = y + 30 + i * 26
        out += (
            f'<circle class="blink" cx="{x + 244}" cy="{sy - 4}" r="4" fill="{color}" '
            f'style="animation-delay:{i * 0.4:.1f}s"/>'
            + text(x + 256, sy, name, size=12, fill=s["text"], font=MONO)
            + text(x + w - 18, sy, "ok", size=12, fill=s["muted"], font=MONO, anchor="end")
        )
    out += (
        f'<path d="M{x + 18} {y + h - 34} H{x + w - 18}" stroke="{s["line"]}"/>'
        + text(x + 18, y + h - 14, "INCIDENTES POR UMBRAL", size=10, fill=s["muted"], font=MONO, spacing=1.5)
    )
    return out


SCENES = {
    "playlist": scene_playlist,
    "route": scene_route,
    "agents": scene_agents,
    "ticket": scene_ticket,
    "devices": scene_devices,
    "pulse": scene_pulse,
}


def card(i: int, p: dict, theme: dict) -> str:
    s = SCREEN
    x = (i % COLS) * (CW + GAP)
    y = (i // COLS) * (CH + GAP)
    frame, box = device(x, y, CW, CH, theme, r=18, pad=9)
    ix, iy, iw, ih = box
    live = p["status"] == "live"
    status = "● PRODUCCIÓN" if live else "◐ EN DESARROLLO"
    color = s["ok"] if live else s["warn"]
    sw = mono_width(status, 10, 1.2) + 20
    sx, sy, sww, sh = ix + 16, iy + 48, iw - 32, 150
    body = (
        frame + f'<g clip-path="url(#c{i})">'
        + text(ix + 18, iy + 30, f"{i + 1:02d} · {p['kind'].upper()}", size=11, fill=s["muted"], font=MONO,
               weight=600, spacing=1.6)
        + f'<rect x="{ix + iw - 16 - sw:.1f}" y="{iy + 15}" width="{sw:.1f}" height="22" rx="11" fill="{color}" '
        f'fill-opacity="0.1" stroke="{color}" stroke-opacity="0.45"/>'
        + text(ix + iw - 16 - sw / 2, iy + 30, status, size=10, fill=color, font=MONO, weight=700, spacing=1.2,
               anchor="middle")
        + f'<rect x="{sx}" y="{sy}" width="{sww}" height="{sh}" rx="10" fill="{s["panel"]}" stroke="{s["line"]}"/>'
        + SCENES[p["scene"]](sx, sy, sww, sh)
        + text(ix + 18, iy + 238, p["name"], size=27, fill=s["text"], font=SANS, weight=800, spacing=-0.6)
        + "".join(text(ix + 18, iy + 266 + k * 21, line, size=15, fill=s["muted"]) for k, line in enumerate(p["text"]))
        + f'<path d="M{ix + 18} {iy + ih - 44} H{ix + iw - 18}" stroke="{s["line"]}"/>'
        + text(ix + 18, iy + ih - 20, p["stack"], size=11.5, fill=s["cyan"], font=MONO, spacing=0.3)
        + screen_overlay(box, 10) + "</g>"
    )
    return body, f'<clipPath id="c{i}"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="10"/></clipPath>'


def build(data: dict, theme: dict) -> str:
    products = data["products"]
    rows = -(-len(products) // COLS)
    h = int(rows * CH + (rows - 1) * GAP)
    bodies, clips = zip(*(card(i, p, theme) for i, p in enumerate(products)), strict=True)
    style = (
        ".slot{opacity:0;animation:slot 6s infinite}.sl0{opacity:1}"
        "@keyframes slot{0%,30%{opacity:1}34%,100%{opacity:0}}"
        ".sl1{animation-delay:2s}.sl2{animation-delay:4s}"
        ".play{transform-box:fill-box;transform-origin:left center;animation:play 6s linear infinite}"
        "@keyframes play{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".route{animation:route 1.2s linear infinite}@keyframes route{to{stroke-dashoffset:-13}}"
        ".here{transform-box:fill-box;transform-origin:center;animation:here 1.8s ease-out infinite}"
        "@keyframes here{0%{transform:scale(.6);opacity:1}100%{transform:scale(2.2);opacity:0}}"
        ".bub{opacity:0;animation:bub 4s infinite}.b0{opacity:1}"
        "@keyframes bub{0%,40%{opacity:1}45%,100%{opacity:0}}"
        ".b1{animation-delay:1s}.b2{animation-delay:2s}.b3{animation-delay:3s}"
        ".call{animation:call 2.4s ease-in-out infinite}@keyframes call{50%{opacity:.55}}"
        ".link{animation:route 1.2s linear infinite}"
        ".dv{animation:dv 3s ease-in-out infinite}.d1{animation-delay:1s}.d2{animation-delay:2s}"
        "@keyframes dv{50%{fill-opacity:.15}}"
        ".beat{animation:beat 2.6s linear infinite}@keyframes beat{from{stroke-dashoffset:260}to{stroke-dashoffset:-260}}"
        ".blink{animation:blink 1.4s ease-in-out infinite}@keyframes blink{50%{opacity:.25}}"
    )
    title = "Productos de ZemZysteM: " + "; ".join(f'{p["name"]} ({p["kind"]})' for p in products)
    return svg(1200, h, screen_defs() + "".join(clips), "".join(bodies), title, style)
