"""Draw two art-directed sizes of the Phase Loom with the Python standard library."""
from math import cos, cosh, hypot, pi, radians, sin, sqrt, tanh
from pathlib import Path

ART = Path(__file__).resolve().parents[1] / "assets" / "lab"
PAPER, INK, BLUE, TEAL = "#F6F8FA", "#182433", "#2457E6", "#009F91"
MUTED, RULE = "#53677A", "#D7E0EA"
SANS = "Inter,Helvetica Neue,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"
# In the local orbital plane, positive y is in front of the aperture.
ORBITS = [("outer", -15, 191, 35, TEAL, 24), ("inner", 41, 138, 40, BLUE, 12)]


def point(vertex):
    x, y, *_ = vertex
    return f"{x:.1f},{y:.1f}"


def path(vertices, close=False):
    return "M" + " ".join(point(p) for p in vertices) + ("Z" if close else "")


def tint(dark, light, weight):
    a, b = bytes.fromhex(dark), bytes.fromhex(light)
    return "#" + "".join(f"{round(x + (y-x)*weight):02x}" for x, y in zip(a, b))


def surface(t, across, loom, phase, below=0):
    """One material point on the strip, projected through a 520-unit camera."""
    # The spine bends while its local cross-section rolls. Shared vertices of
    # neighboring facets take identical positions in both breathing poses.
    side = 1 if loom == 0 else -1
    angle = radians((-38 if loom == 0 else 39) + 2.2*side*phase)
    radius = 145 if loom == 0 else 131
    opening = (33 if loom == 0 else 29) + phase * side * 4
    bend = 2.4
    spine_x = opening*cos(t) + (radius-opening)*tanh(bend*cos(t))/tanh(bend)
    speed = opening + bend*(radius-opening)/(tanh(bend)*cosh(bend*cos(t))**2)
    # The spine has a shallow bend; use its actual tangent for the lip.
    bend_y = (3 + 2*phase)*sin(2*t+.2)
    nx = opening*cos(t) + 2*(3 + 2*phase)*cos(2*t+.2)
    ny = speed*sin(t)
    length = hypot(nx, ny)
    twist = .53 + 1.03*sin(t + loom*1.55) + .63*sin(2*t-.8) + phase*.33*cos(2*t+.4)
    width = (17 if loom == 0 else 16) + 5.5*cos(t-.85)
    offset = across*width*cos(twist)
    x = spine_x + offset*nx/length
    y = opening*sin(t) + offset*ny/length + bend_y
    z = 28*sin(t) + (17+phase*6)*sin(2*t+loom*.7) + across*width*sin(twist)
    z += 6*side - below
    projection = 520/(520-z)
    return ((x*cos(angle) - y*sin(angle) + .1*z)*projection,
            (x*sin(angle) + y*cos(angle) - .4*z)*projection, z)


