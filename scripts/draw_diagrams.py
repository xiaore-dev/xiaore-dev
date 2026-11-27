"""Draw the three Agent Lab plates. The SVG attributes also define a still edition."""
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
    for t in range(4):
        # A shallow fan-out on the exposed silicon joins the silver contacts.
        points = [pad(-42+t*9,69,16), pad(-42+t*9,59-t*2,16),
                  pad(-48+t*9,53-t*2,16), pad(-48+t*9,46-t*2,16)]
        parts.append(path("M"+" ".join(xy(p) for p in points), "#B3C7FC", width=1.2))
        parts.append(f'<circle cx="{points[-1][0]:.2f}" cy="{points[-1][1]:.2f}" r="1.5" fill="white"/>')
    parts.append(path(poly([pad(-56,-55,16), pad(-31,-55,16), pad(-37,-50,16), pad(-56,-50,16)]), fill="#89B5FF"))
    # The small contact groups on two corners indicate the conductive surface.
    for i in range(4):
        a = 18 + i * 7
        parts.append(path(f"M{xy(pad(a,53,16))}L{xy(pad(a+3,56,16))}", "#B4CCFF", width=1.6))
    return "".join(parts)


LOOP_STYLE = """<style>
@keyframes address {0%,14%{opacity:1} 19%,98%{opacity:0} 100%{opacity:1}}
@keyframes send {0%{stroke-dashoffset:13;opacity:0} 2%{opacity:1} 8%{stroke-dashoffset:-97;opacity:1} 10%,11%{stroke-dashoffset:-103;opacity:0} 12%{opacity:.8} 17%{stroke-dashoffset:6;opacity:.8} 19%,100%{stroke-dashoffset:13;opacity:0}}
@keyframes feedback {0%,87%{stroke-dashoffset:12;opacity:0} 88%{stroke-dashoffset:10;opacity:1} 99%{stroke-dashoffset:-97;opacity:1} 100%{stroke-dashoffset:-103;opacity:0}}
.address{animation:address 12s ease-in-out infinite}.send{animation:send 12s linear infinite}
.feedback{animation:feedback 12s linear infinite}
@media(prefers-reduced-motion:reduce){.address,.send,.feedback{animation:none}}
</style>"""


def loop(narrow):
    w, h = (420, 353) if narrow else (960, 322)
    # Route five ordered address lines into five distinct die contacts.
    if narrow:
        x, title_y, start_x, stage_x = 14, 52, 122, 40
        first, step, cx, cy, scale = 126, 43, 290, 220, .73
    else:
        x, title_y, start_x, stage_x = 24, 68, 290, 67
        first, step, cx, cy, scale = 113, 36, 707, 171, 1.26
    body = [LOOP_STYLE,
            folio(x, title_y-5, 1),
            label(x+(48 if narrow else 63), title_y, "Intelligence Loop", 33 if narrow else 48, weight=700, space=-1.7)]
    if narrow:
        body.append(label(x+48, title_y+26, "CONCEPT STUDY", 13, MUTED, mono=True, space=1))
    else:
        body.append(label(w-x, title_y-7, "CONCEPT STUDY", 15, MUTED, mono=True, align="end", space=1.4))
    # Socket addresses wrap around the two left edges of the package. The
    # upper traces reach the far side; lower traces approach its near side.
    contacts = [(-84,-40), (-84,10), (-84,54), (-44,84), (16,84)]
    for i, (stage, contact) in enumerate(zip(STAGES, contacts)):
        y = first + i * step
        local_x, local_y = pad(*contact, -15)
        end_x, end_y = cx + (local_x-5) * scale, cy + local_y * scale
        elbow = start_x + (19 if narrow else 50) + i * (2 if narrow else 10)
        # A flexible middle span keeps all stages in order on both layouts.
        d = (f"M{start_x} {y}H{elbow} C{elbow+26} {y} {end_x-36:.2f} "
             f"{end_y:.2f} {end_x-9:.2f} {end_y:.2f}H{end_x:.2f}")
        delay = f'style="animation-delay:{-12+i*2.4:g}s"'
        body.extend([
            path(d, "#BACCDC", width=1.4),
            path(d, TEAL, width=2.8, extra=f'pathLength="100" stroke-dasharray="13 110" class="send" opacity="0" {delay}'),
            label(x, y+5, f"{i+1:02}", 13, MUTED, mono=True),
            label(stage_x, y+7, stage, 19 if narrow else 23, weight=600, space=-.5),
            path(f"M{stage_x} {y+12}h25",BLUE,width=2,extra=f'class="address" opacity="0" {delay}'),
            f'<circle cx="{start_x}" cy="{y}" r="3.2" fill="white" stroke="{BLUE}"/>',
            f'<circle class="address" {delay} cx="{start_x}" cy="{y}" r="4" fill="{BLUE}" opacity="0"/>',
            f'<circle cx="{end_x:.2f}" cy="{end_y:.2f}" r="2.5" fill="{TEAL}"/>',
            path(f"M{end_x:.2f} {end_y:.2f}h{9*scale:.2f}", TEAL),
        ])
    body.append(f'<g transform="translate({cx} {cy}) scale({scale})">{chip()}</g>')
    # After the fifth exchange the core drives a separate return bus to the
    # first address. Its arrival and the next Perceive highlight coincide.
    bottom = h-23
    right = w-x
    bus_x = 3 if narrow else 9
    return_bus = (f"M{cx+76*scale:.1f} {cy+52*scale:.1f}l19 9 H{right-12}l10 10 "
                  f"V{bottom-9}l-9 9H{bus_x+8}l-8 -8V{first+4}l4 -4h3")
    body.append(path(return_bus, "#8EA5BA", width=1.2))
    body.append(path(return_bus, TEAL,width=2.3,extra='class="feedback" pathLength="100" stroke-dasharray="12 110" opacity="0"'))
    body.append(path(f"M{bus_x+4} {first-3}l4 3-4 3", TEAL, width=1.5))
    return frame(w,h,"01 · Intelligence Loop",
                 "Concept study. Perceive, reason, act, observe and loop back to perception. Each addressed stage exchanges a pulse with the X-shaped control die.", body)


