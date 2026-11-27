"""Redraw the diagrams and development environment at their wide and narrow aspect ratios."""
from math import asinh, cos, radians, sin, sqrt
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "assets" / "lab"
BLUE, TEAL, INK = "#2457E6", "#009F91", "#182433"
RULE, MUTED, PAPER = "#D7E0EA", "#64748B", "#F6F8FA"
SANS = "Inter,Helvetica Neue,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"


def frame(w, h, title, description, drawing):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{title}</title>
<desc id="desc">{description}</desc>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" fill="#FFFFFF" stroke="{RULE}"/>
{drawing}
</svg>
'''


# Paths are hand-drawn around the local origin. Each pictogram is a different
# physical operation: collect, assemble, transmit, inspect and recirculate.
SYMBOLS = (
    '<path d="M-23 0Q0 -29 23 0Q0 29 -23 0Z"/><circle r="8.5"/><circle r="3" fill="currentColor" stroke="none"/>',
    '<path d="M0 -21 19 -11 19 10 0 21 -19 10 -19 -11Z M-19 -11 0 0 19 -11 M0 0V21 M-9 -16 10 -5V5L0 11 -10 5V-5L9 -16"/>',
    '<path d="M-20 -14H-5L10 0 -5 14H-20L-5 0Z" fill="currentColor" stroke="none"/><path d="M0 -14H9L24 0 9 14H0L14 0Z"/>',
    '<circle r="18.5"/><circle r="10.3" stroke-dasharray="31 6 16 12"/><path d="M0 -24V-16 M0 16V24 M-24 0H-16 M16 0H24"/><circle r="3" fill="currentColor" stroke="none"/>',
    '<path d="M-17 -2a17 17 0 0 1 28-11l6 6m0-10v10H7 M17 2a17 17 0 0 1-28 11l-6-6m0 10V7h10"/>',
)
STAGES = ("Perceive", "Reason", "Act", "Observe", "Loop")


def point(x, y):
    return f"{x:.2f},{y:.2f}"


def arrow(x, y, rotate=0):
    return (f'<path transform="translate({x} {y}) rotate({rotate})" '
            f'd="M-4 -3.5 0 0 -4 3.5" stroke="{MUTED}" stroke-width="1.4" fill="none"/>')


def loop(narrow):
    if narrow:
        w, h = 420, 277
        nodes = [(73, 69), (210, 69), (347, 69), (281, 186), (137, 186)]
        right, left, turn, radius = 405, 15, 186, 15
        arrows = [(145, 69, 0), (282, 69, 0), (405, 131, 90), (210, 186, 180), (15, 124, 270)]
        lengths = [0, 137, 274]
    else:
        w, h = 960, 205
        nodes = [(92 + 194*i, 81) for i in range(5)]
        right, left, turn, radius = 925, 35, 173, 15
        arrows = [(194 + 194*i, 81, 0) for i in range(4)] + [(480, 173, 180)]
        lengths = [194*i for i in range(5)]

    # Use the length of the drawn Bezier corners when scheduling arrivals.
    # Relative coordinates put the carrier beneath the first node even when
    # a viewer does not animate SMIL.
    start_x, start_y = nodes[0]
    height = turn - start_y
    path = (f"M0 0h{right-radius-start_x}q{radius} 0 {radius} {radius}"
            f"v{height-2*radius}q0 {radius} -{radius} {radius}"
            f"h-{right-left-2*radius}q-{radius} 0 -{radius} -{radius}"
            f"v-{height-2*radius}q0 -{radius} {radius} -{radius}h{start_x-left-radius}")
    corner_length = radius * (1 + asinh(1) / sqrt(2))
    cut = 2*radius - corner_length
    perimeter = 2 * (right - left + height) - 4*cut
    if narrow:
        for x, _ in nodes[3:]:
            lengths.append(right - nodes[0][0] + height + right - x - 2*cut)
    stops = ";".join(f"{d/perimeter:.5f};{d/perimeter:.5f}" for d in lengths) + ";1"
    times = "0;.07;.16;.23;.32;.39;.48;.55;.64;.71;1"
    body = [f"""<style>
@keyframes select {{0%,7% {{opacity:1}} 12%,95% {{opacity:0}} 100% {{opacity:1}}}}
.halo {{animation:select 10s linear infinite both}}
@media (prefers-reduced-motion:reduce) {{.halo,.carrier {{display:none}}}}
</style>
<path transform="translate({start_x} {start_y})" d="{path}" stroke="{RULE}" stroke-width="1.6" fill="none"/>"""]
    body.extend(arrow(*mark) for mark in arrows)
    body.append(f'''<g class="carrier" transform="translate({start_x} {start_y})" fill="{TEAL}">
