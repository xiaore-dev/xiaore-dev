"""Generate the wide and narrow orbital plates using only the standard library."""

from math import asin, atan2, cos, pi, radians, sin
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "lab"
RADIUS = 132
TILT = radians(23)
MERIDIANS = 20
ROTATION = 28  # seconds per revolution
BLUE = "#2457E6"
INK = "#182433"
MUTED = "#64748B"
LINE = "#D7E0EA"
TEAL = "#009F91"
MONO = "ui-monospace, Menlo, Consolas, monospace"


def pair(point):
    return " ".join(f"{value:.1f}" for value in point)


def sphere(latitude, longitude):
    """Project coordinates on the inclined polar axis into the drawing plane."""
    return (
        RADIUS * sin(latitude) * cos(longitude),
        RADIUS * (-cos(latitude) * cos(TILT) + sin(latitude) * sin(longitude) * sin(TILT)),
    )


def arc(point, start, end, segments):
    """Convert a projected circular arc to tangent-matched cubic Béziers."""
    step = (end - start) / segments
    commands = ["M" + pair(point(start))]
    for segment in range(segments):
        a = start + segment * step
        b = a + step
        p, q = point(a), point(b)
        # For a projected circle the derivative is a quarter-turn along its
        # ellipse, less its center. Central differences are exact at ±pi/2.
        p1, p0 = point(a + pi / 2), point(a - pi / 2)
        q1, q0 = point(b + pi / 2), point(b - pi / 2)
        handle = 2 / 3 * sin(step / 2) / (1 + cos(step / 2))
        first = [p[i] + handle * (p1[i] - p0[i]) for i in (0, 1)]
        last = [q[i] - handle * (q1[i] - q0[i]) for i in (0, 1)]
        commands.append("C" + " ".join(pair(x) for x in (first, last, q)))
    return "".join(commands)


def meridian(angle, front):
    # At this latitude the surface normal is parallel to the image plane.
    horizon = atan2(sin(TILT), -sin(angle) * cos(TILT))
    start, end = (0, horizon) if front else (horizon, pi)
    return arc(lambda t: sphere(t, angle), start, end, 2)


def parallel(degrees, front):
    theta = radians(degrees)
    crossing = -cos(theta) * sin(TILT) / (sin(theta) * cos(TILT))
    point = lambda t: sphere(theta, t)
    if abs(crossing) >= 1:
        return arc(point, 0, 2 * pi, 4) if front == (crossing < 0) else ""
    start = asin(crossing)
    a, b = (start, pi - start) if front else (pi - start, 2 * pi + start)
    return arc(point, a, b, 4)


def animated_styles():
    styles = [
        ".grid-drift{animation:drift 26s linear infinite}",
        "@keyframes drift{to{transform:translate(24px,24px)}}",
        ".scanner{animation:scan 21s ease-in-out infinite}",
        "@keyframes scan{0%,100%{transform:translateY(-52px);opacity:0}"
        "30%{opacity:.38}76%{transform:translateY(68px);opacity:0}}",
        ".glitch{animation:slip 13s ease-in-out infinite}",
        "@keyframes slip{0%,82%,86%,100%{opacity:0;transform:translateX(0)}"
        "84%{opacity:.64;transform:translateX(4px)}}",
        ".travel{animation:orbit 22s linear infinite}",
    ]
    positions = []
    for step in range(49):
        angle = 2 * pi * step / 48
        dx, dy = 196 * (cos(angle) - 1), 46 * sin(angle)
        positions.append(f"{100 * step / 48:.3f}%{{transform:translate({dx:.2f}px,{dy:.2f}px)}}")
    styles.append(f"@keyframes orbit{{{''.join(positions)}}}")
    # One pair of interpolated paths drives every rib. A phase shift selects
    # each longitude. Native 'd' attributes also draw the complete still plate.
    for front, name in [(False, "far"), (True, "near")]:
        styles.append(f".{name}{{animation:{name} {ROTATION}s linear infinite}}")
        frames = []
        for frame in range(41):
            path = meridian(2 * pi * frame / 40, front)
            frames.append(f"{frame * 2.5:g}%{{d:path('{path}')}}")
        styles.append(f"@keyframes {name}{{{''.join(frames)}}}")
    for index in range(MERIDIANS):
        styles.append(f".p{index}{{animation-delay:-{ROTATION * index / MERIDIANS:g}s}}")
    styles.append("@media(prefers-reduced-motion:reduce){*{animation:none!important}}")
    return "\n".join(styles)


