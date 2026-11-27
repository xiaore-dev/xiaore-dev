"""Draw the two editions of Phase Loom, Xiaore's kinetic X sculpture."""
from math import cos, cosh, hypot, pi, radians, sin, sqrt, tanh
from pathlib import Path

ART = Path(__file__).resolve().parents[1] / "assets" / "lab"
PAPER, INK, BLUE, TEAL = "#F6F8FA", "#182433", "#2457E6", "#009F91"
MUTED, RULE = "#53677A", "#D7E0EA"
SANS = "Inter,Helvetica Neue,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"


def point(vertex):
    x, y, *_ = vertex
    return f"{x:.1f},{y:.1f}"


def path(vertices, close=False):
    return "M" + " ".join(point(p) for p in vertices) + ("Z" if close else "")


def tint(dark, light, weight):
    a = bytes.fromhex(dark)
    b = bytes.fromhex(light)
    return "#" + "".join(f"{round(x+(y-x)*weight):02x}" for x, y in zip(a, b))


def surface(t, across, loom, under=False):
    """Project a cut, twisting strip around an elongated elliptical spine."""
    angle = radians(-38 if loom == 0 else 39)
    radius, opening = (151, 28) if loom == 0 else (139, 26)
    twist = .38 + .90 * sin(t + loom * 1.7) + .40 * sin(2*t - .7)
    width = 15.5 + 5.5 * cos(t - .85)
    # The planar normal is perpendicular to the elliptical spine's tangent.
    bend = 2.2
    spine_x = opening*cos(t) + (radius-opening)*tanh(bend*cos(t))/tanh(bend)
    speed = opening + bend*(radius-opening)/(tanh(bend)*cosh(bend*cos(t))**2)
    nx, ny = opening*cos(t), speed*sin(t)
    length = hypot(nx, ny)
    normal = across * width * cos(twist)
    x = spine_x + normal*nx/length
    y = opening*sin(t) + normal*ny/length
    z = 24*sin(t) + 14*sin(2*t + loom*.8) + across*width*sin(twist)
    z += (-5 if under else 0) + (9 if loom == 0 else -9)
    return (x*cos(angle) - y*sin(angle) + .10*z,
            x*sin(angle) + y*cos(angle) - .44*z, z)


def ribbon_faces(loom):
    count = 48
    # Saw cuts at the outer tips expose the thickness of the optical bands.
    gap = .76 if loom == 1 else 0
    angles = [gap/2 + (2*pi-gap)*i/count for i in range(count+1)]
    faces = []
    for i, (start, end) in enumerate(zip(angles, angles[1:])):
        a, b = surface(start,-1,loom), surface(end,-1,loom)
        c, d = surface(end,1,loom), surface(start,1,loom)
        # Both faces use a cold, highly directional satin reflection.
        along = [b[j]-a[j] for j in range(3)]
        across = [d[j]-a[j] for j in range(3)]
        vx = along[1]*across[2]-along[2]*across[1]
        vy = along[2]*across[0]-along[0]*across[2]
        vz = along[0]*across[1]-along[1]*across[0]
        shine = abs((-.38*vx-.53*vy+.76*vz)/sqrt(vx*vx+vy*vy+vz*vz))
        if loom == 0:
            fill = tint("102777","8dbbff",.06+.91*shine**2.6)
            edge = "#142e83"
        else:
            fill = tint("0b5a66","b3eee2",.02+.96*shine**2.2)
            edge = "#165c63"
        fragment = []
        for side in (-1,1):
            rim = [surface(start,side,loom),surface(end,side,loom),
                   surface(end,side,loom,True),surface(start,side,loom,True)]
            fragment.append(f'<path d="{path(rim,True)}" fill="{edge}" stroke="{edge}" stroke-width=".5"/>')
        fragment.append(f'<path d="{path([a,b,c,d],True)}" fill="{fill}" stroke="{fill}" stroke-width=".65"/>')
        # Two longitudinal facets pick up the hard and soft reflections of a
        # pressed metal edge. They follow the surface all the way to the cut.
        for lo,hi,finish in [(-1,-.80,"192f5a"),(.49,.79,"ffffff")]:
            facet = [surface(start,lo,loom),surface(end,lo,loom),surface(end,hi,loom),surface(start,hi,loom)]
            lacquer = tint(fill[1:],finish,.49 if hi>0 else .38)
            fragment.append(f'<path d="{path(facet,True)}" fill="{lacquer}" stroke="{lacquer}" stroke-width=".4"/>')
        fragment.append(f'<path d="{path([a,b])} {path([d,c])}" fill="none" stroke="#edf7ff" stroke-opacity=".75" stroke-width=".8"/>')
        # Sparse triangular facets carry the visible topology across the skin.
        if i % 3 == 0:
            fragment.append(f'<path d="{path([a,d,c])}" stroke="{edge}" stroke-opacity=".38" stroke-width=".7" fill="none"/>')
        if gap and i in (0,count-1):
            t = start if i == 0 else end
            cap = [surface(t,-1,loom),surface(t,1,loom),surface(t,1,loom,True),surface(t,-1,loom,True)]
            fragment.append(f'<path d="{path(cap,True)}" fill="{INK}" stroke="#ffffff" stroke-width=".65"/>')
        z = sum(v[2] for v in (a,b,c,d))/4
        faces.append((z, f'<g class="ribbon{loom}">'+"".join(fragment)+'</g>'))
    return faces


