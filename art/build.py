# Builds the README artwork. Every word is converted to outlined paths so it renders the same on GitHub.
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
G = "/usr/share/fonts/truetype/sand-box/google/"
FONTS = {"serif": G+"Instrument Serif/InstrumentSerif-Regular.ttf", "italic": G+"Instrument Serif/InstrumentSerif-Italic.ttf",
         "mono": G+"IBM Plex Mono/IBMPlexMono-Regular.ttf", "hand": G+"Caveat/Caveat-VariableFont_wght.ttf"}
_c = {}
def font(k):
    if k not in _c:
        f = TTFont(FONTS[k]); _c[k] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _c[k]
def width(s, k, size, track=0):
    f, gs, cm, upm = font(k)
    return sum(gs[cm.get(ord(ch), cm[32])].width for ch in s) * size / upm + track * len(s)
def T(s, x, y, size, k="serif", fill="var(--ink)", track=0, anchor="start", extra=""):
    f, gs, cm, upm = font(k); sc = size / upm
    if anchor == "end": x -= width(s, k, size, track)
    if anchor == "middle": x -= width(s, k, size, track) / 2
    pen = SVGPathPen(gs, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip(".")); cx = x
    for ch in s:
        g = gs[cm.get(ord(ch), cm[32])]
        g.draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        cx += g.width * sc + track
    return f'<path {extra} fill="{fill}" d="{pen.getCommands()}"/>'

# Palette: warm paper and ink, one burnt amber accent. Dark mode is the same palette inverted.
THEMES = {"light": dict(ink="#141414", muted="#6B655B", faint="#D9D3C7", paper="#F4F1EA"),
          "dark":  dict(ink="#EDE8DC", muted="#A39E93", faint="#34312C", paper="#121212")}
ACC = "#C8772E"
PAD = 28
def wrap(w, h, body, th, css=""):
    t = THEMES[th]
    w, h = w + 2*PAD, h + 2*PAD
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>svg{{--ink:{t["ink"]};--muted:{t["muted"]};--faint:{t["faint"]};--paper:{t["paper"]};--acc:{ACC}}}{css}</style>'
            f'<rect width="{w}" height="{h}" fill="var(--paper)"/><g transform="translate({PAD} {PAD})">{body}</g></svg>')

# 1. Masthead
def masthead(th):
    b = []
    b.append(T("NO. 01", 0, 22, 12, "mono", "var(--muted)", 2))
    b.append(T("THE PROFILE OF", 860, 22, 12, "mono", "var(--muted)", 2, "end"))
    b.append('<rect y="34" width="860" height="1.5" fill="var(--ink)"/>')
    b.append(T("Alok Yadav", -4, 152, 124, "serif"))
    b.append(T("biotech student,", 0, 198, 30, "italic", "var(--muted)"))
    b.append(T("ships Android apps, fixes Flutter and Dart docs.", width("biotech student, ", "italic", 30), 198, 30, "italic"))
    b.append('<rect y="226" width="860" height="0.75" fill="var(--faint)"/>')
    b.append(T("INDIA", 0, 250, 11, "mono", "var(--muted)", 2))
    b.append(T("KOTLIN  ·  COMPOSE  ·  FLUTTER  ·  DART", 430, 250, 11, "mono", "var(--muted)", 2, "middle"))
    # rubber stamp date
    b.append(f'<g transform="translate(770 112) rotate(-7)" opacity=".9"><rect x="-62" y="-20" width="124" height="38" rx="3" fill="none" stroke="var(--acc)" stroke-width="1.5"/>'
             + T("30.10.2026", 0, 6, 15, "mono", "var(--acc)", 1.5, "middle") + '</g>')
    return wrap(860, 262, "".join(b), th)

