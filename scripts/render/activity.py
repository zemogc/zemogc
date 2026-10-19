"""CH 03 — Señal: ciudad isométrica con las contribuciones reales del último año."""

from __future__ import annotations

import math
from datetime import date, timedelta

from .kit import MONO, SANS, SCREEN, channel, device, live_badge, screen_defs, screen_overlay, svg, text

W, H = 1200, 640
MONTHS = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

# Proyección: una semana avanza hacia la derecha, un día hacia el espectador.
ORIGIN = (118, 262)
U = (19.0, 4.2)
V = (-9.0, 8.5)
MAX_TOWER = 150
GAP = 0.12

# Rampa secuencial de un solo tono (cian), de menos a más actividad.
EMPTY = "#0F1723"
RAMP = ["#0E5266", "#0E7C97", "#19B4D2", "#67E8F9"]


def stats(github: dict | None) -> dict | None:
    if not github:
        return None
    days = [d for week in github["weeks"] for d in week]
    counts = [d["count"] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    current = 0
    tail = counts[:-1] if counts and counts[-1] == 0 else counts
    for c in reversed(tail):
        if not c:
            break
        current += 1
    best = max(days, key=lambda d: d["count"]) if days else {"count": 0, "date": ""}
    return {
        "total": sum(counts),
        "active": sum(1 for c in counts if c),
        "longest": longest,
        "current": current,
        "best": best,
        "repos": github.get("public_repos", 0),
        "updated": github["generated_at"][:10],
    }


def point(w: float, d: float, lift: float = 0) -> tuple[float, float]:
    return ORIGIN[0] + w * U[0] + d * V[0], ORIGIN[1] + w * U[1] + d * V[1] - lift


def poly(points: list[tuple[float, float]], fill: str) -> str:
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in points)}" fill="{fill}"/>'


def shade(color: str, factor: float) -> str:
    return "#" + "".join(f"{round(int(color[i:i + 2], 16) * factor):02X}" for i in (1, 3, 5))


def placeholder_weeks() -> list[list[dict]]:
    # Rejilla vacía y determinista mientras no exista data/github.json.
    start = date(2025, 10, 19)
    return [[{"date": (start + timedelta(days=w * 7 + d)).isoformat(), "count": 0} for d in range(7)]
            for w in range(53)]


def city(weeks: list[list[dict]]) -> str:
    peak = max((d["count"] for wk in weeks for d in wk), default=0) or 1
    body = ""
    for w, week in enumerate(weeks):
        for day in week:
            d = date.fromisoformat(day["date"]).isoweekday() % 7  # domingo = 0, como GitHub
            count = day["count"]
            w0, w1, d0, d1 = w + GAP, w + 1 - GAP, d + GAP, d + 1 - GAP
            if not count:
                body += poly([point(w0, d0), point(w1, d0), point(w1, d1), point(w0, d1)], EMPTY)
                continue
            level = min(3, math.ceil(4 * count / peak) - 1)
            top = RAMP[level]
            h = max(6.0, MAX_TOWER * math.sqrt(count / peak))
            body += (
                f'<g class="t" style="animation-delay:{w * 0.018:.2f}s">'
                + poly([point(w0, d1), point(w1, d1), point(w1, d1, h), point(w0, d1, h)], shade(top, 0.62))
                + poly([point(w1, d0), point(w1, d1), point(w1, d1, h), point(w1, d0, h)], shade(top, 0.42))
                + poly([point(w0, d0, h), point(w1, d0, h), point(w1, d1, h), point(w0, d1, h)], top)
                + "</g>"
            )
    labels, seen = "", None
    for w, week in enumerate(weeks):
        month = date.fromisoformat(week[0]["date"]).month
        if month != seen and w < len(weeks) - 2:
            x, y = point(w + 0.5, 7.9)
            labels += text(x, y + 14, MONTHS[month - 1], size=12, fill=SCREEN["muted"], font=MONO, spacing=1.5)
            seen = month
    return body + labels


