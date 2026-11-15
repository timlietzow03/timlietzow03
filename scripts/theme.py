"""Shared createtim visual system: Sakura (light) and Nightbloom (dark) palettes.

Scripts draw using the Nightbloom (dark) tokens; write() saves img/<name>-dark.svg
and swaps each dark hex for its Sakura (light) partner to create img/<name>-light.svg.
The README picks one per viewer via <picture> + prefers-color-scheme.
"""

import os

FONT = "Inter,system-ui,-apple-system,'Segoe UI',sans-serif"
SERIF = "Georgia,'Times New Roman','Noto Serif',serif"
MONO = "ui-monospace,'SF Mono','Cascadia Code',Menlo,Consolas,monospace"

DARK = {
    "bg": "#181122",      # Nightbloom background
    "node": "#231934",    # Card / inner surface
    "border": "#3d2c52",  # Subtle plum border
    "bright": "#f4ebf3",  # Primary headline ink
    "fg": "#d8c8d6",      # Body ink
    "muted": "#a78fa4",   # Muted copy
    "dim": "#6e5873",     # Axes & grid lines
    "key": "#ef8ab8",     # Sakura pink (--brand)
    "rose": "#c95f92",    # Deep rose (--accent)
    "petal": "#f7b8d0",   # Soft petal pink
    "gold": "#f0c56a",    # Stamen gold (--stamen)
    "accent": "#7fd4a8",  # Online mint green (--ok-ink)
    "danger": "#f85149",  # Offline red
}
LIGHT = {
    "bg": "#faf9f7",      # Warm Sakura paper
    "node": "#f3f0ed",    # Soft warm surface
    "border": "#e4dce1",  # Hairline border
    "bright": "#231c20",  # Deep anthracite ink
    "fg": "#4b4247",      # Soft ink
    "muted": "#6b6166",   # Muted warm grey
    "dim": "#9a8f94",     # Axes & grid lines
    "key": "#b22e69",     # Deep sakura (--brand-700)
    "rose": "#e0518c",    # Vibrant sakura (--brand)
    "petal": "#f2a3c8",   # Light petal pink
    "gold": "#d99a2b",    # Stamen gold (--stamen)
    "accent": "#3d8a64",  # Online green (--ok-ink)
    "danger": "#cf222e",  # Offline red
}

# The swap is a plain text replace, so no dark hex may repeat or reappear as a light one.
assert len(set(DARK.values())) == len(DARK) and not set(DARK.values()) & set(LIGHT.values())

BG, NODE, BORDER = DARK["bg"], DARK["node"], DARK["border"]
BRIGHT, FG, MUTED, DIM = DARK["bright"], DARK["fg"], DARK["muted"], DARK["dim"]
KEY, ROSE, PETAL, GOLD = DARK["key"], DARK["rose"], DARK["petal"], DARK["gold"]
ACCENT, DANGER = DARK["accent"], DARK["danger"]

WIDTH = 860
OUT_DIR = "img"


def esc(s, nbsp=False):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s.replace(" ", "\u00a0") if nbsp else s


def svg(w, h, body, framed=True, rx=14, **attrs):
    extra = "".join(f' {k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    frame = (
        f'<rect x="0.5" y="0.5" width="{w - 1:.0f}" height="{h - 1:.0f}" rx="{rx}" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    ) if framed else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
        f'width="{w:.0f}" height="{h:.0f}" font-family="{FONT}"{extra}>{frame}{body}</svg>'
    )


def to_light(dark_svg):
    for role, hex_ in DARK.items():
        dark_svg = dark_svg.replace(hex_, LIGHT[role])
    return dark_svg


def write(name, dark_svg, note=""):
    """Save img/<name>-dark.svg and img/<name>-light.svg."""
    os.makedirs(OUT_DIR, exist_ok=True)
    for variant, content in (("dark", dark_svg), ("light", to_light(dark_svg))):
        with open(os.path.join(OUT_DIR, f"{name}-{variant}.svg"), "w", encoding="utf-8") as f:
            f.write(content)
    print(f"{OUT_DIR}/{name}-{{dark,light}}.svg: {len(dark_svg) / 1024:.1f} KB{note}")
