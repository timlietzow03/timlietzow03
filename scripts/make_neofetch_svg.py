"""neofetch.svg: a rotating shaded 3D ASCII cube on the left, the info card on the right.

GitHub strips <script> from READMEs but does play SMIL inside SVGs served via <img>,
so every cube frame is baked in as a <g> and cycled with <animate calcMode="discrete">.
One SVG instead of two side by side: a README <table> draws grey cell borders and
insets its images, so they never line up with the full-width panels above and below.

STATIC=1 emits a frozen frame for previewing. --demo runs the self-checks.
"""

import math
import os

from make_info_card import CARD_W, card
from theme import FG, WIDTH, esc, svg, write

# --- cube geometry ---
L = 1.45  # cube half-side length
K2 = 6.0  # viewer distance
SURF_STEP = 0.03
RAMP = ".,-~:;=!*#$@"  # dark -> bright

# --- light direction (normalized) ---
_LX, _LY, _LZ = -0.35, 0.65, -0.67
_LNORM = math.sqrt(_LX * _LX + _LY * _LY + _LZ * _LZ)
LIGHT = (_LX / _LNORM, _LY / _LNORM, _LZ / _LNORM)

# --- output grid ---
RAW_COLS, RAW_ROWS = 76, 44
TARGET_COLS, TARGET_ROWS = 50, 26  # 50 * 7 + 28 = 378 px; 378 + 482 = 860 == WIDTH
CHAR_W, CHAR_H = 7.0, 14.0  # monospace cell: twice as tall as wide
SPAN = 42  # approximate width span in columns
FRAMES = 90
DURATION = 9.0  # seconds per loop
PAD = 14.0
OUT = "neofetch"


def frange(start, stop, step):
    n = int(round((stop - start) / step)) + 1
    return (start + i * step for i in range(n))


def angles(i):
    """Seamless loop with initial 3D tilt so multiple faces show from frame 0."""
    t = 2 * math.pi * i / FRAMES
    return 0.58 + t, 0.72 + 2 * t, 0.32


def rotate(x, y, z, ca, sa, cb, sb, cc, sc):
    # X rotation
    y1 = y * ca - z * sa
    z1 = y * sa + z * ca
    # Y rotation
    x2 = x * cb + z1 * sb
    z2 = -x * sb + z1 * cb
    # Z rotation
    x3 = x2 * cc - y1 * sc
    y3 = x2 * sc + y1 * cc
    return x3, y3, z2


def render_frame(a, b, c):
    """One projected frame of the 3D cube, as a list of RAW_ROWS strings."""
    grid = [[" "] * RAW_COLS for _ in range(RAW_ROWS)]
    zbuf = [[0.0] * RAW_COLS for _ in range(RAW_ROWS)]

    kx = 49.0
    ky = kx * (CHAR_W / CHAR_H)

    ca, sa = math.cos(a), math.sin(a)
    cb, sb = math.cos(b), math.sin(b)
    cc, sc = math.cos(c), math.sin(c)

    faces = (
        (lambda u, v: (u, v, L), (0.0, 0.0, 1.0)),
        (lambda u, v: (u, v, -L), (0.0, 0.0, -1.0)),
        (lambda u, v: (L, v, u), (1.0, 0.0, 0.0)),
        (lambda u, v: (-L, v, u), (-1.0, 0.0, 0.0)),
        (lambda u, v: (u, L, v), (0.0, 1.0, 0.0)),
        (lambda u, v: (u, -L, v), (0.0, -1.0, 0.0)),
    )

    lx, ly, lz = LIGHT
    coords = list(frange(-L, L, SURF_STEP))

    for pt_fn, (nx, ny, nz) in faces:
        wnx, wny, wnz = rotate(nx, ny, nz, ca, sa, cb, sb, cc, sc)
        # Normal points from camera at (0,0,-K2) when dot with face center is positive; skip back faces.
        cx, cy, cz = rotate(nx * L, ny * L, nz * L, ca, sa, cb, sb, cc, sc)
        if wnx * cx + wny * cy + wnz * (K2 + cz) >= 0:
            continue
        dot = wnx * lx + wny * ly + wnz * lz
        shade = 0.22 + 0.78 * max(0.0, dot)
        face_ch = RAMP[min(int(shade * (len(RAMP) - 1)), len(RAMP) - 1)]

        for u in coords:
            edge_u = abs(u) >= L - 0.11
            for v in coords:
                px, py, pz = pt_fn(u, v)
                rx, ry, rz = rotate(px, py, pz, ca, sa, cb, sb, cc, sc)
                z = K2 + rz
                ooz = 1.0 / z
                xp = int(RAW_COLS / 2 + kx * ooz * rx)
                yp = int(RAW_ROWS / 2 - ky * ooz * ry)
                if not (0 <= xp < RAW_COLS and 0 <= yp < RAW_ROWS):
                    continue
                is_edge = edge_u or abs(v) >= L - 0.11
                eff_ooz = ooz + (0.003 if is_edge else 0.0)
                if eff_ooz > zbuf[yp][xp]:
                    zbuf[yp][xp] = eff_ooz
                    grid[yp][xp] = "@" if is_edge else face_ch

    return ["".join(row) for row in grid]


