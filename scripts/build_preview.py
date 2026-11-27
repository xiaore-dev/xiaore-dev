"""Build motion-free SVG editions and the offline preview from README.md."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets" / "lab"
SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")


def still_frame(source):
    # The artwork defines its rest pose with presentation attributes. The
    # style blocks contain motion only; no external rendering engine is needed.
    root = ET.parse(source).getroot()
    for parent in root.iter():
        for child in list(parent):
            kind = child.tag.rsplit("}", 1)[-1]
            if kind in {"animate", "animateMotion", "animateTransform", "set", "style"} or child.get("data-motion-only") == "true":
                parent.remove(child)
        parent.attrib.pop("class", None)
        style = parent.attrib.get("style", "")
        if style.startswith("animation-delay:"):
            del parent.attrib["style"]
    serialized = ET.tostring(root, encoding="unicode")
    return "\n".join(line.rstrip() for line in serialized.splitlines()) + "\n"


# The profile body uses GitHub-supported HTML, so both views share one source.
HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Xiaore / Agent Lab — README preview</title>
<style>
:root{color-scheme:light;--bg:#fff;--ink:#1f2328;--muted:#59636e;--rule:#d1d9e0;--link:#0969da;--bar:#f6f8fa}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){color-scheme:dark;--bg:#0d1117;--ink:#f0f6fc;--muted:#9198a1;--rule:#3d444d;--link:#4493f8;--bar:#151b23}}
:root[data-theme=dark]{color-scheme:dark;--bg:#0d1117;--ink:#f0f6fc;--muted:#9198a1;--rule:#3d444d;--link:#4493f8;--bar:#151b23}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
header,article{max-width:900px;margin:auto}header{display:flex;align-items:center;gap:18px;padding:16px 4px;font-size:13px;color:var(--muted);flex-wrap:wrap}
header strong{color:var(--ink);margin-right:auto}select{font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--rule);border-radius:5px;padding:3px}
input{vertical-align:middle;accent-color:#2457e6}article{padding:28px 32px;border:1px solid var(--rule);border-radius:6px;margin-bottom:30px}
article h2{margin:24px 0 12px;font-size:1.5em;font-weight:600;line-height:1.25;border-bottom:1px solid var(--rule);padding-bottom:.3em}
article p{margin:0 0 16px}article a{color:var(--link);text-underline-offset:2px}article img{max-width:100%;height:auto;vertical-align:middle}
article picture{display:block;margin:0 0 16px}article>picture:last-child{margin:24px 0 0}
:focus-visible{outline:2px solid var(--link);outline-offset:3px}
@media(max-width:640px){article{padding:16px;border:0}header{padding:10px 16px;gap:8px 14px;background:var(--bar)}header strong{width:100%}}
</style></head><body>
<header aria-label="Local preview controls"><strong>README.md · Local preview</strong>
<label>Theme <select id="theme"><option value="auto">System</option><option value="light">Light</option><option value="dark">Dark</option></select></label>
<label><input type="checkbox" id="still"> Still frames</label></header>
<main><article aria-label="Xiaore GitHub profile">
"""

TAIL = """</article></main>
<script>
const theme = document.querySelector('#theme');
theme.addEventListener('change', () => { document.documentElement.dataset.theme = theme.value; });
const still = document.querySelector('#still');
const frames = document.querySelectorAll('picture source, picture img');
for (const frame of frames) {
  const attr = frame.tagName === 'IMG' ? 'src' : 'srcset';
  frame.dataset.original = frame.getAttribute(attr);
}
still.addEventListener('change', () => {
  for (const frame of frames) {
    const attr = frame.tagName === 'IMG' ? 'src' : 'srcset';
    const original = frame.dataset.original;
    const fixed = original.includes('/still/') ? original : original.replace('assets/lab/', 'assets/lab/still/');
    frame.setAttribute(attr, still.checked ? fixed : original);
  }
});
</script></body></html>
"""


if __name__ == "__main__":
    output = ART / "still"
    output.mkdir(exist_ok=True)
    for svg in sorted(ART.glob("*.svg")):
        (output / svg.name).write_text(still_frame(svg), encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    (ROOT / "preview.html").write_text(HEAD + readme + TAIL, encoding="utf-8")
