"""diagram: how Nae (Jarvis Local) processes a request offline on my PC.

Animated SMIL network path matching Tarek's SVG style: packets travel under node boxes
so they vanish inside each component while it processes them.
"""

from theme import ACCENT, BORDER, BRIGHT, DIM, FG, KEY, MUTED, NODE, WIDTH, esc, svg, write

TITLE = "How Nae (Jarvis Local) runs offline on my machine"
TITLE_H = 40  # px the title adds on top; the pipeline below shifts down by this much
HEIGHT = 250 + TITLE_H
MAIN_Y = 140  # center line before the vertical title shift
OUT = "diagram"


def node(x, y, w, label, color=FG):
    return (
        f'<rect x="{x}" y="{y - 16}" width="{w}" height="32" rx="6" fill="{NODE}" '
        f'stroke="{BORDER}"/><text x="{x + w / 2:.0f}" y="{y + 5}" fill="{color}" '
        f'text-anchor="middle">{esc(label)}</text>'
    )


def small(x, y, s, anchor="middle"):
    return f'<text x="{x}" y="{y}" fill="{MUTED}" font-size="12" text-anchor="{anchor}">{esc(s)}</text>'


def packet(path, dur, begin):
    """A dot running forward along `path`. Hidden without SMIL."""
    timing = f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"'
    return (
        f'<circle r="3.5" fill="{ACCENT}" opacity="0">'
        f'<animateMotion path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="linear" {timing}/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" {timing}/>'
        f'</circle>'
    )


def main():
    you_x, you_w = 24, 96
    stt_x, stt_w = 176, 120
    llm_x, llm_w = 344, 148
    fork_x, br_x, br_w = 516, 540, 132
    upper_y, lower_y = 92, 188
    merge_x, tts_x, tts_w = 694, 714, 112

    you_c, you_r = you_x + you_w / 2, you_x + you_w
    tts_c = tts_x + tts_w / 2

    to_vault = f"M{you_c:.0f},{MAIN_Y} H{fork_x} V{upper_y} H{merge_x} V{MAIN_Y} H{tts_c:.0f}"
    to_tools = f"M{you_c:.0f},{MAIN_Y} H{fork_x} V{lower_y} H{merge_x} V{MAIN_Y} H{tts_c:.0f}"
    line = f'fill="none" stroke="{DIM}"'

    network = (
        # Local machine boundary: everything inside runs offline on my own PC.
        f'<rect x="152" y="24" width="688" height="210" rx="8" fill="none" stroke="{BORDER}" '
        f'stroke-dasharray="6 5"/>' + small(168, 44, "my PC (100% local & offline)", "start")
        + f'<path d="M{you_r},{MAIN_Y} H{stt_x}" {line}/>'
        + f'<path d="M{stt_x + stt_w},{MAIN_Y} H{llm_x}" {line}/>'
        + f'<path d="M{llm_x + llm_w},{MAIN_Y} H{fork_x} V{upper_y} H{br_x}" {line}/>'
        + f'<path d="M{llm_x + llm_w},{MAIN_Y} H{fork_x} V{lower_y} H{br_x}" {line}/>'
        + f'<path d="M{br_x + br_w},{upper_y} H{merge_x} V{MAIN_Y} H{tts_x}" {line}/>'
        + f'<path d="M{br_x + br_w},{lower_y} H{merge_x} V{MAIN_Y} H{tts_x}" {line}/>'
        + packet(to_vault, 3.4, 0.0)
        + packet(to_tools, 3.4, 1.7)
        + node(you_x, MAIN_Y, you_w, "you", BRIGHT)
        + small(you_c, MAIN_Y + 34, "voice / keys")
        + node(stt_x, MAIN_Y, stt_w, "Whisper STT", KEY)
        + small(stt_x + stt_w / 2, MAIN_Y + 34, "speech to text")
        + node(llm_x, MAIN_Y, llm_w, "router & Ollama", KEY)
        + small(llm_x + llm_w / 2, MAIN_Y + 34, "local LLM (Qwen)")
        + node(br_x, upper_y, br_w, "second brain")
        + small(br_x + br_w / 2, upper_y + 34, "BM25 + vault notes")
        + node(br_x, lower_y, br_w, "local tools")
        + small(br_x + br_w / 2, lower_y + 34, "tasks, UI, briefs")
        + node(tts_x, MAIN_Y, tts_w, "Piper TTS", ACCENT)
        + small(tts_c, MAIN_Y + 34, "spoken reply")
    )
    body = (
        f'<text x="24" y="34" fill="{BRIGHT}" font-weight="600">{esc(TITLE)}</text>'
        f'<g transform="translate(0,{TITLE_H})">{network}</g>'
    )
    write(OUT, svg(WIDTH, HEIGHT, body, font_size=14))


if __name__ == "__main__":
    main()
