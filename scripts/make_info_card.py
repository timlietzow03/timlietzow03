"""The info half of neofetch.svg: createtim-styled profile, skills, path and languages.

Lines fade in on a stagger, then freeze - no loop. `both` (not `forwards`) and no base
opacity:0, so a renderer that ignores CSS animation still shows the card.
"""

from theme import BORDER, BRIGHT, FG, KEY, SERIF, esc

EYEBROW = "PROFILE · SKILLS & BACKGROUND"
TITLE = "What I work with"
ROWS = [
    ("Data & AI", [
        "Demand forecasting, causal ML & regression",
        "AI agents, RAG & local LLM workflows",
    ]),
    ("Software", [
        "Python, TypeScript, Next.js, Django, SQL",
        "Custom web design (fast, no cookie banner)",
    ]),
    ("Path", [
        "B.Sc. Computer Science (BHH, triple-track)",
        "Apprentice App Developer (bonprix AI team)",
        "Founder at createtim.de (Buxtehude)",
    ]),
    ("Languages", [
        "German (native), English (fluent)",
    ]),
]

CARD_W = 480
PAD = 24
VAL_X = 96
LINE = 27
GAP = 10
STEP = 0.07


def card(static, height):
    """Return (style, body) for a CARD_W x height area whose origin is its top-left."""
    body = []

    def line(i, content):
        if static:
            return f"<g>{content}</g>"
        return f'<g class="l" style="animation-delay:{i * STEP:.2f}s">{content}</g>'

    body.append(
        line(
            0,
            f'<text x="0" y="44" fill="{KEY}" font-size="11.5" font-weight="600" '
            f'letter-spacing="0.06em">{esc(EYEBROW)}</text>',
        )
    )
    body.append(
        line(
            1,
            f'<text x="0" y="74" fill="{BRIGHT}" font-family="{SERIF}" font-size="24" '
            f'font-weight="700">{esc(TITLE)}</text>',
        )
    )
    body.append(line(2, f'<path d="M0 90 H{CARD_W - 2 * PAD}" stroke="{BORDER}"/>'))

    y = 122
    n = 3
    for k, values in ROWS:
        for j, v in enumerate(values):
            key = (
                f'<text x="0" y="{y}" fill="{KEY}" font-size="13.5" font-weight="600">'
                f'{esc(k)}</text>'
            ) if j == 0 else ""
            body.append(line(n, f'{key}<text x="{VAL_X}" y="{y}" fill="{FG}" font-size="14">{esc(v)}</text>'))
            n += 1
            y += LINE
        y += GAP
    last = y - LINE - GAP

    assert last + PAD <= height, f"card overflows: needs {last + PAD}px, have {height}"
    longest = max(len(v) for _, values in ROWS for v in values)
    assert VAL_X + longest * 7.5 <= CARD_W - PAD, f"value too wide: {longest} chars"

    style = "" if static else (
        "<style>@keyframes fi{from{opacity:0;transform:translateY(4px)}"
        "to{opacity:1;transform:translateY(0)}}.l{animation:fi .45s ease-out both}</style>"
    )
    return style, f'<g transform="translate({PAD},0)">{"".join(body)}</g>'