def build(data: dict, theme: dict) -> str:
    s = SCREEN
    github = data.get("github")
    st = stats(github)
    weeks = github["weeks"] if github else placeholder_weeks()

    frame, box = device(0, 0, W, H, theme)
    ix, iy, iw, ih = box
    head = (
        channel(ix + 34, iy + 40, 3, "Señal · actividad en GitHub")
        + live_badge(ix + iw - 28, iy + 40, "EN VIVO" if st else "SINCRONIZANDO")
        + text(ix + 34, iy + 92, "Contribuciones de los últimos 12 meses,", size=17, fill=s["text"],
               attrs=' fill-opacity="0.85"')
        + text(ix + 34, iy + 116, "públicas y privadas, día por día.", size=17, fill=s["text"],
               attrs=' fill-opacity="0.85"')
    )

    # Panel de cifras.
    rx = 760
    if st:
        big = f'{st["total"]:,}'.replace(",", ".")
        best = st["best"]
        best_label = f'{best["count"]} · {date.fromisoformat(best["date"]).day} {MONTHS[date.fromisoformat(best["date"]).month - 1]}' \
            if best["date"] else "—"
        cells = [
            (str(st["active"]), "DÍAS ACTIVOS"),
            (f'{st["longest"]} d', "RACHA MÁXIMA"),
            (f'{st["current"]} d', "RACHA ACTUAL"),
            (best_label, "DÍA RÉCORD"),
        ]
    else:
        big = "—"
        cells = [("—", "DÍAS ACTIVOS"), ("—", "RACHA MÁXIMA"), ("—", "RACHA ACTUAL"), ("—", "DÍA RÉCORD")]
    panel = (
        text(rx, iy + 132, big, size=76, fill="url(#brand)", font=SANS, weight=800, spacing=-2)
        + text(rx + 4, iy + 160, "CONTRIBUCIONES · 12 MESES", size=12, fill=s["muted"], font=MONO, weight=600,
               spacing=2)
    )
    for i, (value, label) in enumerate(cells):
        cx = rx + (i % 2) * 196
        cy = iy + 206 + (i // 2) * 58
        panel += (
            f'<rect x="{cx - 2}" y="{cy - 26}" width="3" height="40" rx="1.5" fill="{s["cyan"]}" fill-opacity="0.7"/>'
            + text(cx + 12, cy, value, size=24, fill=s["text"], font=MONO, weight=700)
            + text(cx + 12, cy + 18, label, size=11, fill=s["muted"], font=MONO, weight=600, spacing=1.5)
        )

    legend_x = ix + iw - 220
    legend_y = iy + ih - 30
    legend = text(legend_x - 10, legend_y, "menos", size=12, fill=s["muted"], font=MONO, anchor="end")
    for i, c in enumerate([EMPTY] + RAMP):
        legend += f'<rect x="{legend_x + i * 22}" y="{legend_y - 12}" width="16" height="16" rx="3" fill="{c}"/>'
    legend += text(legend_x + 5 * 22 + 4, legend_y, "más", size=12, fill=s["muted"], font=MONO)
    footer = text(ix + 34, iy + ih - 30,
                  f'actualizado {st["updated"]} · github actions' if st else "esperando la primera sincronización",
                  size=12, fill=s["dim"], font=MONO)

    defs = screen_defs() + f'<clipPath id="scr"><rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="14"/></clipPath>'
    body = (
        frame + '<g clip-path="url(#scr)">' + head + panel + city(weeks) + legend + footer
        + screen_overlay(box) + "</g>"
    )
    style = (
        ".t{transform-box:fill-box;transform-origin:50% 100%;animation:rise .9s cubic-bezier(.2,.8,.2,1) both}"
        "@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
        ".blink{animation:blink 1.4s ease-in-out infinite}@keyframes blink{50%{opacity:.25}}"
    )
    if st:
        title = (f'{st["total"]} contribuciones en los últimos 12 meses; {st["active"]} días activos; '
                 f'racha máxima de {st["longest"]} días; día récord con {st["best"]["count"]}.')
    else:
        title = "Actividad en GitHub: sincronizando."
    return svg(W, H, defs, body, title, style)