# 2. The Vedrino piece: a Reels feed scrolls, stops, and turns into a focus timer.
PHX, PHY, PW, PH = 560, 24, 170, 330
def vedrino(th):
    css = """
.feed{animation:feed 9s cubic-bezier(.33,0,.15,1) infinite}
@keyframes feed{0%{transform:translateY(0);opacity:1}30%{transform:translateY(-330px);opacity:1}38%{transform:translateY(-345px);opacity:1}46%,100%{transform:translateY(-345px);opacity:0}}
.ring{stroke-dasharray:345;stroke-dashoffset:345;animation:ring 9s cubic-bezier(.65,0,.35,1) infinite}
@keyframes ring{0%,44%{stroke-dashoffset:345}60%,90%{stroke-dashoffset:24;opacity:1}100%{stroke-dashoffset:24;opacity:0}}
.in{opacity:0;animation:in 9s ease infinite}.in2{animation-name:in2}
@keyframes in{0%,50%{opacity:0;transform:translateY(6px)}58%,92%{opacity:1;transform:none}100%{opacity:0}}
@keyframes in2{0%,60%{opacity:0;transform:translateY(6px)}68%,92%{opacity:1;transform:none}100%{opacity:0}}
.ink{stroke-dasharray:300;stroke-dashoffset:300;animation:ink 9s ease-out infinite}
@keyframes ink{0%,4%{stroke-dashoffset:300}22%,100%{stroke-dashoffset:0}}
@media (prefers-reduced-motion:reduce){.feed{animation:none;opacity:0}.ring{animation:none;stroke-dashoffset:24}.in{animation:none;opacity:1}.ink{animation:none;stroke-dashoffset:0}}"""
    b = []
    b.append(T("NOW BUILDING", 0, 22, 12, "mono", "var(--acc)", 2))
    b.append('<rect y="34" width="380" height="0.75" fill="var(--faint)"/>')
    b.append(T("Vedrino", -3, 128, 96, "serif"))
    b.append(T("Plan less. Flow more.", 0, 174, 32, "italic", "var(--muted)"))
    for i, line in enumerate(["A focus app for Android. Plan your day,", "study without the scroll, and block", "just the Shorts and Reels, not the", "whole app."]):
        b.append(T(line, 0, 222 + i * 20, 13, "mono", "var(--ink)"))
    b.append('<rect y="318" width="380" height="0.75" fill="var(--faint)"/>')
    b.append(T("BETA IN DECEMBER", 0, 342, 11, "mono", "var(--muted)", 2))
    b.append(T("VEDRINO.WEBSITE", 380, 342, 11, "mono", "var(--ink)", 2, "end"))
    # hand note + arrow
    b.append(f'<g transform="rotate(-4 470 70)">{T("the thing I'm", 412, 62, 24, "hand", "var(--acc)")}{T("making right now", 412, 86, 24, "hand", "var(--acc)")}</g>')
    b.append('<path class="ink" d="M470 100 C 478 140, 500 160, 548 168" fill="none" stroke="var(--acc)" stroke-width="1.6" stroke-linecap="round"/>'
             '<path d="M538 160 L549 168 L537 175" fill="none" stroke="var(--acc)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    # phone
    x, y = PHX, PHY
    b.append(f'<rect x="{x}" y="{y}" width="{PW}" height="{PH}" rx="26" fill="var(--paper)" stroke="var(--ink)" stroke-width="1.5"/>')
    b.append(f'<rect x="{x+PW/2-18}" y="{y+10}" width="36" height="8" rx="4" fill="none" stroke="var(--ink)" stroke-width="1"/>')
    b.append(f'<clipPath id="s"><rect x="{x+10}" y="{y+26}" width="{PW-20}" height="{PH-46}" rx="6"/></clipPath><g clip-path="url(#s)"><g class="feed">')
    for i in range(6):
        cy = y + 30 + i * 115
        b.append(f'<rect x="{x+16}" y="{cy}" width="{PW-32}" height="105" rx="6" fill="none" stroke="var(--faint)" stroke-width="1"/>'
                 f'<path d="M{x+PW/2-9} {cy+38} l20 14 l-20 14z" fill="none" stroke="var(--muted)" stroke-width="1.2" stroke-linejoin="round"/>'
                 f'<rect x="{x+26}" y="{cy+88}" width="{40+(i*17)%50}" height="2" fill="var(--faint)"/>')
    b.append('</g></g>')
    cx, cy = x + PW / 2, y + 140
    b.append(f'<circle cx="{cx}" cy="{cy}" r="55" fill="none" stroke="var(--faint)" stroke-width="1" class="in"/>')
    b.append(f'<circle class="ring" cx="{cx}" cy="{cy}" r="55" fill="none" stroke="var(--acc)" stroke-width="1.6" stroke-linecap="round" transform="rotate(-90 {cx} {cy})"/>')
    b.append(f'<g class="in">{T("25:00", cx, cy + 12, 38, "serif", "var(--ink)", 0, "middle")}{T("FOCUS 1 OF 4", cx, cy + 32, 8, "mono", "var(--muted)", 1.2, "middle")}</g>')
    b.append(f'<g class="in in2">{T("Not now.", cx, cy + 102, 22, "italic", "var(--ink)", 0, "middle")}{T("You've got this.", cx, cy + 124, 16, "italic", "var(--muted)", 0, "middle")}</g>')
    return wrap(860, 360, "".join(b), th, css)

# 3. Three linked tiles
def tile(th, num, kicker, title, lines, foot):
    b = [T(num, 0, 20, 11, "mono", "var(--acc)", 2), T(kicker, 272, 20, 11, "mono", "var(--muted)", 2, "end"),
         '<rect y="32" width="272" height="1.5" fill="var(--ink)"/>', T(title, -2, 92, 46, "serif")]
    for i, l in enumerate(lines):
        b.append(T(l, 0, 124 + i * 20, 15, "italic", "var(--muted)"))
    b.append('<rect y="178" width="272" height="0.75" fill="var(--faint)"/>')
    b.append(T(foot, 0, 200, 10, "mono", "var(--ink)", 1.6))
    return wrap(272, 208, "".join(b), th)
TILES = {
 "tile-vedrino": ("01", "ANDROID", "Vedrino", ["Take your focus back", "from short videos."], "VEDRINO.WEBSITE  →"),
 "tile-hobee":   ("02", "FLUTTER", "Hobee", ["An ad-free Reddit gallery.", "Just the pictures."], "GITHUB / HOBEE  →"),
 "tile-oss":     ("03", "OPEN SOURCE", "Docs fixes", ["Small doc bugs in", "Flutter and Dart."], "5 OPEN  ·  READ BELOW"),
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
for th in THEMES:
    open(f"{out}/masthead-{th}.svg", "w").write(masthead(th))
    open(f"{out}/vedrino-{th}.svg", "w").write(vedrino(th))
    for k, v in TILES.items():
        open(f"{out}/{k}-{th}.svg", "w").write(tile(th, *v))
print("built")