<circle r="4"><animateMotion path="{path}" dur="10s" keyTimes="{times}" keyPoints="{stops}" calcMode="linear" repeatCount="indefinite"/></circle>
</g>''')
    for index, ((x, y), stage, symbol) in enumerate(zip(nodes, STAGES, SYMBOLS)):
        color = TEAL if index in (0, 3) else BLUE
        # An explicit rest state survives renderers without CSS animations.
        body.append(f'''<g transform="translate({x} {y})">
<circle r="33" fill="{PAPER}" stroke="{RULE}"/>
<circle class="halo" style="animation-delay:{-10 + index*1.6:.1f}s" r="33" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-width="2" opacity="0"/>
<g fill="none" color="{color}" stroke="{color}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round">{symbol}</g>
<text y="-42" text-anchor="middle" fill="{MUTED}" font-family="{MONO}" font-size="12" letter-spacing="1.2">{index+1:02}</text>
<text y="59" text-anchor="middle" fill="{INK}" font-family="{SANS}" font-size="21" font-weight="600">{stage}</text>
</g>''')
    return frame(w, h, "Agent feedback loop",
                 "Perceive, reason, act, observe, and loop back to the next perception. Concept diagram.",
                 "\n".join(body))


# Marker directions are graphic coordinates. Every topic has the same radius.
FIELDS = (
    ("Agent Architecture", -145), ("LLM Inference", -104),
    ("Context Engineering", -47), ("Tool Calling", -2),
    ("MCP", 42), ("RAG", 86), ("Software Engineering", 142),
)


def polar(r, degrees):
    angle = radians(degrees)
    return r*cos(angle), r*sin(angle)


def wedge(radius, start, end):
    return f"M0 0L{point(*polar(radius,start))}A{radius} {radius} 0 0 1 {point(*polar(radius,end))}Z"


def radar(narrow):
    w, h, cx, cy, radius = (420, 430, 210, 126, 99) if narrow else (960, 330, 460, 165, 126)
    body = [f'''<style>