def orbit(foreground):
    elements = []
    for angle, rx, ry, color, name in [(-17,207,46,TEAL,"tiltA"),(52,152,48,BLUE,"tiltB")]:
        d = (f"M{rx} 0A{rx} {ry} 0 0 1 {-rx} 0" if foreground
             else f"M{-rx} 0A{rx} {ry} 0 0 1 {rx} 0")
        dash = "7 141" if foreground and name == "tiltB" else "none"
        elements.append(f'<g transform="rotate({angle})"><g class="{name}">'
                        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{1.15 if foreground else .85}" '
                        f'stroke-opacity="{.65 if foreground else .36}" stroke-dasharray="{dash}"/>'
                        f'<path class="relay" d="{d}" fill="none" stroke="{color}" stroke-width="2.7" '
                        f'pathLength="100" stroke-dasharray="3 97" stroke-dashoffset="26"/>'
                        '</g></g>')
    return "".join(elements)


def particles():
    pieces = []
    for i in range(16):
        # Each set of grains belongs to a cut tip of the corresponding band.
        loom = i % 2
        flank = -1 if (i//2)%2 else 1
        axis = radians(-38 if loom == 0 else 39)
        reach = flank*(145 + (i*13)%42)
        cross = (i*23)%28 - 14
        x, y = reach*cos(axis)-cross*sin(axis), reach*sin(axis)+cross*cos(axis)
        color = BLUE if loom == 0 else TEAL
        w = 1.4 + (i%3)*.7
        dock_x = flank*(145 if loom == 0 else 133) - reach
        dock_y = (i%3-1)*1.8 - cross
        pieces.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({-38 if loom==0 else 39})">'
                      f'<g class="grain" style="animation-delay:-{i*.39:.2f}s;--dx:{dock_x:.1f}px;--dy:{dock_y:.1f}px">'
                      f'<rect x="{-w:.1f}" y="-1" width="{w*2:.1f}" height="{w:.1f}" fill="{color}" opacity=".8"/>'
                      '</g></g>')
    return "".join(pieces)


def topology():
    # Rosettes in the central window are the terminals of a switching bridge.
    # One diagonal hands the connection to the other every half-cycle.
    vertices = [(-70,6),(-31,-32),(28,-39),(69,-11),(40,21),(-22,38)]
    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]
    elements = []
    for a,b in edges:
        elements.append(f'<path d="{path([vertices[a],vertices[b]])}" stroke="#365e91" stroke-opacity=".55" stroke-width=".95" fill="none"/>')
    for cls, a,b in [("bridgeA",1,4),("bridgeB",2,5)]:
        elements.append(f'<path class="{cls}" d="{path([vertices[a],(0,0),vertices[b]])}" stroke="{TEAL}" '
                        f'stroke-width="1.25" fill="none" stroke-dasharray="2 2" opacity="{.8 if cls=="bridgeA" else .1}"/>')
    # The marker runs from vertex to vertex over a closed routed strand.
    route = path(vertices,True)
    elements.append(f'<path class="route" d="{route}" pathLength="100" stroke="{BLUE}" stroke-width="2.6" '
                    'stroke-dasharray="4 96" stroke-dashoffset="0" fill="none"/>')
    lengths = [hypot(vertices[b][0]-vertices[a][0],vertices[b][1]-vertices[a][1]) for a,b in edges]
    for i,(x,y) in enumerate(vertices):
        delay = 8*sum(lengths[:i])/sum(lengths)-8
        elements.append(f'<g transform="translate({x} {y})"><circle r="3.1" fill="#fff" stroke="{BLUE}" stroke-width="1.3"/>'
                        f'<circle class="hit" style="animation-delay:{delay:.2f}s" r="5.4" fill="none" stroke="{TEAL}" stroke-width="1.2" opacity="0"/></g>')
    return "".join(elements)


def core():
    faces = ribbon_faces(0) + ribbon_faces(1)
    # Drawing the facets from back to front lets the bands pass over and
    # under each other. The nucleus occupies the actual gap between layers.
    nucleus = f'''<g>
      <circle class="wave" r="17" fill="none" stroke="{TEAL}" stroke-width="1" opacity=".5"/>
      <path d="M0-12 12-2 2 12-11 2Z" fill="{INK}"/>
      <path d="M0-12 12-2 1 0Z" fill="#afdfec"/><path d="m1 0 11-2-10 14Z" fill="{BLUE}"/>
      <path d="M-11 2 0-12 1 0Z" fill="#ffffff" stroke="{BLUE}" stroke-width=".7"/>
    </g>'''
    faces.append((-3,topology()))
    faces.append((0,nucleus))
    return orbit(False) + "".join(f for _,f in sorted(faces)) + particles() + orbit(True)


