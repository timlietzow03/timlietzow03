"""linienplan.svg: Tim's transit-line map (L, D, W) in Sakura & Nightbloom style."""

from theme import ACCENT, BG, BORDER, BRIGHT, DIM, GOLD, KEY, MONO, MUTED, NODE, SERIF, WIDTH, esc, svg, write

EYEBROW = "TRANSIT MAP · MY PATH & WORK"
TITLE = "Seven stations, three still running"
HEIGHT = 286
OUT = "linienplan"


def badge(x, y, letter, color):
    return (
        f'<circle cx="{x}" cy="{y}" r="11" fill="{color}"/>'
        f'<text x="{x}" y="{y + 4}" fill="{BG}" font-family="{MONO}" font-size="11.5" '
        f'font-weight="700" text-anchor="middle">{esc(letter)}</text>'
    )


def station(x, y, label, sub, color, active=False, interchange=False, label_pos="top"):
    if interchange:
        ring = (
            f'<circle cx="{x}" cy="{y}" r="10.5" fill="{BG}" stroke="{BRIGHT}" stroke-width="2.5"/>'
            f'<circle cx="{x}" cy="{y}" r="4.5" fill="{color}"/>'
        )
    elif active:
        ring = (
            f'<circle cx="{x}" cy="{y}" r="7.5" fill="{color}" stroke="{BG}" stroke-width="2"/>'
            f'<circle cx="{x}" cy="{y}" r="7.5" fill="none" stroke="{color}" opacity="0">'
            f'<animate attributeName="r" values="7.5;15" dur="2.4s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.75;0" dur="2.4s" repeatCount="indefinite"/>'
            f'</circle>'
        )
    else:
        ring = f'<circle cx="{x}" cy="{y}" r="7" fill="{BG}" stroke="{color}" stroke-width="2.5"/>'

    if label_pos == "top":
        txt = (
            f'<text x="{x}" y="{y - 18}" fill="{BRIGHT}" font-size="12" font-weight="600" '
            f'text-anchor="middle">{esc(label)}</text>'
            + (
                f'<text x="{x}" y="{y - 33}" fill="{GOLD if active or interchange else MUTED}" '
                f'font-family="{MONO}" font-size="10" text-anchor="middle">{esc(sub)}</text>'
                if sub else ""
            )
        )
    elif label_pos == "bottom":
        txt = (
            f'<text x="{x}" y="{y + 24}" fill="{BRIGHT}" font-size="12" font-weight="600" '
            f'text-anchor="middle">{esc(label)}</text>'
        )
    else:  # left
        txt = (
            f'<text x="{x - 16}" y="{y + 4}" fill="{BRIGHT}" font-size="12" font-weight="600" '
            f'text-anchor="end">{esc(label)}</text>'
        )
    return ring + txt


def pulse_dot(path, dur, begin, color):
    timing = f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"'
    return (
        f'<circle r="3.2" fill="{BRIGHT}" stroke="{color}" stroke-width="1.5" opacity="0">'
        f'<animateMotion path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="linear" {timing}/>'
        f'<animate attributeName="opacity" values="0;0.95;0.95;0" keyTimes="0;0.08;0.92;1" {timing}/>'
        f'</circle>'
    )


def main():
    header = (
        f'<text x="28" y="32" fill="{KEY}" font-size="11.5" font-weight="600" '
        f'letter-spacing="0.06em">{esc(EYEBROW)}</text>'
        f'<text x="28" y="58" fill="{BRIGHT}" font-family="{SERIF}" font-size="22" '
        f'font-weight="700">{esc(TITLE)}</text>'
        # Legend chips top-right
        + badge(534, 42, "L", KEY)
        + f'<text x="550" y="46" fill="{MUTED}" font-size="12">Path</text>'
        + badge(606, 42, "D", GOLD)
        + f'<text x="622" y="46" fill="{MUTED}" font-size="12">Data &amp; AI</text>'
        + badge(708, 42, "W", ACCENT)
        + f'<text x="724" y="46" fill="{MUTED}" font-size="12">Web &amp; Software</text>'
    )

    grid = (
        f'<defs><pattern id="tgrid" width="32" height="32" patternUnits="userSpaceOnUse">'
        f'<path d="M32 0H0V32" fill="none" stroke="{BORDER}" stroke-width="0.7" opacity="0.55"/>'
        f'</pattern></defs>'
        f'<rect x="24" y="72" width="812" height="184" rx="10" fill="{NODE}" fill-opacity="0.45" '
        f'stroke="{BORDER}"/>'
        f'<rect x="24" y="72" width="812" height="184" rx="10" fill="url(#tgrid)"/>'
    )

    path_l = "M62,132 H768"
    path_d = "M650,132 V174 L604,220 H220"
    path_w = "M768,132 V220 H684"

    lines = (
        f'<path d="{path_l}" fill="none" stroke="{KEY}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="{path_d}" fill="none" stroke="{GOLD}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{path_w}" fill="none" stroke="{ACCENT}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>'
        + badge(62, 132, "L", KEY)
        + badge(650, 174, "D", GOLD)
        + badge(768, 174, "W", ACCENT)
    )

    trains = (
        pulse_dot(path_l, 5.5, 0.0, KEY)
        + pulse_dot(path_d, 4.2, 1.2, GOLD)
        + pulse_dot(path_w, 3.0, 2.0, ACCENT)
    )

    stations = (
        station(128, 132, "Dorsten", "born", KEY)
        + station(228, 132, "Gahlen, NRW", "grew up", KEY)
        + station(328, 132, "Buxtehude", "base", KEY)
        + station(434, 132, "Apprenticeship", "running", KEY, active=True)
        + station(540, 132, "B.Sc. CS", "running", KEY, active=True)
        + station(650, 132, "AI team", "running", KEY, interchange=True)
        + station(768, 132, "Taiwan", "2026", KEY, interchange=True)
        + station(530, 220, "Bread Roll Forecast", "", GOLD, label_pos="bottom")
        + station(380, 220, "Nae (Local AI)", "", GOLD, active=True, label_pos="bottom")
        + station(220, 220, "Neural Net (Blender)", "", GOLD, label_pos="bottom")
        + station(768, 198, "Sanxia Explorer", "", ACCENT, label_pos="left")
        + station(684, 220, "createtim.de", "", ACCENT, active=True, label_pos="bottom")
    )

    caption = (
        f'<text x="430" y="275" fill="{MUTED}" font-family="{MONO}" font-size="11" '
        f'text-anchor="middle">'
        f'{esc("fig. 2 — seven stations from Dorsten to Buxtehude & Taiwan; pulsing rings are still running")}'
        f'</text>'
    )

    write(OUT, svg(WIDTH, HEIGHT, header + grid + lines + trains + stations + caption))


if __name__ == "__main__":
    main()
