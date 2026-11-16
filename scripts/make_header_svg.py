"""header.svg: createtim hero with drifting Sakura petals and Hase & Igel forecast."""

from theme import BG, BORDER, BRIGHT, DIM, FG, GOLD, KEY, MONO, MUTED, NODE, PETAL, ROSE, SERIF, WIDTH, esc, svg, write

HEIGHT = 230
OUT = "header"


def petals_svg():
    """Six subtle Sakura petals drifting diagonally via SMIL."""
    specs = [
        (95, -12, 235, 242, 11.0, 0.0, PETAL),
        (210, -12, 360, 242, 13.5, 2.2, ROSE),
        (330, -12, 465, 242, 10.5, 4.8, PETAL),
        (150, -12, 290, 242, 12.0, 6.5, PETAL),
        (410, -12, 535, 242, 14.0, 1.4, ROSE),
        (45, -12, 185, 242, 11.5, 8.0, PETAL),
    ]
    out = []
    for x0, y0, x1, y1, dur, begin, color in specs:
        path = f"M{x0},{y0} Q{(x0 + x1) / 2 + 18:.0f},{(y0 + y1) / 2:.0f} {x1},{y1}"
        timing = f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"'
        out.append(
            f'<g opacity="0">'
            f'<path d="M0,0 C4,-3 9,-1 10,2 C6,5 1,3 0,0 Z" fill="{color}">'
            f'<animateTransform attributeName="transform" type="rotate" '
            f'from="0 5 1" to="360 5 1" dur="{dur * 0.7:.1f}s" repeatCount="indefinite"/>'
            f'</path>'
            f'<animateMotion path="{path}" {timing}/>'
            f'<animate attributeName="opacity" values="0;0.55;0.55;0" keyTimes="0;0.12;0.88;1" {timing}/>'
            f'</g>'
        )
    return "".join(out)


