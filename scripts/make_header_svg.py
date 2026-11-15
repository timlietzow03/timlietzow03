"""header.svg: createtim-styled hero card with brand mark and Hase & Igel demand forecast."""

from theme import BG, BORDER, BRIGHT, DIM, FG, GOLD, KEY, MONO, MUTED, NODE, ROSE, SERIF, WIDTH, esc, svg, write

HEIGHT = 230
OUT = "header"


def main():
    # Actual sales curve (x: 498 -> 675, y: 160 -> 118)
    actual_pts = [
        (498, 160), (512, 152), (526, 139), (540, 143), (554, 126),
        (568, 131), (582, 112), (596, 119), (610, 102), (624, 104),
        (638, 113), (652, 108), (664, 114), (675, 118),
    ]
    actual_d = "M " + " L ".join(f"{x},{y}" for x, y in actual_pts)

    # Forecast curve (x: 675 -> 812, y: 118 -> 96) and 80% uncertainty band
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

    right_col = (
        f'<rect x="480" y="24" width="356" height="182" rx="10" fill="{NODE}" stroke="{BORDER}"/>'
        f'<text x="498" y="46" fill="{KEY}" font-size="11" font-weight="600" letter-spacing="0.04em">'
        f'{esc("DEMAND FORECAST · BUXTEHUDE")}</text>'
        f'<rect x="692" y="31" width="126" height="22" rx="11" fill="{BG}" stroke="{KEY}"/>'
        f'<text x="755" y="46" fill="{KEY}" font-family="{SERIF}" font-style="italic" '
        f'font-size="11.5" text-anchor="middle">{esc("Ick bün all hier!")}</text>'
        # Grid lines + baseline + today marker
        f'<path d="M498 82H816M498 114H816M498 146H816" fill="none" stroke="{BORDER}" stroke-width="1"/>'
        f'<path d="M498 176H816" fill="none" stroke="{DIM}" stroke-width="1"/>'
        f'<path d="M675 68V176" fill="none" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="3 3"/>'
        # Forecast interval + actual & forecast lines
        f'<path d="{band_d}" fill="{KEY}" fill-opacity="0.16"/>'
        f'<path d="{actual_d}" fill="none" stroke="{BRIGHT}" stroke-width="2.2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<path d="{forecast_d}" fill="none" stroke="{KEY}" stroke-width="2.2" '
        f'stroke-dasharray="5 4" stroke-linecap="round"/>'
        # Today marker & animated forecast endpoint
        f'<circle cx="675" cy="118" r="3.8" fill="{GOLD}"/>'
        f'<circle cx="812" cy="96" r="4" fill="{KEY}"/>'
        f'<circle cx="812" cy="96" r="4" fill="none" stroke="{KEY}" opacity="0">'
        f'<animate attributeName="r" values="4;11" dur="2.2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.75;0" dur="2.2s" repeatCount="indefinite"/>'
        f'</circle>'
        # Axis labels
        f'<text x="498" y="194" fill="{MUTED}" font-family="{MONO}" font-size="10.5">actual sales</text>'
        f'<text x="675" y="194" fill="{GOLD}" font-family="{MONO}" font-size="10.5" text-anchor="middle">today</text>'
        f'<text x="812" y="194" fill="{KEY}" font-family="{MONO}" font-size="10.5" text-anchor="end">'
        f'{esc("forecast →")}</text>'
    )

    write(OUT, svg(WIDTH, HEIGHT, left_col + right_col))


if __name__ == "__main__":
    main()