def ribbons():
    faces, variations = [], []
    for loom in range(2):
        count = 40
        gap = .69 if loom == 1 else 0
        edge = "#123276" if loom == 0 else "#12575a"
        dark, light = ("1335a4", "a4d0ff") if loom == 0 else ("116369", "b7f3df")
        for i in range(count):
            start, end = [gap/2 + (2*pi-gap)*j/count for j in (i,i+1)]
            def section(lo, hi, below=0):
                return [(start,lo,below),(end,lo,below),(end,hi,below),(start,hi,below)]
            def layer(points, fill, width=".5", stroke=None):
                # A single CSS morph interpolates every patch. The base d is
                # also the complete still drawing in viewers without CSS d.
                poses = [path([surface(t,a,loom,phase,b) for t,a,b in points], True)
                         for phase in (1, -.75)]
                name = f"f{len(variations)}"
                variations.append(f"#{name}{{--pose:path('{poses[1]}')}}")
                return (f'<path id="{name}" class="flex" d="{poses[0]}" fill="{fill}" '
                        f'stroke="{stroke or fill}" stroke-width="{width}" stroke-linejoin="round"/>')
            a, b, c, d = [surface(t,v,loom,1) for t,v,_ in section(-1,1)]
            u = [b[j]-a[j] for j in range(3)]
            v = [d[j]-a[j] for j in range(3)]
            nx, ny, nz = u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]
            shine = abs((-.36*nx-.52*ny+.77*nz)/sqrt(nx*nx+ny*ny+nz*nz))
            fill = tint(dark, light, .06+.9*shine**2.3)
            # Draw the thickness around each lip, then the satin face and an
            # inset highlight. Depth ordering splits each loop at its crossings.
            panels = []
            for k in (-1,1):
                panels.append(layer([(start,k,0),(end,k,0),(end,k,4),(start,k,4)],edge))
            panels.append(layer(section(-1,1),fill))
            panels.append(layer(section(.48,.73),tint(fill[1:],"ffffff",.49),".35"))
            if gap and i in (0,count-1):
                t = start if i==0 else end
                panels.append(layer([(t,-1,0),(t,1,0),(t,1,4),(t,-1,4)],INK))
            faces.append((sum(p[2] for p in (a,b,c,d))/4, "".join(panels)))
    faces.append((-4, topology()))
    faces.append((0, nucleus()))
    return "".join(f for _,f in sorted(faces)), "\n".join(variations)


def orbital_point(t, rx, ry):
    # The packet grows as it approaches the observer. Sampling true anomaly
    # preserves the change in apparent speed across the projected ellipse.
    depth = .15*sin(t)
    scale = 1/(1-depth)
    return rx*cos(t)*scale, ry*sin(t)*scale, scale


def orbital_styles():
    styles = []
    for name, _, rx, ry, _, duration in ORBITS:
        frames = []
        for step in range(49):
            x,y,k = orbital_point(2*pi*step/48, rx,ry)
            frames.append(f"{step/48*100:.3f}%{{transform:translate({x:.2f}px,{y:.2f}px) scale({k*k:.3f})}}")
        styles.append(f"@keyframes {name}Flow{{{''.join(frames)}}}")
        styles.append(f".{name}Packet{{animation:{name}Flow {duration}s linear infinite}}")
    return "\n".join(styles)


def orbit(foreground):
    parts = []
    for number, (name, tilt, rx, ry, color, duration) in enumerate(ORBITS):
        start = 0 if foreground else pi
        d = path([orbital_point(start+pi*j/36, rx, ry) for j in range(37)])
        weight = 1.2 if foreground else 1
        parts.append(f'<g transform="rotate({tilt})"><g class="{name}Plane">')
        parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{weight}" opacity="{.58 if foreground else .33}"/>')
        clip = "near" if foreground else "far"
        parts.append(f'<g clip-path="url(#{clip})">')
        # A pair of unequal packets serves as a material trace of the orbit.
        # Both halves share their phase and meet at the silhouette. The far
        # half is painted before the ribbons, and is occluded by them.
        for j, radius in enumerate((3.8,2.55,1.65)):
            delay = -duration*(.12+number*.19) + j*.25
            x,y,_ = orbital_point(-delay/duration*2*pi, rx,ry)
            parts.append(f'<g class="{name}Packet" style="animation-delay:{delay:.2f}s" transform="translate({x:.2f} {y:.2f})">'
                         f'<circle r="{radius}" fill="{color}" opacity="{1-j*.21:.2f}" stroke="white" stroke-width=".6"/></g>')
        parts.append('</g></g></g>')
    return "".join(parts)


