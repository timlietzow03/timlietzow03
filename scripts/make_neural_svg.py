"""neural.svg: animated 4-layer neural network forward pass in createtim style."""

from theme import BORDER, BRIGHT, DIM, FG, GOLD, KEY, MONO, MUTED, NODE, PETAL, ROSE, SERIF, WIDTH, esc, svg, write

EYEBROW = "DEEP LEARNING · FORWARD PASS"
TITLE = "Signal propagation"
HEIGHT = 260
OUT = "neural"


def main():
    layers = [
        [(396, 68), (396, 108), (396, 148), (396, 188)],
        [(526, 48), (526, 80), (526, 112), (526, 144), (526, 176), (526, 208)],
        [(656, 58), (656, 94), (656, 130), (656, 166), (656, 202)],
        [(776, 84), (776, 130), (776, 176)],
    ]
    layer_colors = [KEY, ROSE, KEY, GOLD]

    edges = []
    for l_idx in range(len(layers) - 1):
        for x1, y1 in layers[l_idx]:
            for x2, y2 in layers[l_idx + 1]:
                edges.append(
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{DIM}" stroke-width="0.8" stroke-opacity="0.45"/>'
                )

    # Curated forward-pass signal pulses cascading layer by layer over a 3.6s cycle
    pulses = []
    cycle = 3.6
    hop_paths = [
        # Layer 0 -> 1 (0.0s .. 1.0s)
        (0, 0, 1, 0.00, KEY), (0, 1, 2, 0.08, GOLD), (0, 2, 3, 0.14, KEY),
        (0, 3, 4, 0.20, PETAL), (0, 1, 1, 0.25, KEY), (0, 2, 5, 0.30, GOLD),
        # Layer 1 -> 2 (0.9s .. 1.9s)
        (1, 0, 0, 0.90, KEY), (1, 2, 1, 0.96, GOLD), (1, 3, 2, 1.02, KEY),
        (1, 4, 3, 1.08, PETAL), (1, 1, 2, 1.14, KEY), (1, 5, 4, 1.20, GOLD),
        # Layer 2 -> 3 (1.8s .. 2.8s)
        (2, 0, 0, 1.80, GOLD), (2, 1, 1, 1.88, KEY), (2, 2, 1, 1.94, GOLD),
        (2, 3, 2, 2.00, PETAL), (2, 4, 2, 2.06, GOLD),
    ]
    for l_idx, i_src, i_dst, delay, color in hop_paths:
        x1, y1 = layers[l_idx][i_src]
        x2, y2 = layers[l_idx + 1][i_dst]
        path = f"M{x1},{y1} L{x2},{y2}"
        # Visible only during its ~0.95s flight within the 3.6s cycle
        t0 = delay / cycle
        t1 = (delay + 0.95) / cycle
        t_mid1 = (delay + 0.12) / cycle
        t_mid2 = (delay + 0.83) / cycle
        kt = f"0;{t0:.3f};{t_mid1:.3f};{t_mid2:.3f};{t1:.3f};1"
        kp = f"0;0;0.15;0.85;1;1"
        op = "0;0;1;1;0;0"
        pulses.append(
            f'<circle r="3" fill="{color}" opacity="0">'
            f'<animateMotion path="{path}" keyPoints="{kp}" keyTimes="{kt}" calcMode="linear" '
            f'dur="{cycle}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op}" keyTimes="{kt}" '
            f'dur="{cycle}s" repeatCount="indefinite"/>'
            f'</circle>'
        )

    neurons = []
    for l_idx, pts in enumerate(layers):
        c = layer_colors[l_idx]
        for x, y in pts:
            neurons.append(
                f'<circle cx="{x}" cy="{y}" r="6.5" fill="{NODE}" stroke="{c}" stroke-width="2"/>'
            )
            if l_idx == 3:
                neurons.append(
                    f'<circle cx="{x}" cy="{y}" r="6.5" fill="none" stroke="{GOLD}" opacity="0">'
                    f'<animate attributeName="r" values="6.5;14" dur="{cycle}s" begin="2.5s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0;0.75;0" keyTimes="0;0.2;1" dur="{cycle}s" '
                    f'begin="2.5s" repeatCount="indefinite"/>'
                    f'</circle>'
                )

    left_col = (
        f'<text x="28" y="42" fill="{KEY}" font-size="11.5" font-weight="600" '
        f'letter-spacing="0.06em">{esc(EYEBROW)}</text>'
        f'<text x="28" y="72" fill="{BRIGHT}" font-family="{SERIF}" font-size="22" '
        f'font-weight="700">{esc(TITLE)}</text>'
        f'<text x="28" y="106" fill="{FG}" font-size="13.8">'
        f'{esc("Inspired by my 3D Blender neural net")}</text>'
        f'<text x="28" y="126" fill="{FG}" font-size="13.8">'
        f'{esc("on createtim.de: activations travel")}</text>'
        f'<text x="28" y="146" fill="{FG}" font-size="13.8">'
        f'{esc("layer by layer from inputs to output.")}</text>'
        f'<rect x="28" y="168" width="280" height="26" rx="6" fill="{NODE}" stroke="{BORDER}"/>'
        f'<text x="168" y="185" fill="{MUTED}" font-family="{MONO}" font-size="11" '
        f'text-anchor="middle">{esc("4 inputs → 6 hidden → 5 hidden → 3 outputs")}</text>'
        f'<text x="28" y="232" fill="{MUTED}" font-family="{MONO}" font-size="11">'
        f'{esc("fig. 4 — forward pass across 4 layers")}</text>'
    )

    stage = (
        f'<rect x="336" y="20" width="500" height="220" rx="10" fill="{NODE}" stroke="{BORDER}"/>'
        + "".join(edges)
        + "".join(pulses)
        + "".join(neurons)
    )

    write(OUT, svg(WIDTH, HEIGHT, left_col + stage))


if __name__ == "__main__":
    main()
