"""Draw the two Agent Lab plates. The SVG attributes also define a still edition."""
from math import cos, radians, sin
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "lab"
BLUE, TEAL, INK = "#2457E6", "#009F91", "#182433"
RULE, MUTED, PAPER = "#D7E0EA", "#53667D", "#F6F8FA"
SANS = "Inter,Helvetica Neue,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"
STAGES = ("Perceive", "Reason", "Act", "Observe", "Loop")
FIELDS = ("Agent Architecture", "LLM Inference", "Context Engineering", "Tool Calling",
          "MCP", "RAG", "Software Engineering")


def xy(point):
    return ",".join(f"{v:.2f}" for v in point)


def poly(points):
    return "M" + " ".join(xy(p) for p in points) + "Z"


def path(d, stroke="none", fill="none", width=1, extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" {extra}/>'


def label(x, y, words, size, color=INK, weight=500, mono=False, align="start", space=0):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{MONO if mono else SANS}" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="{space}" '
            f'text-anchor="{align}">{words}</text>')


def folio(x, y, n):
    return label(x, y, f"/ {n:02}", 17, BLUE, 650, mono=True, space=-.8)


def frame(w, h, title, desc, body, background="white"):
    content = "\n".join(body)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title><desc id="desc">{desc}</desc>
<rect width="{w}" height="{h}" fill="{background}"/>
{content}
</svg>
'''


def pad(a, b, z=0):
    """Project points on the die. The z axis remains vertical on the page."""
    return a - b, (a + b) * .46 - z


def chip():
    # One chamfered carrier, ceramic layers and a blue die with a split X etched into it.
    contour = [(-58,-72), (58,-72), (72,-58), (72,58), (58,72), (-58,72), (-72,58), (-72,-58)]
    parts = []
    for z, scale, face, side in [(-14, 1.17, "#E4EDF6", "#A7B9CC"), (-2, 1.07, "#D3E4EA", TEAL),
                                  (15, 1, BLUE, "#163DAD")]:
        upper = [pad(a * scale, b * scale, z) for a, b in contour]
        lower = [(x, y + 6) for x, y in upper]
        parts.append(path(poly(lower), side, side, 1))
        for i in (2, 3, 4, 5, 6):
            j = (i + 1) % len(upper)
            parts.append(path(poly([upper[i], upper[j], lower[j], lower[i]]), side, side, .7))
        parts.append(path(poly(upper), BLUE if z == 15 else "#B6C7D6", face, 1))
    for t in range(-48, 56, 13):
        for a, b, end_a, end_b in [(t, 72, t, 80), (72, t, 80, t)]:
            parts.append(path(f"M{xy(pad(a,b,12))}L{xy(pad(end_a,end_b,11))}", "#7B9DF8", width=2))
    # The die is etched in screen-aligned coordinates, so the X keeps both
    # diagonals at this shallow viewing angle.
    parts.append('<g transform="translate(0 -14) matrix(1 -.04 -.22 .6 0 0)">')
    for d, color in [("M-43-40h21l20 24-12 14Z", "white"),
                     ("M22-40h23L-23 40h-24Z", "white"),
                     ("M12 5l31 35H21L0 18Z", "#9DDDD9")]:
        parts.append(path(d,fill=color))
    parts.append("</g>")
    parts.append(path(poly([pad(-56,-55,16), pad(-31,-55,16), pad(-37,-50,16), pad(-56,-50,16)]), fill="#89B5FF"))
    # The small contact groups on two corners indicate the conductive surface.
    for i in range(4):
        a = 18 + i * 7
        parts.append(path(f"M{xy(pad(a,53,16))}L{xy(pad(a+3,56,16))}", "#B4CCFF", width=1.6))
    return "".join(parts)


# Each interval uses the same 12-second clock. The bright head of one trace
# reaches its last vertex when the next trace starts at that same vertex.
CYCLE = 12
STAGE_TIMES = (0, 2.2, 4.4, 6.4, 9.5, CYCLE)
CIRCUIT = (
    ((-102,-15), (-85,-15), (-65,-27), (-47,-27), (-24,-42), (-4,-42)),
    ((-4,-42), (13,-42), (31,-51), (57,-37), (57,-27), (80,-14)),
    ((80,-14), (60,-2), (43,-2), (27,10), (16,10), (0,0), (0,-14)),
)
CORE_TO_RIM = ((0,-14), (16,-20), (40,-20), (66,-6), (93,-6),
               (120,-18), (128,-14), (134,0), (146,5))


def progress(seconds):
    return f"{seconds/CYCLE*100:.3f}%"


def loop_styles():
    css = []
    # Observe reaches the nucleus at 8.4 s. It holds the result until 9.5 s.
    intervals = ((0,2.2), (2.2,4.4), (4.4,6.4), (6.4,8.4), (9.5,10.4), (10.4,11.86))
    for i, (start, end) in enumerate(intervals):
        css.append(f"@keyframes travel{i}{{0%,{progress(start)}{{stroke-dashoffset:15;opacity:0}}"
                   f"{progress(start+.12)}{{opacity:1}}{progress(end)}{{stroke-dashoffset:-85;opacity:1}}"
                   f"{progress(min(end+.14,CYCLE))}{{stroke-dashoffset:-100;opacity:0}}100%{{opacity:0}}}}")
        css.append(f".leg{i}{{animation:travel{i} {CYCLE}s linear infinite}}")
    for i in range(len(STAGES)):
        start, end = STAGE_TIMES[i:i+2]
        css.append(f"@keyframes select{i}{{0%,{progress(start)}{{opacity:0}}"
                   f"{progress(start+.12)},{progress(end-.14)}{{opacity:1}}"
                   f"{progress(end)},100%{{opacity:0}}}}")
        css.append(f".selected{i}{{animation:select{i} {CYCLE}s linear infinite}}")
    # Each illuminated circuit stays charged through the pulse, allowing the
    # visitor to follow the internal sequence across short sections of copper.
    for i in range(3):
        arrived = intervals[i+1][1]
        css.append(f"@keyframes charge{i}{{0%,{progress(arrived-.18)}{{opacity:0}}"
                   f"{progress(arrived)},{progress(9.4)}{{opacity:.84}}"
                   f"{progress(9.95)},100%{{opacity:0}}}}")
        css.append(f".charge{i}{{animation:charge{i} {CYCLE}s ease-in-out infinite}}")
    css.extend((
        "@keyframes coreWave{0%,70%{opacity:0;transform:scale(.45)}72%{opacity:.9}"
        "79.1667%{opacity:0;transform:scale(2)}100%{opacity:0;transform:scale(2)}}",
        ".coreWave{animation:coreWave 12s ease-out infinite}",
        "@media(prefers-reduced-motion:reduce){*{animation:none!important}}",
    ))
    return "<style>\n" + "\n".join(css) + "\n</style>"


def track(d, i, ink, pulse, width=1.5):
    return (path(d, ink, width=width) +
            path(d, pulse, width=width+1.8, extra=f'class="leg{i}" pathLength="100" '
                 'stroke-dasharray="15 120" stroke-linecap="round" opacity="0"'))


def trace(points):
    return "M" + " ".join(xy(p) for p in points)


def loop(narrow):
    w, h = (420, 353) if narrow else (960, 322)
    if narrow:
        x, title_y, inlet_x, stage_x = 14, 52, 124, 40
        first, step, cx, cy, scale = 126, 43, 290, 220, .73
    else:
        x, title_y, inlet_x, stage_x = 34, 68, 263, 77
        first, step, cx, cy, scale = 113, 36, 707, 171, 1.26
    body = [loop_styles(), folio(x, title_y-5, 1),
            label(x+(48 if narrow else 63), title_y, "Intelligence Loop", 33 if narrow else 48,
                  weight=700, space=-1.7)]
    if narrow:
        body.append(label(x+48, title_y+26, "CONCEPT STUDY", 13, MUTED, mono=True, space=1))
    else:
        body.append(label(w-x, title_y-7, "CONCEPT STUDY", 15, MUTED, mono=True, align="end", space=1.4))

    def on_page(point):
        return cx + point[0]*scale, cy + point[1]*scale

    # A phase register on the left names the active operation. Only the input
    # and output are physical buses. Intermediate transactions live on the die.
    for i, stage in enumerate(STAGES):
        y = first+i*step
        body.extend((label(x, y+5, f"{i+1:02}", 13, MUTED, mono=True),
                     label(stage_x, y+7, stage, 19 if narrow else 23, weight=600, space=-.5),
                     path(f"M{stage_x} {y+12}h27", BLUE, width=2,
                          extra=f'class="selected{i}" opacity="0"')))
    inlet = on_page((-145,0))
    d = (f"M{inlet_x} {first}H{inlet_x+13} "
         f"C{inlet_x+45} {first} {inlet[0]-40:.2f} {inlet[1]:.2f} {xy(inlet)}"
         f"L{xy(on_page((-128,-15)))} {xy(on_page(CIRCUIT[0][0]))}")
    body.append(f'<g transform="translate({cx} {cy}) scale({scale})">{chip()}</g>')
    body.append(track(d, 0, "#829DB9", TEAL, 1.6))

    body.append(f'<g transform="translate({cx} {cy}) scale({scale})">')
    for i, points in enumerate(CIRCUIT):
        d = trace(points)
        body.append(track(d, i+1, "#ADCDF1", "white", 1.8))
        body.append(path(d, "#C8FFEE", width=2, extra=f'class="charge{i}" opacity="0"'))
        node_x, node_y = points[0]
        body.append(f'<circle cx="{node_x}" cy="{node_y}" r="3" fill="{BLUE}" stroke="#DFFFFA" stroke-width="1.4"/>')
    body.append(track(trace(CORE_TO_RIM), 4, "#91B7E0", "#B4FFF0", 1.7))
    body.append('<g transform="translate(0 -14) scale(1 .58)">'
                '<circle r="12" fill="#223CA0" stroke="#BCF7EE" stroke-width="2"/>'
                '<circle r="4" fill="white"/><circle class="coreWave" r="12" fill="none" '
                'stroke="white" stroke-width="2.2" opacity="0"/></g></g>')

    # The return starts exactly at the final vertex of the illuminated trace.
    # The folded bus delivers its sample to the very same Perceive socket.
    right, bottom = w-x, h-21
    back_x = inlet_x-6
    outer = (f"M{xy(on_page(CORE_TO_RIM[-1]))}H{right-10}l8 8V{bottom-9}"
             f"l-9 9H{back_x+8}l-8 -8V{first+6}l6 -6")
    body.append(track(outer, 5, "#829DB9", TEAL, 1.4))
    body.append(path(f"M{back_x-3} {first+24}l3-5 3 5", MUTED, width=1.3))
    body.append(f'<circle cx="{inlet_x}" cy="{first}" r="3.4" fill="white" stroke="{BLUE}" stroke-width="1.6"/>')
    return frame(w, h, "01 · Intelligence Loop",
                 "Concept study. Perceive brings the signal into the die. Reason, Act and Observe "
                 "light consecutive tracks. The nucleus pulses and sends the result back to Perceive.", body)


def polar(r, angle):
    a = radians(angle)
    return (r*cos(a), r*sin(a))


def aperture():
    """A rotating sweep in the circular plane is projected by the outer group."""
    # A graduated annular wedge leaves the central bearing and its stem clear.
    bits = []
    for i in range(12):
        a, b = -54 + 4.5*i, -49.5 + 4.5*i
        d = (f"M{xy(polar(19,a))}L{xy(polar(136,a))} "
             f"A136 136 0 0 1 {xy(polar(136,b))}L{xy(polar(19,b))} "
             f"A19 19 0 0 0 {xy(polar(19,a))}Z")
        bits.append(path(d, fill=BLUE, extra=f'opacity="{.045+.46*(i/11)**1.8:.3f}"'))
    bits.append(path("M19 0H136", BLUE, width=2.8))
    bits.append(path("M118 0H136", TEAL, width=3.2))
    return "".join(bits)


RADAR_STYLE = """<style>
@keyframes scan{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
@keyframes counter{from{transform:rotate(0deg)}to{transform:rotate(-360deg)}}
@keyframes receive{0%,100%{opacity:.95;transform:scale(.75)}5%{opacity:.36;transform:scale(1.6)}10%,98%{opacity:0;transform:scale(2)}99%{opacity:0;transform:scale(.74)}}
@keyframes deposit{0%,100%{opacity:0}1.2%{opacity:.95}6%{opacity:.5}10%,98%{opacity:0}}
@keyframes propagate{0%{stroke-dashoffset:6;opacity:.9}5%{stroke-dashoffset:-18;opacity:.9}6%{stroke-dashoffset:-24;opacity:0}98%,99.9%{stroke-dashoffset:6;opacity:0}}
.sweep{animation:scan 24s linear infinite}.satellite{animation:counter 48s linear infinite}
.receive{animation:receive 24s ease-out infinite}.deposit{animation:deposit 24s ease-out infinite}
.transfer{animation:propagate 24s linear infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""


def radar_field():
    parts = []
    # Three separated elevations share an orthographic plane. Each topic sits
    # at the same physical radius. Depth is purely a property of the drawing.
    for z, face, edge in [(53, "#DFE8F6", "#829AC2"), (36, "#EBF4F3", "#629DA4"), (0, "#F4F8FF", "#7C9DE9")]:
        parts.append(f'<g transform="translate(0 {z}) scale(1.31 .49)">')
        rim = BLUE if z == 0 else ("#65ACA8" if z == 36 else "#A5B7D1")
        parts.append(path("M140 0a140 140 0 0 1-280 0v6a140 140 0 0 0 280 0Z",fill=rim))
        parts.append(f'<circle r="140" fill="{face}" stroke="{edge}" stroke-width="1.8"/>')
        for r in (44, 88, 122):
            parts.append(f'<circle r="{r}" fill="none" stroke="{edge}" stroke-opacity=".56" stroke-width="1.2"/>')
        if z == 36:
            parts.append('<g class="satellite"><path d="M124.9 43.0A132 132 0 0 1 96.0 90.6" '
                         'fill="none" stroke="#4CAAA5" stroke-width="3"/>'
                         '<circle cx="96" cy="90.6" r="5" fill="white" stroke="#007F79" '
                         'stroke-width="2.8"/></g>')
        if z == 0:
            for angle in range(0,360,30):
                parts.append(path(f"M{xy(polar(12,angle))}L{xy(polar(138,angle))}", RULE))
            for angle in range(4,360,4):
                if angle % 60 < 40:
                    parts.append(path(f"M{xy(polar(128,angle))}L{xy(polar(134,angle))}", "#829ECF",width=1.2))
            parts.append(path("M-18 0a18 18 0 1 1 36 0a18 18 0 1 1-36 0Z",BLUE,"#DEE9FF",1.4))
            parts.append(f'<g class="sweep">{aperture()}</g>')
        parts.append("</g>")
    # Satellites exchange signals vertically between the upper plane and the
    # receiving deck. The sweep and echoes share a clock and angular origin.
    for index, degrees in enumerate((-149,-101,-51,0,51,105,156)):
        a,b = polar(122,degrees)
        x,y = a*1.31,b*.49
        phase = (degrees % 360)/360*24 - 24
        delay = f'style="animation-delay:{phase:.3f}s"'
        line = f"M{x:.2f} {y:.2f}v53"
        tint = TEAL if index in (1,4,6) else BLUE
        parts.append(path(line, tint, width=1, extra='stroke-opacity=".48" stroke-dasharray="2 3"'))
        parts.append(path(line, tint, width=2.6, extra=f'class="transfer" {delay} pathLength="24" stroke-dasharray="6 40" opacity="0"'))
        parts.append(f'<g transform="translate({x:.2f} {y:.2f})"><circle class="receive" {delay} r="5" fill="none" stroke="{tint}" stroke-width="1.8" opacity="0"/><circle r="4.2" fill="white" stroke="{tint}" stroke-width="1.8"/><circle r="1.4" fill="{tint}"/></g>')
        # The destination lights after the downward packet has crossed the gap.
        destination_delay = f'style="animation-delay:{phase + 1.2:.3f}s"'
        parts.append(f'<ellipse cx="{x:.2f}" cy="{y+53:.2f}" rx="5" ry="2.5" fill="none" '
                     f'stroke="{tint}" stroke-opacity=".45"/>')
        parts.append(f'<ellipse class="deposit" {destination_delay} cx="{x:.2f}" cy="{y+53:.2f}" '
                     f'rx="6" ry="3" fill="{tint}" opacity="0"/>')
        # Rotate each marker back against the mounting angle of the instrument.
        offset = -10 if y < 0 else 20
        parts.append(f'<g transform="translate({x:.2f} {y+offset:.2f}) rotate(13)">{label(0,0,chr(65+index),12,INK,700,mono=True,align="middle")}</g>')
    parts.extend([path("M0 -53V50", INK, width=1.3),
                  path("M-5 -53l5 -3 5 3-5 3Z", fill=TEAL),
                  '<ellipse rx="8" ry="4" fill="white" stroke="#2457E6" stroke-width="2"/>',
                  '<circle r="2.7" fill="#2457E6"/>'])
    return "".join(parts)


def radar(narrow):
    w,h = (420,445) if narrow else (960,332)
    x,y = (14,48) if narrow else (505,63)
    cx,cy,s = (209,160,.88) if narrow else (236,142,1.12)
    body = [RADAR_STYLE, folio(x,y-4,2),
            label(x+(48 if narrow else 57),y,"Technology Radar",33 if narrow else 39,weight=700,space=-1.5),
            f'<g transform="translate({cx} {cy}) scale({s}) rotate(-13)">{radar_field()}</g>']
    for i, title in enumerate(FIELDS):
        if narrow:
            lx,ly = 14 + (i%2)*202, 299 + (i//2)*39
            size = 16.4
        else:
            lx,ly = 512, 110 + i*30
            size = 19
        body.extend([label(lx,ly,chr(65+i),14,BLUE,650,mono=True),
                     path(f"M{lx+20} {ly-5}h10", "#95A9BF"),
                     label(lx+40,ly,title,size,weight=550,space=-.4)])
    return frame(w,h,"02 · Technology Radar",", ".join(FIELDS)+". Seven equally placed channels on a projected scanning field.",body,PAPER)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in (("loop", loop), ("radar", radar)):
        for suffix, narrow in (("",False),("-mobile",True)):
            (OUT / f"{name}{suffix}.svg").write_text(draw(narrow), encoding="utf-8")