def topology():
    vertices = [(-63,3),(-28,-34),(31,-37),(65,-8),(39,21),(-22,38)]
    route = path(vertices, True)
    parts = [f'<path d="{route}" fill="none" stroke="#759bb8" stroke-width=".9"/>',
             f'<path class="route" d="{route}" pathLength="100" fill="none" stroke="{TEAL}" stroke-width="2.2" stroke-dasharray="5 95" stroke-dashoffset="0"/>']
    for cls, a, b in [("bridgeA",1,4),("bridgeB",2,5)]:
        parts.append(f'<path class="{cls}" d="{path([vertices[a],(0,0),vertices[b]])}" stroke="{TEAL}" '
                     f'stroke-width="1.2" stroke-dasharray="2 3" fill="none" opacity="{.65 if cls=="bridgeA" else .1}"/>')
    for x,y in vertices:
        parts.append(f'<circle cx="{x}" cy="{y}" r="2.7" fill="white" stroke="{BLUE}" stroke-width="1.2"/>')
    return "".join(parts)


def nucleus():
    return f'''<g>
      <ellipse class="wave" rx="23" ry="14" fill="none" stroke="{TEAL}" stroke-width="1.2" opacity="0"/>
      <path d="M0-13 14-2 2 14-13 2Z" fill="{INK}"/>
      <path d="M0-13 14-2 1 0Z" fill="#a7e0e0"/><path d="m1 0 13-2-12 16Z" fill="{BLUE}"/>
      <path d="M-13 2 0-13 1 0Z" fill="white" stroke="{BLUE}" stroke-width=".7"/>
    </g>'''


STYLE = """
@keyframes flex{50%{d:var(--pose)}}.flex{animation:flex 24s ease-in-out infinite}
@keyframes outerTilt{0%,100%{transform:rotate(-4deg) scale(1,.82)}50%{transform:rotate(9deg) scale(.98,1.16)}}
@keyframes innerTilt{0%,100%{transform:rotate(2deg) scale(1,1)}50%{transform:rotate(-12deg) scale(.97,.82)}}
.outerPlane{animation:outerTilt 36s ease-in-out infinite}.innerPlane{animation:innerTilt 24s ease-in-out infinite}
@keyframes rewireA{0%,33%,100%{opacity:.75}51%,80%{opacity:.08}}
@keyframes rewireB{0%,33%,100%{opacity:.08}51%,80%{opacity:.75}}
.bridgeA{animation:rewireA 12s ease-in-out infinite}.bridgeB{animation:rewireB 12s ease-in-out infinite}
@keyframes route{to{stroke-dashoffset:-100}}.route{animation:route 12s linear infinite}
@keyframes emit{0%,43%,88%,100%{opacity:0;transform:scale(.85)}54%{opacity:.7;transform:scale(1)}81%{opacity:0;transform:scale(3.1)}}
.wave{animation:emit 12s ease-out infinite}
@keyframes drift{to{transform:translate(22px,22px)}}.field{animation:drift 36s linear infinite}
@keyframes slip{0%,88%,91%,100%{opacity:0;transform:translateX(0)}89.5%{opacity:.55;transform:translateX(2px)}}
.glitch{animation:slip 36s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
"""


def draw(mobile):
    w,h = (500,570) if mobile else (1120,449)
    margin = 25 if mobile else 39
    title_x, title_y, scale = (24,77,1.10) if mobile else (36,143,1.64)
    sub_y = 218 if mobile else 345
    cx,cy,unit = (253,363,.96) if mobile else (849,223,1.08)
    left,right = (26,474) if mobile else (627,1080)
    top,bottom = (239,500) if mobile else (68,366)
    # A custom-cut X and a permanently offset blue inlay keep the first
    # letter distinctive even when the narrow chromatic slice is at rest.
    mark = f'''<g fill="{INK}">
      <path d="M0 0h24l23 32-13 18Z M43 57l13-18 37 51H69Z M65 0h24L25 90H1Z"/>
      <path d="m44 56 12-17 3 4-12 17z" fill="{BLUE}"/>
      <text x="89" y="90" font-size="126" font-family="{SANS}" font-weight="750" letter-spacing="-8">iaore</text>
    </g>'''
    footer = h-26
    body, morphs = ribbons()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">Xiaore · Engineering Intelligence.</title>
