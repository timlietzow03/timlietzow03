"""The info half of neofetch.svg: name, then skills, stack, track and languages.

Lines fade in on a stagger, then freeze - no loop. `both` (not `forwards`) and no base
opacity:0, so a renderer that ignores CSS animation still shows the card.
"""

from theme import ACCENT, DIM, FG, KEY, esc

TITLE = "Tim Lietzow"
ROWS = [
    ("Skills", [
        "AI agents & local LLM workflows",
        "Data science & demand forecasting",
        "Causal ML & regression analysis",
        "Full-stack web (Next.js, Django)",
        "Custom web design & automation",
    ]),
    ("Stack", ["Python, TypeScript, SQL, Docker"]),
    ("Track", [
        "B.Sc. Computer Science (BHH, trial)",
        "Apprentice App Developer (bonprix)",
        "Founder at createtim.de",
    ]),
    ("Lang", ["German, English"]),
]

CARD_W = 482
PAD = 22
VAL_X = 96
FONT_SIZE = 15
LINE = 25  # px between lines
GAP = 6  # extra px before each new key
STEP = 0.07  # seconds between line reveals


def card(static, height):
    """Return (style, body) for a CARD_W x height area whose origin is its top-left."""
    body = []

    def line(i, content):
        if static:
            return f"<g>{content}</g>"
        return f'<g class="l" style="animation-delay:{i * STEP:.2f}s">{content}</g>'

    y = PAD + 24
    body.append(line(0, f'<text x="0" y="{y}" fill="{ACCENT}" font-weight="600">{esc(TITLE)}</text>'))
    y += 14
    body.append(line(1, f'<path d="M0 {y} H{CARD_W - 2 * PAD}" stroke="{DIM}"/>'))
    y += 30
    n = 2
    for k, values in ROWS:
        for j, v in enumerate(values):
            key = f'<text x="0" y="{y}" fill="{KEY}">{esc(k)}</text>' if j == 0 else ""
            body.append(line(n, f'{key}<text x="{VAL_X}" y="{y}" fill="{FG}">{esc(v)}</text>'))
            n += 1
            y += LINE
        y += GAP
    last = y - LINE - GAP

    # The last row must sit inside the panel, or the card silently clips.
    assert last + PAD <= height, f"card overflows: needs {last + PAD}px, have {height}"
    # ~9px per glyph at 15px monospace; a longer value runs past the right border.
    longest = max(len(v) for _, values in ROWS for v in values)
    assert VAL_X + longest * 9 <= CARD_W - 2 * PAD, f"value too wide: {longest} chars"

    style = "" if static else (
        "<style>@keyframes fi{from{opacity:0;transform:translateY(4px)}"
        "to{opacity:1;transform:translateY(0)}}.l{animation:fi .45s ease-out both}</style>"
    )
    return style, (
        f'<g transform="translate({PAD},0)" font-size="{FONT_SIZE}">'
        + "".join(body) + "</g>"
    )
