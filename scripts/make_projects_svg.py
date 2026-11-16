"""Project cards: createtim-styled section header, 2x2 cards with stack tags, and fig. 3 caption.

An SVG inside <img> cannot hold its own links, hence one file per card; the links
themselves live in README.md. Each card carries a live light, refreshed hourly by
.github/workflows/update-status.yml.

--demo renders and checks section header, all states, all project cards, and caption
without touching the network.
"""

import urllib.error
import urllib.request
from datetime import datetime, timezone

from theme import ACCENT, BORDER, BRIGHT, DANGER, FG, GOLD, KEY, MONO, MUTED, NODE, SERIF, WIDTH, esc, svg, write

PROJECTS = [
    # (slug, category, name, description lines, stack tags, url or None, display domain or None)
    (
        "createtim",
        "DATA SCIENCE & WEB",
        "createtim",
        ["Data science, demand forecasting", "and custom web design for SMBs."],
        ["HTML/CSS", "Vanilla JS", "Playwright CI"],
        "https://createtim.de",
        "createtim.de",
    ),
    (
        "forecast",
        "DEMAND FORECASTING",
        "Bread Roll Forecast",
        ["Short-term bakery demand model", "using sales, weather and holidays."],
        ["Python", "Time Series", "80% Interval"],
        "https://createtim.de/en/notebook-bread-roll-forecast.html",
        "createtim.de/en/notebook",
    ),
    (
        "helium-start",
        "BROWSER TOOLING",
        "helium-start",
        ["Personal browser startpage with silos,", "daylight modes and command palette."],
        ["JavaScript", "Zero-Build", "GitHub Pages"],
        "https://timlietzow03.github.io/helium-start/",
        "github.io/helium-start",
    ),
    (
        "nae",
        "LOCAL AI AGENT",
        "Nae (Jarvis Local)",
        ["Local voice and vault assistant", "with Whisper, Ollama and Piper TTS."],
        ["Python", "Whisper", "Ollama", "Piper"],
        None,
        None,
    ),
]
CARD_W, CARD_H = 425, 166
PAD = 24

STATES = {  # state: (colour, label)
    "up": (ACCENT, "online"),
    "down": (DANGER, "offline"),
    "soon": (GOLD, "local-only · runs offline on my PC"),
}


def is_up(url):
    """Up = the server answered below 500."""
    req = urllib.request.Request(url, headers={"User-Agent": "timlietzow03-profile-status"})
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True
    except urllib.error.HTTPError as e:
        return e.code < 500
    except (urllib.error.URLError, OSError):
        return False


def projects_header():
    body = (
        f'<text x="4" y="18" fill="{KEY}" font-size="11.5" font-weight="600" '
        f'letter-spacing="0.06em">{esc("APPLICATIONS & PROJECTS")}</text>'
        f'<text x="4" y="46" fill="{BRIGHT}" font-family="{SERIF}" font-size="22" '
        f'font-weight="700">{esc("Selected work & live demos")}</text>'
    )
    return svg(WIDTH, 56, body, framed=False)


def tags_svg(tags, y):
    x = PAD
    parts = []
    for tag in tags:
        w = round(len(tag) * 6.5 + 14)
        parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="20" rx="5" fill="{NODE}" stroke="{BORDER}"/>'
            f'<text x="{x + w / 2:.1f}" y="{y + 13.5}" fill="{MUTED}" font-family="{MONO}" '
            f'font-size="10.5" text-anchor="middle">{esc(tag)}</text>'
        )
        x += w + 6
    assert x - 6 <= CARD_W - PAD, f"tags overflow card width: {x}"
    return "".join(parts)


def card(category, name, lines, tags, url, domain, state):
    color, label = STATES[state]
    dot_y = CARD_H - 20
    pulse = (
        f'<circle cx="{PAD + 4}" cy="{dot_y}" r="4.5" fill="none" stroke="{color}" opacity="0">'
        f'<animate attributeName="r" values="4.5;10" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.7;0" dur="2s" repeatCount="indefinite"/>'
        f'</circle>'
    ) if state == "up" else ""
    status = f'<text x="{PAD + 18}" y="{dot_y + 4.5}" fill="{color}" font-size="13">{esc(label)}</text>'
    if domain:
        status += (
            f'<text x="{CARD_W - PAD}" y="{dot_y + 4.5}" fill="{KEY}" font-family="{MONO}" '
            f'font-size="12" text-anchor="end">{esc(domain)}</text>'
        )
    body = (
        f'<text x="{PAD}" y="25" fill="{KEY}" font-size="10" font-weight="600" '
        f'letter-spacing="0.07em">{esc(category)}</text>'
        f'<text x="{PAD}" y="49" fill="{BRIGHT}" font-family="{SERIF}" font-size="18.5" '
        f'font-weight="700">{esc(name)}</text>'
        + (
            f'<text x="{CARD_W - PAD}" y="49" fill="{KEY}" font-size="18" text-anchor="end">↗</text>'
            if url else ""
        )
        + "".join(
            f'<text x="{PAD}" y="{73 + i * 19}" fill="{FG}" font-size="13.5">{esc(l)}</text>'
            for i, l in enumerate(lines)
        )
        + tags_svg(tags, 106)
        + f'<circle cx="{PAD + 4}" cy="{dot_y}" r="4.5" fill="{color}"/>{pulse}{status}'
    )
    assert len(lines) <= 2, f"{name}: description has room for two lines"
    assert all(PAD + len(l) * 7.5 <= CARD_W - PAD for l in lines), f"{name}: line too long"
    return svg(CARD_W, CARD_H, body, rx=14)


def caption(checked):
    text = esc(f"fig. 3 — live status, checked {checked} (UTC), refreshed hourly")
    return svg(
        WIDTH,
        28,
        f'<text x="{WIDTH / 2:.0f}" y="18" fill="{MUTED}" font-family="{MONO}" font-size="11.5" '
        f'text-anchor="middle">{text}</text>',
        framed=False,
    )


def main():
    write("projects-header", projects_header())
    for slug, category, name, lines, tags, url, domain in PROJECTS:
        state = "soon" if url is None else ("up" if is_up(url) or is_up(url) else "down")
        write(f"project-{slug}", card(category, name, lines, tags, url, domain, state), f" ({state})")
    write("projects-caption", caption(datetime.now(timezone.utc).date().isoformat()))


def demo():
    hdr = projects_header()
    assert "APPLICATIONS &amp; PROJECTS" in hdr and "Selected work &amp; live demos" in hdr
    up = card("CAT", "Up", ["line"], ["Python"], "https://example.org", "example.org", "up")
    down = card("CAT", "Down", ["line"], ["Python"], "https://example.org", "example.org", "down")
    soon = card("CAT", "Soon", ["line"], ["Python"], None, None, "soon")
    assert ">online<" in up and "<animate" in up and "example.org" in up
    assert ">offline<" in down and "<animate" not in down
    assert "↗" not in soon and "example.org" not in soon, "a card without url must not look clickable"
    for _, category, name, lines, tags, url, domain in PROJECTS:
        card(category, name, lines, tags, url, domain, "soon" if url is None else "up")
    assert "2026-01-01" in caption("2026-01-01") and "fig. 3" in caption("2026-01-01")
    print("ok: projects header, all card states, stack tags, all project cards, and fig. 3 caption")


if __name__ == "__main__":
    import sys

    demo() if "--demo" in sys.argv else main()
