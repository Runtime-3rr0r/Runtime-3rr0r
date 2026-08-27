#!/usr/bin/env python3
"""Turn an ASCII-art text file into ascii.svg — a self-typing portrait.

Preserves the art exactly (leading spaces, ragged rows). Same visual language
as make_portrait.py: mono rows revealed by clipPath wipes with a cursor block,
frozen at the end. Reads rows as-is; reveals each row in sequence.
"""
import base64, os, sys

CHAR_W = 7.74
FONT_SIZE = 12.9
LINE_H = 15
ROW_DELAY = 0.09      # per-row stagger, seconds
PAD = 14
FG_LIGHT = "#6e7681"
FG_DARK = "#c9d1d9"
FAMILY = ("JBMono,ui-monospace,SFMono-Regular,Menlo,Consolas,"
          "&apos;Liberation Mono&apos;,monospace")
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "fonts", "jbmono-ramp.woff2")

def build(lines):
    lines = [l.rstrip() for l in lines]
    width = max((len(l) for l in lines), default=1)
    height = len(lines) * LINE_H + PAD * 2
    with open(FONT, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    rule = (f"@font-face{{font-family:JBMono;font-style:normal;font-weight:400;"
            f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAD*2+width*CHAR_W:.0f}" '
         f'height="{height:.0f}" viewBox="0 0 {PAD*2+width*CHAR_W:.0f} {height:.0f}" '
         f'fill="none" font-family="{FAMILY}">',
         f'<style>{rule}.a{{fill:{FG_LIGHT}}}'
         f'@media(prefers-color-scheme:dark){{.a{{fill:{FG_DARK}}}}}</style>']
    for i, line in enumerate(lines):
        y = PAD + i * LINE_H
        begin = f"{i * ROW_DELAY:.2f}s"
        w = len(line) * CHAR_W
        safe = (line.replace("&", "&amp;").replace("<", "&lt;").
                replace(">", "&gt;"))
        p.append(f'<clipPath id="c{i}"><rect x="{PAD}" y="{y}" height="{LINE_H}" width="0">'
                 f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{begin}" '
                 f'dur="{ROW_DELAY}s" fill="freeze"/></rect></clipPath>')
        p.append(f'<g clip-path="url(#c{i})"><text xml:space="preserve" x="{PAD}" '
                 f'y="{y + 11.2:.1f}" class="a" font-size="{FONT_SIZE}">{line if line else " "}</text></g>')
        p.append(f'<rect y="{y + 1}" width="6" height="12" class="a" opacity="0">'
                 f'<animate attributeName="x" from="{PAD}" to="{PAD + w:.1f}" begin="{begin}" '
                 f'dur="{ROW_DELAY}s" fill="freeze"/><set attributeName="opacity" to="0.8" begin="{begin}"/>'
                 f'<set attributeName="opacity" to="0" begin="{i*ROW_DELAY+ROW_DELAY:.2f}s"/></rect>')
    p.append("</svg>")
    return "".join(p)

def main():
    src = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "ascii.svg"
    lines = open(src, encoding="utf-8").read().splitlines()
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    svg = build(lines)
    open(out, "w", encoding="utf-8").write(svg)
    print(f"wrote {out} — {len(lines)} rows")

if __name__ == "__main__":
    main()