STYLE = """
@keyframes turnA{0%,100%{transform:rotate(-3deg) scale(1,.97)}50%{transform:rotate(3deg) scale(.97,1.03)}}
@keyframes turnB{0%,100%{transform:rotate(2deg) scale(1,1.02)}50%{transform:rotate(-3deg) scale(1.03,.96)}}
.ribbon0{animation:turnA 15s ease-in-out infinite}.ribbon1{animation:turnB 19s ease-in-out infinite}
@keyframes precessA{0%,100%{transform:rotate(0) scale(1,.8)}50%{transform:rotate(12deg) scale(.96,1.17)}}
@keyframes precessB{0%,100%{transform:rotate(1deg) scale(.97,.76)}50%{transform:rotate(-16deg) scale(1,.99)}}
.tiltA{animation:precessA 29s ease-in-out infinite}.tiltB{animation:precessB 23s ease-in-out infinite}
@keyframes rewireA{0%,38%,100%{opacity:.85}52%,87%{opacity:.08}}
@keyframes rewireB{0%,38%,100%{opacity:.08}52%,87%{opacity:.85}}
.bridgeA{animation:rewireA 8s ease-in-out infinite}.bridgeB{animation:rewireB 8s ease-in-out infinite}
@keyframes route{to{stroke-dashoffset:-100}}.route{animation:route 8s linear infinite}
@keyframes hit{0%{opacity:.85;transform:scale(.72)}12%{opacity:0;transform:scale(1.8)}100%{opacity:0}}
.hit{animation:hit 8s ease-out infinite}
@keyframes transmit{to{stroke-dashoffset:-74}}.relay{animation:transmit 9s linear infinite}
@keyframes gather{0%,18%,100%{transform:translate(0,0);opacity:.8}52%,64%{transform:translate(var(--dx),var(--dy));opacity:.4}}
.grain{animation:gather 7s ease-in-out infinite}
@keyframes emit{0%,100%{opacity:0;transform:scale(.65)}18%{opacity:.58}70%{opacity:0;transform:scale(3.4)}}
.wave{animation:emit 7.5s ease-out infinite}
@keyframes drift{to{transform:translate(22px,22px)}}.field{animation:drift 26s linear infinite}
@keyframes scan{0%,100%{opacity:0;transform:translateY(-62px)}31%{opacity:.36}76%{opacity:0;transform:translateY(68px)}}
.scanner{animation:scan 18s ease-in-out infinite}
@keyframes slip{0%,86%,91%,100%{opacity:0;transform:translateX(0)}88%{opacity:.72;transform:translateX(3px)}}
.glitch{animation:slip 16s ease-in-out infinite}
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">Xiaore · Engineering Intelligence.</title>
<desc id="desc">XIAORE / AGENT LAB. Phase Loom: two folded ribbons cross around a crystal nucleus. AI Agents / LLM Systems.</desc>
<defs>
  <pattern id="field" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".83" fill="#9bb0c5"/></pattern>
  <clipPath id="viewport"><rect x="{left-7}" y="{top}" width="{right-left+14}" height="{bottom-top}"/></clipPath>
  <clipPath id="slice"><path d="M0 37h345v3H0z"/></clipPath>
  <g id="letters">{mark}</g>
</defs>
<style>{STYLE}</style>
<rect width="{w}" height="{h}" fill="{PAPER}"/>
<path d="M{margin} 58H{w-margin}M{margin} {h-63}H{w-margin}" stroke="{RULE}"/>
<g font-family="{MONO}" fill="{INK}" font-size="{14 if mobile else 15}">
  <path d="M{margin} 25h8l16 17h-8z M{margin+17} 25h8l-17 17h-8z" fill="{BLUE}"/>
  <text x="{margin+39}" y="40" font-family="{SANS}" font-weight="700" letter-spacing="1.6">XIAORE / AGENT LAB</text>
  <text x="{w-margin}" y="40" text-anchor="end" letter-spacing="1.3" fill="{MUTED}">ED. 02</text>
</g>
<g clip-path="url(#viewport)">
  <rect class="field" x="{left-22}" y="{top-22}" width="{right-left+44}" height="{bottom-top+44}" fill="url(#field)" opacity=".48"/>
  <path d="M{left} {cy}H{right} M{cx} {top}V{bottom}" stroke="{RULE}" stroke-dasharray="3 7" fill="none"/>
  <path class="scanner" d="M{left} {cy}H{right}" opacity="0" stroke="{TEAL}" stroke-width="1"/>
</g>
<g transform="translate({cx} {cy}) scale({unit})">{core()}</g>
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