def wires(front):
    name = "near" if front else "far"
    rails = []
    for index in range(MERIDIANS):
        path = meridian(2 * pi * index / MERIDIANS, front)
        rails.append(f'<path class="{name} p{index}" d="{path}"/>')
    # Tightly spaced latitude lines toward one pole give the plate its weight.
    for latitude in (12, 20, 28, 36, 44, 52, 60, 69, 79, 90, 102, 115, 128, 141, 154, 167):
        path = parallel(latitude, front)
        if path:
            rails.append(f'<path d="{path}"/>')
    return "\n".join(rails)


def orbit(front):
    # The same two particles draw behind the sphere for half their orbit,
    # then on its face. Translation preserves their circular silhouette.
    half = "bottom" if front else "top"
    return f"""<g transform="rotate(-21)" fill="none" stroke="{TEAL}">
  <path d="M196 0A196 46 0 0 {1 if front else 0} -196 0" stroke-width="{1.9 if front else 1.05}"/>
  <g clip-path="url(#{half})">
    <g class="travel">
      <circle cx="196" r="4.7" fill="{TEAL}" stroke="white" stroke-width="1.5"/>
    </g>
    <g transform="rotate(180)">
      <g class="travel"><circle cx="196" r="3.4" fill="white" stroke-width="1.8"/></g>
    </g>
  </g>
</g>"""


def globe():
    belt = parallel(90, True)
    return f"""<g>
  {orbit(False)}
  <g transform="rotate(18)">
    <circle r="{RADIUS}" fill="url(#ceramic)" stroke="{BLUE}" stroke-width="1.9"/>
    <g fill="none" stroke="{BLUE}" opacity=".22" stroke-width=".8">
      {wires(False)}
    </g>
    <g fill="none" stroke="{BLUE}" stroke-width="1.55">
      {wires(True)}
    </g>
    <path d="{belt}" fill="none" stroke="{BLUE}" stroke-width="5"/>
    <circle cx="0" cy="{-RADIUS * cos(TILT):.1f}" r="4" fill="{INK}"/>
  </g>
  {orbit(True)}
</g>"""