@keyframes sweep {{to {{transform:rotate(360deg)}}}}
@keyframes echo {{0% {{opacity:0;transform:scale(.68)}} 4% {{opacity:.55}} 16%,100% {{opacity:0;transform:scale(1.7)}}}}
@keyframes core {{0%,70%,100% {{opacity:.18}} 35% {{opacity:.65}}}}
.sweep {{animation:sweep 18s linear infinite}}
.echo {{animation:echo 18s ease-out infinite}}
.core {{animation:core 8s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce) {{.sweep,.echo,.core {{animation:none}}}}
</style>
<g transform="translate({cx} {cy})">
<circle r="{radius}" fill="{PAPER}"/>''']
    for frac in (.27,.53,.78,1):
        body.append(f'<circle r="{radius*frac:.2f}" fill="none" stroke="{RULE}" stroke-width="1"/>')
    for angle in range(0, 360, 45):
        body.append(f'<path d="M0 0L{point(*polar(radius,angle))}" stroke="{RULE}" stroke-width=".8"/>')
    for angle in range(0, 360, 5):
        major = angle % 30 == 0
        body.append(f'<path d="M{point(*polar(radius+4,angle))}L{point(*polar(radius+(10 if major else 6),angle))}" stroke="{MUTED if major else RULE}"/>')
    # Offset calibration arcs bracket each topic on the rim.
    for i, (_, direction) in enumerate(FIELDS):
        r = radius + 3
        arc = f"M{point(*polar(r,direction-8))}A{r} {r} 0 0 1 {point(*polar(r,direction+8))}"
        body.append(f'<path d="{arc}" fill="none" stroke="{BLUE if i % 2 == 0 else TEAL}" stroke-width="2.2"/>')
    body.append('<g class="sweep">')
    for n in range(6):
        body.append(f'<path d="{wedge(radius,-121+n*5,-116+n*5)}" fill="{BLUE}" opacity="{.012*(n+1):.3f}"/>')
    body.append(f'<path d="M0 0V-{radius}" stroke="{BLUE}" stroke-width="1.2" opacity=".65"/></g>')
    body.append(f'<circle class="core" r="13" fill="none" stroke="{TEAL}" opacity=".45"/><circle r="6" fill="{INK}"/><circle r="2" fill="white"/></g>')
    desktop_labels = [(255,126),(255,54),(691,49),(691,117),(691,206),(691,273),(255,244)]
    for i, (label, angle) in enumerate(FIELDS):
        dx, dy = polar(.78*radius,angle)
        x, y = cx+dx, cy+dy
        color = BLUE if i % 2 == 0 else TEAL
        marker = chr(65+i)
        if narrow:
            lx, ly = 26 + (i % 2)*200, 268 + (i//2)*41
            body.append(f'<path d="M{lx} {ly-14}h168" stroke="{RULE}"/>')
            body.append(f'<text x="{lx}" y="{ly+6}" font-family="{MONO}" font-size="13" fill="{BLUE}">{marker}</text>'
                        f'<text x="{lx+18}" y="{ly+6}" font-family="{SANS}" font-size="16" font-weight="600" fill="{INK}">{label}</text>')
            offset_x, offset_y = polar(17,angle)
            body.append(f'<text x="{x+offset_x:.2f}" y="{y+offset_y+4:.2f}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="bold" fill="{INK}">{marker}</text>')
        else:
            lx, ly = desktop_labels[i]
            side = 1 if dx > 0 else -1
            end = lx - side*11
            elbow = x + side*abs(ly-y)
            # Direct labels keep the compass readable without consulting a key.
            body.append(f'<path d="M{point(x,y)}L{point(elbow,ly)}H{end}" fill="none" stroke="{MUTED}" stroke-opacity=".63"/>')
            body.append(f'<text x="{lx}" y="{ly+6}" text-anchor="{"start" if side==1 else "end"}" font-family="{SANS}" font-size="21" font-weight="600" fill="{INK}">{label}</text>')
        phase = ((angle + 90) % 360)/360 * 18
        body.append(f'''<g transform="translate({x:.2f} {y:.2f})">
<circle class="echo" style="animation-delay:{phase-18:.3f}s" r="8" stroke="{color}" fill="none" opacity="0"/>
<circle r="5.3" fill="white" stroke="{color}" stroke-width="2"/><circle r="2.2" fill="{color}"/></g>''')
    return frame(w,h,"Technology radar",", ".join(label for label, _ in FIELDS) + ". A map of exploration topics.",
                 "\n".join(body))


# Instruments share a rounded drawing stroke and a single spot color.
TOOLS = (
    ("Python", "Language",
     '<path d="M-14 -13h13l6 6h10 M-15 -2h8l6 6h14 M-15 10h5l5 5h9"/><circle cx="15" cy="-7" r="3.1" fill="#2457E6" stroke="none"/>'),
    ("TypeScript", "Language",
     '<path d="M-12 -11l-8 11 8 11 M12 -11l8 11 -8 11 M-5 -7H6 M.5 -7V8"/><path d="M-3 9h7" stroke="#2457E6"/>'),
    ("Pydantic", "Validation",
     '<path d="M-5 -16h-8v10q0 5 -6 6 6 1 6 6v10h8 M5 -16h8v10q0 5 6 6 -6 1 -6 6v10H5"/><path d="M-6 0l4 4 8-9" stroke="#2457E6"/>'),
    ("Playwright", "Browser tests",
     '<path d="M-11 -14v-3h28v22h-3 M-17 -10h29v24h-29Z M-16 -4h27"/><path d="m-5 0 7 4-7 5Z" fill="#2457E6" stroke="none"/>'),
)


def environment(narrow):
    w, h = (420, 224) if narrow else (960, 136)
    cols = 2 if narrow else 4
    cell_w, cell_h = w / cols, h / (2 if narrow else 1)
    body = [f'''<style>
@keyframes trace {{0%,48%,100% {{opacity:0;stroke-dashoffset:48}} 8% {{opacity:.8}} 38% {{opacity:.65;stroke-dashoffset:0}} 46% {{opacity:0;stroke-dashoffset:-16}}}}
.trace {{animation:trace 12s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce) {{.trace {{animation:none}}}}
</style>''']
    if narrow:
        body.append(f'<path d="M0 {cell_h:g}h{w}" stroke="{RULE}"/>')
    for i in range(1, cols):
        body.append(f'<path d="M{cell_w*i:g} 0v{h}" stroke="{RULE}"/>')
    for index, (name, role, symbol) in enumerate(TOOLS):
        x, y = cell_w*(index % cols), cell_h*(index // cols)
        icon_y, title_y, role_y = (30, 71, 93) if narrow else (37, 87, 111)
        body.append(f'''<g transform="translate({x:g} {y:g})">
<g transform="translate(39 {icon_y})" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{symbol}</g>
<path d="M77 {icon_y}h{cell_w-100:g}" stroke="{RULE}" stroke-width="1"/>
<path class="trace" style="animation-delay:{-12+index*3}s" d="M77 {icon_y}h{cell_w-100:g}" stroke="{TEAL}" stroke-width="2" stroke-dasharray="16 32" opacity="0"/>
<text x="21" y="{title_y}" font-family="{SANS}" font-size="24" font-weight="600" fill="{INK}">{name}</text>
<text x="22" y="{role_y}" font-family="{MONO}" font-size="14" fill="{MUTED}">{role}</text></g>''')
    return frame(w, h, "Development environment", "Python and TypeScript languages, Pydantic for validation, and Playwright for browser tests.", "\n".join(body))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in (("loop",loop),("radar",radar),("environment",environment)):
        for suffix, narrow in (("", False), ("-mobile", True)):
            (OUT / f"{name}{suffix}.svg").write_text(draw(narrow), encoding="utf-8")