def fit_frames(frames):
    """Crop to the union bounding box across all frames and center in TARGET_ROWS x TARGET_COLS."""
    top, bottom, left, right = RAW_ROWS, -1, RAW_COLS, -1
    for lines in frames:
        for r, line in enumerate(lines):
            stripped = line.rstrip()
            if not stripped:
                continue
            top, bottom = min(top, r), max(bottom, r)
            left = min(left, len(line) - len(line.lstrip()))
            right = max(right, len(stripped) - 1)
    assert bottom >= top and right >= left, "nothing drawn in any frame"

    used_h = bottom - top + 1
    used_w = right - left + 1
    assert used_h <= TARGET_ROWS and used_w <= TARGET_COLS, (
        f"cube {used_w}x{used_h} exceeds target {TARGET_COLS}x{TARGET_ROWS}"
    )

    pad_top = (TARGET_ROWS - used_h) // 2
    pad_left = (TARGET_COLS - used_w) // 2
    pad_right = TARGET_COLS - used_w - pad_left
    blank_row = " " * TARGET_COLS

    fitted = []
    for lines in frames:
        out = [blank_row] * pad_top
        for l in lines[top : bottom + 1]:
            out.append((" " * pad_left) + l[left : right + 1] + (" " * pad_right))
        while len(out) < TARGET_ROWS:
            out.append(blank_row)
        fitted.append(out)
    return fitted


def rows_svg(lines, cols):
    # textLength pins each row's width so alignment survives any monospace font.
    return "".join(
        f'<text x="0" y="{(i + 1) * CHAR_H:.0f}" textLength="{cols * CHAR_W:.0f}" '
        f'lengthAdjust="spacingAndGlyphs">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )


def frame_svg(index, lines, cols):
    """A frame group, visible only during its slice of the loop."""
    lo, hi = index / FRAMES, (index + 1) / FRAMES
    if index == 0:
        values, times = "inline;none", f"0;{hi:.5f}"
    elif index == FRAMES - 1:
        values, times = "none;inline", f"0;{lo:.5f}"
    else:
        values, times = "none;inline;none", f"0;{lo:.5f};{hi:.5f}"

    return (
        f'<g display="none">{rows_svg(lines, cols)}'
        f'<animate attributeName="display" calcMode="discrete" values="{values}" '
        f'keyTimes="{times}" dur="{DURATION}s" repeatCount="indefinite"/></g>'
    )


def main():
    static = os.environ.get("STATIC") == "1"
    frames = fit_frames([render_frame(*angles(i)) for i in range(FRAMES)])
    rows, cols = len(frames[0]), len(frames[0][0])
    logo_w, height = cols * CHAR_W + 2 * PAD, rows * CHAR_H + 2 * PAD
    assert logo_w + CARD_W == WIDTH, f"logo {logo_w:.0f} + card {CARD_W} != {WIDTH}"

    style, card_body = card(static, height)
    logo = (
        rows_svg(frames[0], cols)
        if static
        else "".join(frame_svg(i, f, cols) for i, f in enumerate(frames))
    )
    write(
        OUT,
        svg(
            WIDTH,
            height,
            f'{style}<g transform="translate({PAD:.0f},{PAD:.0f})" font-size="{CHAR_H * 0.82:.1f}" '
            f'fill="{FG}">{logo}</g>'
            f'<g transform="translate({logo_w:.0f},0)">{card_body}</g>',
        ),
        f", {1 if static else FRAMES} frame(s), cube {cols}x{rows} chars, {WIDTH}x{height:.0f} px"
        f"{' (static)' if static else ''}",
    )


def demo():
    """Sanity check: loop is seamless, cube fits cleanly, and card dimensions match."""
    raw = [render_frame(*angles(i)) for i in range(FRAMES)]
    a0, b0, c0 = angles(0)
    af, bf, cf = angles(FRAMES)
    assert math.isclose(math.cos(a0), math.cos(af)) and math.isclose(math.sin(a0), math.sin(af))
    assert math.isclose(math.cos(b0), math.cos(bf)) and math.isclose(math.sin(b0), math.sin(bf))
    assert math.isclose(c0, cf)
    assert all(len(f) == RAW_ROWS and all(len(l) == RAW_COLS for l in f) for f in raw)

    frames = fit_frames(raw)
    rows, cols = len(frames[0]), len(frames[0][0])
    assert rows == TARGET_ROWS and cols == TARGET_COLS
    logo_w, height = cols * CHAR_W + 2 * PAD, rows * CHAR_H + 2 * PAD
    assert logo_w + CARD_W == WIDTH
    card(False, height)

    filled = sum(c != " " for l in frames[0] for c in l)
    assert 100 < filled < rows * cols * 0.75, f"implausible fill: {filled}"
    print("\n".join(frames[0]))
    print(f"ok: {cols}x{rows}, {filled} glyphs in frame 0, {WIDTH}x{height:.0f} px")


if __name__ == "__main__":
    import sys

    demo() if "--demo" in sys.argv else main()