def draw(mobile):
    if mobile:
        width, height, margin = 520, 620, 24
        mast, head_rule, foot_rule = 27, 64, 555
        title_y, title_size, sub_y, sub_size = 171, 121, 213, 29
        cx, cy, scale = 261, 390, 1.0
        field_x, field_y, field_w, field_h = 19, 238, 482, 301
    else:
        width, height, margin = 1120, 448, 40
        mast, head_rule, foot_rule = 29, 70, 379
        title_y, title_size, sub_y, sub_size = 245, 163, 297, 36
        cx, cy, scale = 852, 224, 1.03
        field_x, field_y, field_w, field_h = 598, 80, 482, 288
    right = width - margin
    title_x = margin - 5
    footer_y = foot_rule + 39
    corners = (f"M{field_x} {field_y+14}v-14h15 M{field_x+field_w-15} {field_y}h15v14 "
               f"M{field_x} {field_y+field_h-14}v14h15 M{field_x+field_w-15} {field_y+field_h}h15v-14")
    wordmark = (f'<text x="{title_x}" y="{title_y}" font-family="Inter, Helvetica Neue, Arial, sans-serif" '
                f'font-weight="800" letter-spacing="{-title_size * .067:.1f}" font-size="{title_size}">Xiaore</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Xiaore · Engineering Intelligence.</title>
<desc id="desc">XIAORE / AGENT LAB. AI Agents / LLM Systems. A blue wireframe sphere revolves inside an inclined teal orbit.</desc>
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0v24" fill="none" stroke="{LINE}" stroke-width=".8"/>
    <circle r="1.4" fill="{LINE}"/>
  </pattern>
  <radialGradient id="ceramic" cx="34%" cy="27%" r="83%">
    <stop stop-color="white"/><stop offset=".67" stop-color="#F6F8FA"/>
    <stop offset="1" stop-color="#D7E0EA"/>
  </radialGradient>
  <clipPath id="plot"><rect x="{field_x}" y="{field_y}" width="{field_w}" height="{field_h}"/></clipPath>
  <clipPath id="top"><rect x="-210" y="-80" width="420" height="80"/></clipPath>
  <clipPath id="bottom"><rect x="-210" width="420" height="80"/></clipPath>
  <clipPath id="cut"><rect x="{title_x}" y="{title_y - title_size * .38:.1f}" width="{title_size * 3.5}" height="4.5"/></clipPath>
  <g id="wordmark">{wordmark}</g>
</defs>
<style>
{animated_styles()}
</style>
<rect width="{width}" height="{height}" fill="#F6F8FA"/>
<g transform="translate({margin} {mast-3})" fill="{BLUE}">
  <path d="M0 0h9l7 7-5 5z M22 0h9L12 22H3z M20 15l8 8h-9l-4-4z"/>
</g>
<g fill="{INK}" font-family="Inter, Helvetica Neue, Arial, sans-serif">
  <text x="{margin+43}" y="{mast+16}" font-size="{19 if mobile else 17}" font-weight="700" letter-spacing="1.3">XIAORE / AGENT LAB</text>
  <text x="{right}" y="{mast+16}" text-anchor="end" font-family="{MONO}" fill="{INK}" opacity=".78" font-size="{17 if mobile else 15}" letter-spacing="1.2">XR–01</text>
  <path d="M{margin} {head_rule}H{right}M{margin} {foot_rule}H{right}" fill="none" stroke="{LINE}" stroke-width="1.3"/>
  <g clip-path="url(#plot)">
    <rect x="{field_x}" y="{field_y}" width="{field_w}" height="{field_h}" fill="white"/>
    <rect class="grid-drift" x="{field_x-24}" y="{field_y-24}" width="{field_w+48}" height="{field_h+48}" fill="url(#grid)" opacity=".8"/>
    <path class="scanner" opacity="0" d="M{field_x} {cy}H{field_x+field_w}" stroke="{TEAL}" stroke-width=".8"/>
  </g>
  <path d="{corners}" fill="none" stroke="{MUTED}" opacity=".6" stroke-width="1"/>
  <g transform="translate({cx} {cy}) scale({scale})">
    {globe()}
  </g>
  <use href="#wordmark" xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#wordmark"/>
  <g clip-path="url(#cut)"><g class="glitch" opacity="0" fill="#E88DAB">{wordmark}</g></g>
  <text x="{margin}" y="{sub_y}" font-size="{sub_size}" letter-spacing="-1.2" font-weight="500">Engineering Intelligence.</text>
</g>
<g font-family="{MONO}" font-size="{20 if mobile else 17}" fill="{INK}">
  <path d="M{margin} {footer_y-12}h6v12h-6z M{margin+10} {footer_y-12}h3v12h-3z" fill="{BLUE}"/>
  <text x="{margin+25}" y="{footer_y}">AI Agents / LLM Systems</text>
  <text x="{right}" y="{footer_y}" text-anchor="end" fill="{INK}" opacity=".78" font-size="{16 if mobile else 15}" letter-spacing=".8">{'FIG. 01' if mobile else 'FIG. 01   /   ORBITAL STUDY'}</text>
</g>
</svg>
"""


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    for mobile, name in [(False, "hero.svg"), (True, "hero-mobile.svg")]:
        (ASSETS / name).write_text(draw(mobile), encoding="utf-8")
