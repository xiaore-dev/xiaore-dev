"""Draw both editions of the profile cover. Run with Python 3, no packages needed."""

from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets"
DIGITS = "1975544"
PAPER = "#f4efdf"
INK = "#153d39"
JADE = "#427c70"
VERMILION = "#cf492f"

# A hand-drawn plan view of a cloud. The same edge acts as a printing plate
# for the silhouettes, relief faces and contour cuts.
CLOUD = (
    "M-236 6 C-249-10-240-28-220-36 C-209-41-198-42-182-40 "
    "C-184-61-164-77-140-78 C-121-80-105-73-96-65 "
    "C-85-88-60-100-34-98 C-8-99 12-87 19-71 "
    "C42-86 79-84 97-68 C107-64 112-58 115-51 "
    "C143-64 178-53 186-32 C211-37 240-24 243-5 "
    "C247 12 233 25 214 31 C222 50 202 66 176 68 "
    "C160 70 146 66 134 61 C123 82 84 92 57 80 "
    "C38 95 10 100-18 92 C-33 89-42 82-48 75 "
    "C-78 90-114 82-127 66 C-156 77-189 67-197 46 "
    "C-225 43-242 27-236 6Z"
)


def cloud(attributes):
    return f'<use xlink:href="#plate" {attributes}/>'


def definitions():
    return f"""<defs>
  <path id="plate" d="{CLOUD}"/>
  <pattern id="edge-cuts" width="5" height="5" patternUnits="userSpaceOnUse">
    <path d="M-1 2L2-1M1 5L6 0M4 7L7 4" stroke="{PAPER}" stroke-width="1.15"/>
  </pattern>
  <pattern id="fibres" width="47" height="53" patternUnits="userSpaceOnUse">
    <path d="M3 9l2-.5m16 8l.7.3m13 17l2-.3m-24 12l1-.3" stroke="{INK}" stroke-width="0.7" opacity=".12"/>
    <path d="M5 30l2 .6m22-25l.9-.3m12 38l1.7-.5" stroke="white" stroke-width="1" opacity=".34"/>
  </pattern>
  <clipPath id="sun"><circle cx="164" cy="-93" r="80"/></clipPath>
</defs>"""


def relief():
    # The leading digit controls the top sheet. Work back-to-front, from
    # the last digit upward. Its value changes the registration and width.
    sheets = []
    for index in reversed(range(len(DIGITS))):
        digit = int(DIGITS[index])
        x = 2 * (digit - 5) - index * 1.5
        y = index * 17
        scale = 1 - index * 0.047 + digit * 0.005
        face = [PAPER, "#b6c8ae", JADE, PAPER, "#9fb7a1", JADE, PAPER][index]
        parts = [
            f'<g transform="translate({x} {y}) matrix({scale:.3f} -0.13 0.31 {0.65 * scale:.3f} 0 0)" stroke-linejoin="round">',
            cloud(f'transform="translate(0 12)" fill="{INK}" stroke="{INK}" stroke-width="3"'),
            cloud('transform="translate(0 12)" fill="url(#edge-cuts)"'),
            cloud(f'fill="{face}" stroke="{INK}" stroke-width="2.8"'),
        ]
        if index == 0:
            # The shifting centers give the carved rings a shallow saddle.
            for ring in range(1, 13):
                k = 1 - ring * 0.072
                dx = ring * 4.2
                dy = -ring * 0.85
                weight = 2.4 if ring % 3 else 3.8
                parts.append(cloud(f'transform="translate({dx:.1f} {dy:.1f}) scale({k:.3f})" '
                                   f'fill="none" stroke="{INK}" stroke-width="{weight / k:.2f}"'))
            parts.append(cloud(f'transform="translate(53 -11) scale(.085)" fill="{INK}"'))
        else:
            parts.append(cloud(f'transform="scale(.957)" fill="none" stroke="{INK}" stroke-width="1.6"'))
        parts.append("</g>")
        sheets.append("\n    ".join(parts))
    return "\n  ".join(sheets)


def illustration():
    # Long tapered incisions follow the curve of the disc.
    incisions = []
    for line in range(12):
        y = -99 + line * 6
        incisions.append(f'<path d="M76 {y}q83-9 176-2q-93-1-176 4Z"/>')
    return f"""<circle cx="164" cy="-93" r="80" fill="{VERMILION}"/>
  <g clip-path="url(#sun)" fill="{PAPER}">
    {''.join(incisions)}
  </g>
  {relief()}"""


def signature(x, y, size):
    # Seven cut marks share the seven offsets of the handle.
    cuts = []
    for index, digit in enumerate(DIGITS):
        left = 5.5 + index * 3.4
        top = 15 - int(digit) * 0.9
        cuts.append(f'<path d="M{left:.1f} {top:.1f}v{22 - top:.1f}" stroke="{PAPER}" stroke-width="1.7"/>')
    return f"""<g transform="translate({x} {y}) scale({size})">
  <rect width="32" height="30" rx="2" fill="{VERMILION}"/>
  {''.join(cuts)}
  <text x="45" y="21.5" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="18" fill="{INK}">x{DIGITS}-cloud</text>
</g>"""


def draw(compact):
    width, height = (500, 475) if compact else (1120, 440)
    mark = signature(26, 24, 0.97) if compact else signature(46, 32, 1.05)
    art = "translate(278 260) scale(.80)" if compact else "translate(800 200) scale(.98)"
    title_x, title_y, title_size = (22, 162, 132) if compact else (39, 259, 184)
    subtitle_y = 202 if compact else 317
    subtitle_size = 23 if compact else 31
    margin, rule_y = (27, 405) if compact else (47, 376)
    footer_y = rule_y + 37
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">x{DIGITS}-cloud · 七层云版画</title>
<desc id="desc">七张带有刻纹的云形版片悬叠在朱红日轮前。自上而下，各层的宽度和错位由 {DIGITS} 依次决定。</desc>
{definitions()}
<rect width="{width}" height="{height}" fill="{PAPER}"/>
{mark}
<text x="{title_x}" y="{title_y}" font-family="Georgia, 'Times New Roman', serif" font-style="italic" font-size="{title_size}" letter-spacing="-6" fill="{INK}">cloud</text>
<text x="{margin}" y="{subtitle_y}" font-family="'Songti SC', 'Noto Serif CJK SC', SimSun, serif" font-weight="600" font-size="{subtitle_size}" letter-spacing="2" fill="{INK}">七层云版画</text>
<g transform="{art}">
  {illustration()}
</g>
<g fill="{INK}" font-family="ui-monospace, Menlo, Consolas, monospace" font-size="{17 if compact else 19}">
  <path d="M{margin} {rule_y}H{width-margin}" fill="none" stroke="{INK}" stroke-width="1.3"/>
  <text x="{margin}" y="{footer_y}" letter-spacing="{1 if compact else 2}">SEVEN IMPRESSIONS</text>
  <text x="{width-margin}" y="{footer_y}" text-anchor="end" letter-spacing="2">{' '.join(DIGITS)}</text>
</g>
<rect width="{width}" height="{height}" fill="url(#fibres)"/>
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, compact in [("cloud-press.svg", False), ("cloud-press-mobile.svg", True)]:
        (ASSETS / name).write_text(draw(compact), encoding="utf-8")