<desc id="desc">XIAORE / AGENT LAB. Phase Loom: two flexing ribbons cross around a crystal nucleus. Particle packets weave between two orbital planes. AI Agents / LLM Systems.</desc>
<defs>
  <pattern id="field" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".83" fill="#9bb0c5"/></pattern>
  <clipPath id="viewport"><rect x="{left-7}" y="{top}" width="{right-left+14}" height="{bottom-top}"/></clipPath>
  <clipPath id="slice"><path d="M0 37h345v3H0z"/></clipPath>
  <clipPath id="near"><path d="M-210 0h420v70h-420Z"/></clipPath>
  <clipPath id="far"><path d="M-210-70h420V0h-420Z"/></clipPath>
  <g id="letters">{mark}</g>
</defs>
<style>{STYLE}
{orbital_styles()}
{morphs}</style>
<rect width="{w}" height="{h}" fill="{PAPER}"/>
<path d="M{margin} 58H{w-margin}M{margin} {h-63}H{w-margin}" stroke="{RULE}"/>
<g font-family="{MONO}" fill="{INK}" font-size="{14 if mobile else 15}">
  <path d="M{margin} 25h8l16 17h-8z M{margin+17} 25h8l-17 17h-8z" fill="{BLUE}"/>
  <text x="{margin+39}" y="40" font-family="{SANS}" font-weight="700" letter-spacing="1.6">XIAORE / AGENT LAB</text>
  <text x="{w-margin}" y="40" text-anchor="end" letter-spacing="1.3" fill="{MUTED}">ED. 03</text>
</g>
<g clip-path="url(#viewport)">
  <rect class="field" x="{left-22}" y="{top-22}" width="{right-left+44}" height="{bottom-top+44}" fill="url(#field)" opacity=".48"/>
  <path d="M{left} {cy}H{right} M{cx} {top}V{bottom}" stroke="{RULE}" stroke-dasharray="3 7" fill="none"/>
</g>
<g transform="translate({cx} {cy}) scale({unit})">{orbit(False)}{body}{orbit(True)}</g>
<g fill="none" stroke="#94a5b6"><path d="M{left} {top+12}v-12h12 M{right-12} {bottom}h12v-12"/></g>
<text x="{cx+7}" y="{top+11}" font-family="{MONO}" font-size="12" letter-spacing=".7" fill="{MUTED}">Y+</text>
<text x="{right-2}" y="{cy-5}" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing=".7" fill="{MUTED}">X+</text>
<text x="{left+2}" y="{bottom-3}" font-family="{MONO}" font-size="11" fill="{MUTED}">O (0,0)</text>
<g transform="translate({title_x} {title_y}) scale({scale})">
  <use href="#letters" xlink:href="#letters"/>
  <g clip-path="url(#slice)"><g class="glitch" opacity="0"><use href="#letters" xlink:href="#letters"/><path d="M25 37h21v3H25z" fill="#E88DAB"/></g></g>
</g>
<text x="{margin}" y="{sub_y}" fill="{INK}" font-family="{SANS}" font-size="{29 if mobile else 36}" letter-spacing="-1.3">Engineering Intelligence.</text>
<g font-family="{MONO}" font-size="{15 if mobile else 17}">
  <path d="M{margin} {footer-11}h5v12h-5z M{margin+8} {footer-11}h2v12h-2z" fill="{BLUE}"/>
  <text x="{margin+21}" y="{footer}" fill="{INK}">AI Agents / LLM Systems</text>
  <text x="{w-margin}" y="{footer}" text-anchor="end" fill="{MUTED}" font-size="{14 if mobile else 15}">PHASE LOOM</text>
</g>
</svg>
'''


if __name__ == "__main__":
    for suffix, narrow in [("",False),("-mobile",True)]:
        (ART / f"hero{suffix}.svg").write_text(draw(narrow), encoding="utf-8")
