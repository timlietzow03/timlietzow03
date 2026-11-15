"""Project cards: one SVG per project, so each card can link to its own site.

An SVG inside <img> cannot hold its own links, hence one file per card; the links
themselves live in README.md. Each card carries a live light, refreshed hourly by
.github/workflows/update-status.yml. Rule for this list: only public URLs or strictly
local non-sensitive projects.

The caption under the grid holds the check date, so a file changes at least daily: that
commit keeps the schedule alive (GitHub disables schedules after 60 quiet days) and
tells visitors how fresh the lights are.

--demo renders test cards per state and verifies all project cards without touching the network.
"""

import urllib.error
import urllib.request
from datetime import datetime, timezone

from theme import ACCENT, BRIGHT, DANGER, DIM, KEY, MUTED, WIDTH, esc, svg, write

PROJECTS = [  # (slug, name, description lines, url or None, display domain or None)
    (
        "createtim",
        "createtim",
        ["Data science, demand forecasting", "and custom web design for SMBs."],
        "https://createtim.de",
        "createtim.de",
    ),
    (
        "forecast",
        "Bread Roll Forecast",
        ["Short-term bakery demand model", "using sales, weather and holidays."],
        "https://createtim.de/en/notebook-bread-roll-forecast.html",
        "createtim.de/en/notebook",
    ),
    (
        "helium-start",
        "helium-start",
        ["Personal browser startpage with silos,", "daylight modes and command palette."],
        "https://timlietzow03.github.io/helium-start/",
        "github.io/helium-start",
    ),
    (
        "nae",
        "Nae (Jarvis Local)",
        ["Local voice and vault assistant", "with Whisper, Ollama and Piper TTS."],
        None,
        None,
    ),
]
CARD_W, CARD_H = 425, 140
PAD = 24

STATES = {  # state: (colour, label)
    "up": (ACCENT, "online"),
    "down": (DANGER, "offline"),
    "soon": (MUTED, "local-only, runs offline on my PC"),
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


def card(name, lines, url, domain, state):
    color, label = STATES[state]
    dot_y = CARD_H - 26
    pulse = (
        f'<circle cx="{PAD + 4}" cy="{dot_y}" r="4.5" fill="none" stroke="{color}" opacity="0">'
        f'<animate attributeName="r" values="4.5;10" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.7;0" dur="2s" repeatCount="indefinite"/>'
        f'</circle>'
    ) if state == "up" else ""
    status = f'<text x="{PAD + 18}" y="{dot_y + 5}" fill="{color}">{esc(label)}</text>'
    if domain:
        status += (
            f'<text x="{CARD_W - PAD}" y="{dot_y + 5}" fill="{KEY}" '
            f'text-anchor="end">{esc(domain)}</text>'
        )
    body = (
        f'<text x="{PAD}" y="40" fill="{BRIGHT}" font-size="18" font-weight="700">{esc(name)}</text>'
        + (
            f'<text x="{CARD_W - PAD}" y="40" fill="{ACCENT}" font-size="18" text-anchor="end">↗</text>'
            if url else ""
        )
        + "".join(
            f'<text x="{PAD}" y="{66 + i * 20}" fill="{MUTED}">{esc(l)}</text>'
            for i, l in enumerate(lines)
        )
        + f'<circle cx="{PAD + 4}" cy="{dot_y}" r="4.5" fill="{color}"/>{pulse}{status}'
    )
    assert len(lines) <= 2, f"{name}: description has room for two lines"
    # ~8.4px per glyph at 14px monospace
    assert all(PAD + len(l) * 8.4 <= CARD_W - PAD for l in lines), f"{name}: line too long"
    return svg(CARD_W, CARD_H, body, font_size=14)


def caption(checked):
    text = esc(f"Live status, checked {checked} (UTC), refreshes hourly.")
    return svg(
        WIDTH,
        28,
        f'<text x="{WIDTH / 2:.0f}" y="18" fill="{DIM}" font-size="12" '
        f'text-anchor="middle">{text}</text>',
        framed=False,
    )


def main():
    for slug, name, lines, url, domain in PROJECTS:
        # One retry, so a single dropped request doesn't paint a card red for an hour.
        state = "soon" if url is None else ("up" if is_up(url) or is_up(url) else "down")
        write(f"project-{slug}", card(name, lines, url, domain, state), f" ({state})")
    write("projects-caption", caption(datetime.now(timezone.utc).date().isoformat()))


def demo():
    up = card("Up", ["line"], "https://example.org", "example.org", "up")
    down = card("Down", ["line"], "https://example.org", "example.org", "down")
    soon = card("Soon", ["line"], None, None, "soon")
    assert ">online<" in up and "<animate" in up and "example.org" in up
    assert ">offline<" in down and "<animate" not in down
    assert "↗" not in soon and "example.org" not in soon, "a card without url must not look clickable"
    for _, name, lines, url, domain in PROJECTS:
        card(name, lines, url, domain, "soon" if url is None else "up")
    assert "2026-01-01" in caption("2026-01-01")
    print("ok: up/down/soon cards, all project cards, and caption render as expected")


if __name__ == "__main__":
    import sys

    demo() if "--demo" in sys.argv else main()