def main():
    actual_pts = [
        (498, 160), (512, 152), (526, 139), (540, 143), (554, 126),
        (568, 131), (582, 112), (596, 119), (610, 102), (624, 104),
        (638, 113), (652, 108), (664, 114), (675, 118),
    ]
    actual_d = "M " + " L ".join(f"{x},{y}" for x, y in actual_pts)

    fc_pts = [
        (675, 118), (692, 122), (710, 125), (728, 124),
        (746, 120), (764, 114), (782, 106), (798, 100), (812, 96),
    ]
    band_top = [
        (675, 110), (692, 111), (710, 111), (728, 108),
        (746, 102), (764, 94), (782, 85), (798, 78), (812, 74),
    ]
    band_bot = [
        (812, 118), (798, 122), (782, 127), (764, 134),
        (746, 138), (728, 140), (710, 139), (692, 133), (675, 126),
    ]
    forecast_d = "M " + " L ".join(f"{x},{y}" for x, y in fc_pts)
    band_d = "M " + " L ".join(f"{x},{y}" for x, y in (band_top + band_bot)) + " Z"

    left_col = (
        f'<rect x="32" y="28" width="28" height="28" rx="8" fill="{ROSE}"/>'
        f'<text x="46" y="47" fill="#ffffff" font-size="14" font-weight="800" text-anchor="middle">c</text>'
        f'<text x="69" y="47" font-size="15.5" font-weight="700">'
        f'<tspan fill="{BRIGHT}">create</tspan><tspan fill="{KEY}">tim</tspan>'
        f'<tspan fill="{DIM}" font-weight="400" font-size="13"> · </tspan>'
        f'<tspan fill="{MUTED}" font-weight="500" font-size="13">Data Science · AI · Buxtehude</tspan>'
        f'</text>'
        f'<text x="32" y="84" fill="{MUTED}" font-size="14">Moin, I&#39;m</text>'
        f'<text x="32" y="118" fill="{KEY}" font-family="{SERIF}" font-size="34" font-weight="700">'
        f'{esc("Tim Lietzow")}</text>'
        f'<text x="32" y="152" fill="{FG}" font-size="14.5">'
        f'{esc("Data science, demand forecasting & custom web design")}</text>'
        f'<text x="32" y="174" fill="{FG}" font-size="14.5">'
        f'{esc("from Buxtehude — helping businesses plan ahead and")}</text>'
        f'<text x="32" y="196" fill="{FG}" font-size="14.5">'
        f'{esc("automate routine work.")}</text>'
    )

    # Hase at today (675, 118) and Igel waiting at forecast end (812, 96)
    hase = (
        f'<g transform="translate(668,107) scale(0.75)">'
        f'<ellipse cx="-10" cy="4" rx="13" ry="7" fill="{BRIGHT}"/>'
        f'<circle cx="5" cy="-2" r="6" fill="{BRIGHT}"/>'
        f'<ellipse cx="3" cy="-15" rx="2.6" ry="10" transform="rotate(-18 3 -15)" fill="{BRIGHT}"/>'
        f'<ellipse cx="8" cy="-14" rx="2.6" ry="10" transform="rotate(8 8 -14)" fill="{BRIGHT}"/>'
        f'<circle cx="7" cy="-3" r="1.2" fill="{BG}"/>'
        f'</g>'
    )
    igel = (
        f'<g transform="translate(808,94) scale(0.58) translate(-505,-164)">'
        f'<path fill="{ROSE}" d="M525.0 164.0 L533.3 157.6 L523.0 155.3 L527.7 145.9 L517.5 148.4 '
        f'L517.6 137.9 L509.5 144.5 L505.0 135.0 L500.5 144.5 L492.4 137.9 L492.5 148.4 '
        f'L482.3 145.9 L487.0 155.3 L476.7 157.6 L485.0 164.0 Z"/>'
        f'<path fill="{GOLD}" d="M487.0 164.0 Q473.0 161.0 470.0 165.0 Q479.0 168.0 487.0 164.0 Z"/>'
        f'<circle cx="481.0" cy="162.0" r="1.8" fill="{BRIGHT}"/>'
        f'<circle cx="470.0" cy="165.0" r="2.0" fill="{BRIGHT}"/>'
        f'</g>'
    )

    right_col = (
        f'<rect x="480" y="24" width="356" height="182" rx="10" fill="{NODE}" stroke="{BORDER}"/>'
        f'<text x="498" y="46" fill="{KEY}" font-size="11" font-weight="600" letter-spacing="0.04em">'
        f'{esc("DEMAND FORECAST · BUXTEHUDE")}</text>'
        f'<rect x="692" y="31" width="126" height="22" rx="11" fill="{BG}" stroke="{KEY}"/>'
        f'<text x="755" y="46" fill="{KEY}" font-family="{SERIF}" font-style="italic" '
        f'font-size="11.5" text-anchor="middle">{esc("Ick bün all hier!")}</text>'
        f'<path d="M498 82H816M498 114H816M498 146H816" fill="none" stroke="{BORDER}" stroke-width="1"/>'
        f'<path d="M498 176H816" fill="none" stroke="{DIM}" stroke-width="1"/>'
        f'<path d="M675 68V176" fill="none" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="3 3"/>'
        f'<path d="{band_d}" fill="{KEY}" fill-opacity="0.16"/>'
        f'<path d="{actual_d}" fill="none" stroke="{BRIGHT}" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{forecast_d}" fill="none" stroke="{KEY}" stroke-width="2.2" '
        f'stroke-dasharray="5 4" stroke-linecap="round"/>'
        f'{hase}{igel}'
        f'<circle cx="675" cy="118" r="3.5" fill="{GOLD}"/>'
        f'<circle cx="812" cy="96" r="3.5" fill="{KEY}"/>'
        f'<circle cx="812" cy="96" r="3.5" fill="none" stroke="{KEY}" opacity="0">'
        f'<animate attributeName="r" values="3.5;11" dur="2.2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.75;0" dur="2.2s" repeatCount="indefinite"/>'
        f'</circle>'
        f'<text x="498" y="194" fill="{MUTED}" font-family="{MONO}" font-size="10.5">actual sales</text>'
        f'<text x="675" y="194" fill="{GOLD}" font-family="{MONO}" font-size="10.5" text-anchor="middle">today</text>'
        f'<text x="812" y="194" fill="{KEY}" font-family="{MONO}" font-size="10.5" text-anchor="end">'
        f'{esc("forecast →")}</text>'
    )

    clip = f'<clipPath id="heroClip"><rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="13"/></clipPath>'
    write(OUT, svg(WIDTH, HEIGHT, f'{clip}<g clip-path="url(#heroClip)">{petals_svg()}</g>{left_col}{right_col}'))


if __name__ == "__main__":
    main()
