"""diagram.svg: how Nae (Jarvis Local) processes requests offline in createtim style."""

from theme import BORDER, BRIGHT, DIM, FG, GOLD, KEY, MONO, MUTED, NODE, SERIF, WIDTH, esc, svg, write

EYEBROW = "ARCHITECTURE · LOCAL AI"
TITLE = "How Nae (Jarvis Local) runs offline on my PC"
TITLE_H = 56
HEIGHT = 310
MAIN_Y = 128
OUT = "diagram"


def node(x, y, w, label, color=FG):
    return (
        f'<rect x="{x}" y="{y - 16}" width="{w}" height="32" rx="8" fill="{NODE}" '
        f'stroke="{BORDER}"/><text x="{x + w / 2:.0f}" y="{y + 5}" fill="{color}" '
        f'font-size="13.5" font-weight="500" text-anchor="middle">{esc(label)}</text>'
    )


def small(x, y, s, anchor="middle", mono=False):
    ff = f' font-family="{MONO}"' if mono else ""
    return f'<text x="{x}" y="{y}" fill="{MUTED}"{ff} font-size="11.5" text-anchor="{anchor}">{esc(s)}</text>'


def packet(path, dur, begin, color):
    """A dot running forward along `path`. Hidden without SMIL."""
    timing = f'dur="{dur}s" begin="{begin}s" repeatCount="indefinite"'
    return (
        f'<circle r="3.8" fill="{color}" opacity="0">'
        f'<animateMotion path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="linear" {timing}/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" {timing}/>'
        f'</circle>'
    )


def main():
    you_x, you_w = 28, 92
    stt_x, stt_w = 176, 120
    llm_x, llm_w = 344, 148
    fork_x, br_x, br_w = 516, 540, 132
    upper_y, lower_y = 82, 174
    merge_x, tts_x, tts_w = 694, 714, 112

    you_c, you_r = you_x + you_w / 2, you_x + you_w
    tts_c = tts_x + tts_w / 2

    to_vault = f"M{you_c:.0f},{MAIN_Y} H{fork_x} V{upper_y} H{merge_x} V{MAIN_Y} H{tts_c:.0f}"
    to_tools = f"M{you_c:.0f},{MAIN_Y} H{fork_x} V{lower_y} H{merge_x} V{MAIN_Y} H{tts_c:.0f}"
    line = f'fill="none" stroke="{DIM}" stroke-width="1.3"'

    network = (
        f'<rect x="152" y="16" width="688" height="204" rx="10" fill="none" stroke="{BORDER}" '
        f'stroke-dasharray="6 5"/>' + small(168, 35, "my PC · 100% local & offline", "start", mono=True)
        + f'<path d="M{you_r},{MAIN_Y} H{stt_x}" {line}/>'
        + f'<path d="M{stt_x + stt_w},{MAIN_Y} H{llm_x}" {line}/>'
        + f'<path d="M{llm_x + llm_w},{MAIN_Y} H{fork_x} V{upper_y} H{br_x}" {line}/>'
        + f'<path d="M{llm_x + llm_w},{MAIN_Y} H{fork_x} V{lower_y} H{br_x}" {line}/>'
        + f'<path d="M{br_x + br_w},{upper_y} H{merge_x} V{MAIN_Y} H{tts_x}" {line}/>'
        + f'<path d="M{br_x + br_w},{lower_y} H{merge_x} V{MAIN_Y} H{tts_x}" {line}/>'
        + packet(to_vault, 3.4, 0.0, KEY)
        + packet(to_tools, 3.4, 1.7, GOLD)
        + node(you_x, MAIN_Y, you_w, "you", BRIGHT)
        + small(you_c, MAIN_Y + 32, "voice / keys")
        + node(stt_x, MAIN_Y, stt_w, "Whisper STT", KEY)
        + small(stt_x + stt_w / 2, MAIN_Y + 32, "speech to text")
        + node(llm_x, MAIN_Y, llm_w, "router & Ollama", KEY)
        + small(llm_x + llm_w / 2, MAIN_Y + 32, "local LLM (Qwen)")
        + node(br_x, upper_y, br_w, "second brain", FG)
        + small(br_x + br_w / 2, upper_y + 32, "BM25 + vault notes")
        + node(br_x, lower_y, br_w, "local tools", FG)
        + small(br_x + br_w / 2, lower_y + 32, "tasks, UI, briefs")
        + node(tts_x, MAIN_Y, tts_w, "Piper TTS", GOLD)
        + small(tts_c, MAIN_Y + 32, "spoken reply")
    )

    body = (
        f'<text x="28" y="32" fill="{KEY}" font-size="11.5" font-weight="600" '
        f'letter-spacing="0.06em">{esc(EYEBROW)}</text>'
        f'<text x="28" y="58" fill="{BRIGHT}" font-family="{SERIF}" font-size="22" '
        f'font-weight="700">{esc(TITLE)}</text>'
        f'<g transform="translate(0,{TITLE_H})">{network}</g>'
        f'<text x="430" y="296" fill="{MUTED}" font-family="{MONO}" font-size="11" '
        f'text-anchor="middle">{esc("fig. 5 — voice in, local LLM routing + second-brain retrieval, spoken reply out")}</text>'
    )
    write(OUT, svg(WIDTH, HEIGHT, body))


if __name__ == "__main__":
    main()