def polar(r, angle):
    a = radians(angle)
    return (r*cos(a), r*sin(a))


def aperture():
    """A rotating sweep in the circular plane is projected by the outer group."""
    bits = []
    for i in range(6):
        a, b = -48+i*8, -40+i*8
        d = f"M0 0L{xy(polar(136,a))} A136 136 0 0 1 {xy(polar(136,b))}Z"
        bits.append(path(d, fill=BLUE, extra=f'opacity="{.055+i*.067:.3f}"'))
    bits.append(path("M0 0H136", BLUE, width=2.6))
    return "".join(bits)


RADAR_STYLE = """<style>
@keyframes scan{to{transform:rotate(360deg)}}@keyframes receive{0%,100%{opacity:.2;transform:scale(.9)}7%{opacity:.9;transform:scale(1.7)}20%,95%{opacity:0;transform:scale(2)}}
@keyframes propagate{0%{stroke-dashoffset:6;opacity:0}3%{opacity:1}13%{stroke-dashoffset:-24;opacity:0}100%{opacity:0}}
.sweep{animation:scan 18s linear infinite}.receive{animation:receive 18s ease-out infinite}.transfer{animation:propagate 18s linear infinite}
@media(prefers-reduced-motion:reduce){.sweep,.receive,.transfer{animation:none}}
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
        phase = (degrees % 360)/360*18 - 18
        delay = f'style="animation-delay:{phase:.3f}s"'
        line = f"M{x:.2f} {y:.2f}v53"
        tint = TEAL if index in (1,4,6) else BLUE
        parts.append(path(line, tint, width=1, extra='stroke-opacity=".48" stroke-dasharray="2 3"'))
        parts.append(path(line, tint, width=2.6, extra=f'class="transfer" {delay} pathLength="24" stroke-dasharray="6 40" opacity="0"'))
        parts.append(f'<g transform="translate({x:.2f} {y:.2f})"><circle class="receive" {delay} r="4.5" fill="none" stroke="{tint}" opacity="0"/><circle r="4.2" fill="white" stroke="{tint}" stroke-width="1.8"/><circle r="1.4" fill="{tint}"/></g>')
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


def environment(narrow):
    w,h = (420,175) if narrow else (960,140)
    left, y = (14,45) if narrow else (24,53)
    body = [f'''<style>@keyframes route{{0%,100%{{stroke-dashoffset:5;opacity:0}} 16%{{opacity:.9}} 72%{{stroke-dashoffset:-59;opacity:.9}} 80%{{opacity:0}}}}.route{{animation:route 9s ease-in-out infinite}}
@media(prefers-reduced-motion:reduce){{.route{{animation:none}}}}</style>''',
            path(f"M{left} 4H{w-left}",RULE),folio(left,y-3,3)]
    if narrow:
        body.append(label(62,y,"Development Environment",27,weight=700,space=-1.3))
        x,start,step = 15,96,41
    else:
        body.extend([label(83,y,"Development",36,weight=700,space=-1.5),
                     label(83,y+37,"Environment",36,weight=700,space=-1.5)])
        x,start,step = 401,48,44
    # Both buses are typeset on one matrix; the terminals are deliberately
    # left open since these tools can be used independently.
    for i,(category,a,b) in enumerate([("LANGUAGES","Python","TypeScript"),("TOOLS","Pydantic","Playwright")]):
        gy = start + i*step
        slot, step_x = (117,136) if narrow else (148,169)
        body.append(label(x,gy,category,13,MUTED,600,mono=True,space=.4))
        body.append(label(x+slot,gy+2,a,21 if narrow else 27,weight=600,space=-.7))
        body.append(label(x+slot+step_x,gy+2,b,21 if narrow else 27,weight=600,space=-.7))
        line = f"M{x} {gy+10}h{w-x-left-3}"
        body.extend([path(line,RULE),path(line,TEAL,width=2,extra=f'class="route" style="animation-delay:{i*-4.5}s" pathLength="60" stroke-dasharray="5 65" opacity="0"'),
                     path(f"M{x} {gy+8}h4v4h-4Z",fill=BLUE)])
    return frame(w,h,"03 · Development Environment","Python and TypeScript. Pydantic for validation and Playwright for browser tests.",body)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in (("loop", loop), ("radar", radar), ("environment", environment)):
        for suffix, narrow in (("",False),("-mobile",True)):
            (OUT / f"{name}{suffix}.svg").write_text(draw(narrow), encoding="utf-8")
