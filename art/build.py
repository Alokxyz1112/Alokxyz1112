# Builds the README artwork. Every word is converted to outlined paths so it renders the same on GitHub.
import os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
G = "/usr/share/fonts/truetype/sand-box/google/"
FONTS = {"serif": G+"Instrument Serif/InstrumentSerif-Regular.ttf", "italic": G+"Instrument Serif/InstrumentSerif-Italic.ttf",
         "mono": G+"IBM Plex Mono/IBMPlexMono-Regular.ttf"}
_c = {}
def font(k):
    if k not in _c:
        f = TTFont(FONTS[k]); _c[k] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _c[k]
def width(s, k, size, track=0):
    f, gs, cm, upm = font(k)
    return sum(gs[cm.get(ord(ch), cm[32])].width for ch in s) * size / upm + track * len(s)
GLYPHS = {}
def T(s, x, y, size, k="serif", fill="var(--ink)", track=0, anchor="start", extra=""):
    # Each glyph is outlined once into <defs> and reused, which keeps the files small.
    f, gs, cm, upm = font(k); sc = size / upm
    if anchor == "end": x -= width(s, k, size, track)
    if anchor == "middle": x -= width(s, k, size, track) / 2
    cx, out = x, []
    for ch in s:
        gn = cm.get(ord(ch), cm[32]); g = gs[gn]
        if ch != " ":
            gid = f"{k[0]}{ord(ch):x}"
            if gid not in GLYPHS:
                pen = SVGPathPen(gs, ntos=lambda v: str(round(v)))
                g.draw(pen); GLYPHS[gid] = pen.getCommands()
            out.append(f'<use href="#{gid}" x="{cx/sc:.0f}" y="{-y/sc:.0f}"/>')
        cx += g.width * sc + track
    return f'<g {extra} fill="{fill}" transform="scale({sc:.5f} {-sc:.5f})">{"".join(out)}</g>'

# v3: no paper panels. Art sits on GitHub's own background; ink and one amber accent only.
# Palette: warm paper and ink, one burnt amber accent. Dark mode is the same palette inverted.
THEMES = {"light": dict(ink="#141414", muted="#6B655B", faint="#D9D3C7", paper="#F4F1EA"),
          "dark":  dict(ink="#EDE8DC", muted="#A39E93", faint="#34312C", paper="#121212")}
ACC = "#C8772E"
PAD = 28
def wrap(w, h, body, th, css=""):
    t = THEMES[th]
    w, h = w + 2*PAD, h + 2*PAD
    defs = "".join(f'<path id="{i}" d="{d}"/>' for i, d in GLYPHS.items()); GLYPHS.clear()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>svg{{--ink:{t["ink"]};--muted:{t["muted"]};--faint:{t["faint"]};--paper:{t["paper"]};--acc:{ACC}}}{css}</style>'
            f'<defs>{defs}</defs><g transform="translate({PAD} {PAD})">{body}</g></svg>')

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
    b.append(f'<g>{T("the thing I'm", 412, 62, 20, "italic", "var(--acc)")}{T("making right now", 412, 84, 20, "italic", "var(--acc)")}</g>')
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

# 4. Fleuron divider: a hairline draws out from the centre around a small amber mark.
def divider(th):
    css = ("@keyframes draw{0%,62%{transform:scaleX(1)}76%{transform:scaleX(0)}100%{transform:scaleX(1)}}"
           "@keyframes turn{0%,62%{transform:rotate(0)}100%{transform:rotate(90deg)}}"
           ".l{transform-box:fill-box;animation:draw 8s cubic-bezier(.6,0,.2,1) infinite}"
           ".l1{transform-origin:right}.l2{transform-origin:left}"
           ".m{transform-box:fill-box;transform-origin:center;animation:turn 8s cubic-bezier(.6,0,.2,1) infinite}")
    b = ['<rect class="l l1" x="0" y="11.6" width="406" height="0.8" fill="var(--muted)"/>',
         '<rect class="l l2" x="454" y="11.6" width="406" height="0.8" fill="var(--muted)"/>',
         '<g transform="translate(430 12)"><g class="m"><rect x="-6" y="-6" width="12" height="12" transform="rotate(45)" fill="none" stroke="var(--acc)" stroke-width="1.3"/>'
         '<circle r="2" fill="var(--acc)"/></g></g>',
         '<circle cx="414" cy="12" r="1.2" fill="var(--muted)"/><circle cx="446" cy="12" r="1.2" fill="var(--muted)"/>']
    return wrap(860, 24, "".join(b), th, css).replace('<rect width="916" height="80" fill="var(--paper)"/>','').replace(f'height="{24+2*PAD}"', 'height="56"').replace(f'viewBox="0 0 {860+2*PAD} {24+2*PAD}"', f'viewBox="0 {PAD-16} {860+2*PAD} 56"')

# 5. Field notes card. Drawn at 600 wide so it stays legible on a phone.
def fieldnotes(th):
    css = ""
    b = [T("FIELD NOTES", 0, 20, 12, "mono", "var(--muted)", 2), T("NO. 02", 600, 20, 12, "mono", "var(--muted)", 2, "end"),
         '<rect y="32" width="600" height="1.5" fill="var(--ink)"/>',
         T("Lab bench to", 0, 92, 50, "serif"), T("home screen.", 0, 140, 50, "italic", "var(--muted)")]
    rows = [("STUDYING", ["Biotech, and bioinformatics with Python"]),
            ("READING", ["Mastering Python for Bioinformatics"]),
            ("BUILDING", ["Vedrino, a focus app for Android"]),
            ("STACK", ["Kotlin, Compose, Flutter, Dart, Firebase,", "Cloudflare Workers, Vercel, Python"])]
    y = 196
    for k, vs in rows:
        b.append(f'<rect y="{y-26}" width="600" height="0.75" fill="var(--faint)"/>')
        b.append(T(k, 0, y - 3, 11, "mono", "var(--acc)" if k == "BUILDING" else "var(--muted)", 2))
        for j, v in enumerate(vs):
            b.append(T(v, 110, y + j * 24, 20, "italic" if k == "READING" else "serif"))
        y += 24 * len(vs) + 18
    b.append(f'<rect y="{y-26}" width="600" height="0.75" fill="var(--faint)"/>')
    H = y - 10
    return wrap(600, H + 6, "".join(b), th, css)

# 6. Projects, one row each, drawn at 600 wide so they stay legible on a phone.
def project(th, num, kicker, title, line, foot):
    b = [T(num, 0, 22, 12, "mono", "var(--acc)", 2), T(kicker, 600, 22, 12, "mono", "var(--muted)", 2, "end"),
         '<rect y="34" width="600" height="1" fill="var(--ink)"/>',
         T(title, -2, 98, 60, "serif"),
         T(line, 0, 134, 21, "italic", "var(--muted)"),
         T(foot, 600, 98, 12, "mono", "var(--ink)", 1.8, "end")]
    return wrap(600, 140, "".join(b), th)
PROJECTS = {
 "proj-vedrino": ("01", "ANDROID", "Vedrino", "Take your focus back from short videos.", "VEDRINO.WEBSITE  →"),
 "proj-hobee":   ("02", "FLUTTER", "Hobee", "An ad-free Reddit gallery. Just the pictures.", "GITHUB / HOBEE  →"),
 "proj-pixelfixo": ("03", "ANDROID", "Pixelfixo", "Small photos made big and sharp, offline.", "GITHUB / PIXELFIXO  →"),
}

# 7. Ledger of documentation fixes (from public pull requests and reviews).
def ledger(th):
    rows = [("FLUTTER / PACKAGES", "in_app_purchase", "completePurchase docs named a missing exception"),
            ("FLUTTER / PACKAGES", "go_router", "when GoRouterState.name and path are null"),
            ("DART SDK", "dart:async", "\"concurrent\" in the record Future.wait docs"),
            ("DART SDK", "linter", "why a key helps in use_key_in_widget_constructors"),
            ("DART SDK", "linter", "the unrelated mounted check, explained")]
    css = ("@keyframes ink{0%,80%{opacity:1;transform:none}86%,92%{opacity:0;transform:translateX(-6px)}100%{opacity:1;transform:none}}"
           ".row{animation:ink 12s ease-out infinite}")
    b = [T("LEDGER", 0, 20, 12, "mono", "var(--muted)", 2), T("NO. 03", 600, 20, 12, "mono", "var(--muted)", 2, "end"),
         '<rect y="32" width="600" height="1.5" fill="var(--ink)"/>',
         T("Small fixes,", 0, 90, 50, "serif"), T("filed carefully.", 0, 138, 50, "italic", "var(--muted)")]
    for i, (repo, area, what) in enumerate(rows):
        y = 194 + i * 66
        b.append(f'<g class="row" style="animation-delay:{i*0.45:.2f}s">'
                 + T(f"{i+1:02d}", 0, y, 12, "mono", "var(--acc)", 2) + T(area, 44, y + 1, 22, "italic")
                 + T(repo, 600, y, 11, "mono", "var(--muted)", 1.6, "end")
                 + T(what, 44, y + 28, 18, "serif", "var(--muted)") + '</g>')
        b.append(f'<rect y="{y+44}" width="600" height="0.75" fill="var(--faint)"/>')
    b.append(T("ALL FIVE IN REVIEW", 0, 194 + 5 * 66 + 2, 11, "mono", "var(--acc)", 2))
    return wrap(600, 194 + 5 * 66 + 8, "".join(b), th, css)

# 8. Signature footer: the name writes itself, then the colophon.
def signature(th):
    css = ("@keyframes write{0%,70%{transform:scaleX(1)}76%{transform:scaleX(0)}100%{transform:scaleX(1)}}"
           ".w{transform-box:fill-box;transform-origin:left;animation:write 9s cubic-bezier(.5,0,.3,1) infinite}")
    sig = T("Alok", 0, 80, 84, "italic", "var(--ink)")
    b = ['<rect width="600" height="1.5" fill="var(--ink)"/>',
         f'<clipPath id="c"><rect class="w" x="-10" y="0" width="200" height="100"/></clipPath><g clip-path="url(#c)">{sig}</g>',
         '<path d="M2 88 C 50 82, 110 92, 150 84" fill="none" stroke="var(--acc)" stroke-width="1.4" stroke-linecap="round"/>',
         T("THANKS FOR READING", 600, 40, 11, "mono", "var(--muted)", 2, "end"),
         T("vedrino.website", 600, 72, 22, "italic", "var(--ink)", 0, "end"),
         T("SET IN INSTRUMENT SERIF AND IBM PLEX MONO", 600, 124, 10, "mono", "var(--muted)", 1.6, "end")]
    return wrap(600, 128, "".join(b), th, css)

# 9. Custom stack icons. 48 grid, 1.5 stroke, ink lines, one amber detail each.
ICONS = {
 "Kotlin":   ('<path d="M10 10H38L24 24L38 38H10Z"/>', '<path d="M38 10L10 38"/>'),
 "Compose":  ('<path d="M24 6L39.6 15V33L24 42L8.4 33V15Z"/><path d="M24 15L31.8 19.5V28.5L24 33L16.2 28.5V19.5Z"/>', '<circle cx="24" cy="24" r="2.2" fill="var(--acc)" stroke="none"/>'),
 "Flutter":  ('<path d="M29 7H39L18 28L13 23Z"/><path d="M29 25H39L29 35L39 43H29L20 35Z"/>', '<path d="M24 30L29 35"/>'),
 "Dart":     ('<path d="M14 10L34 10L40 16L40 36L36 40L16 40L10 34L10 14Z"/>', '<path d="M14 10L36 32V40"/>'),
 "Firebase": ('<path d="M12 36L17 8L23 19L27 13L36 36L24 42Z"/>', '<path d="M12 36L27 13"/>'),
 "Workers":  ('<path d="M14 34H35A7 7 0 0 0 35 20A10 10 0 0 0 16 17A8.5 8.5 0 0 0 14 34Z"/>', '<path d="M21 23L18 27L21 31M27 23L30 27L27 31"/>'),
 "Vercel":   ('<path d="M24 9L41 38H7Z"/>', '<path d="M17 38H31"/>'),
 "Python":   ('<path d="M24 7H18A5 5 0 0 0 13 12V19H24V21H11A5 5 0 0 0 6 26V31A5 5 0 0 0 11 36H15V29A5 5 0 0 1 20 24H28A5 5 0 0 0 33 19V12A5 5 0 0 0 28 7Z"/><path d="M24 41H30A5 5 0 0 0 35 36V29H24V27H37A5 5 0 0 0 42 22V17A5 5 0 0 0 37 12H33"/>', '<circle cx="19" cy="12.5" r="1.8" fill="var(--acc)" stroke="none"/>'),
 "Android":  ('<path d="M10 33A14 14 0 0 1 38 33Z"/><path d="M15 15L18.5 21M33 15L29.5 21"/>', '<circle cx="18" cy="27.5" r="1.8" fill="var(--acc)" stroke="none"/><circle cx="30" cy="27.5" r="1.8" fill="var(--acc)" stroke="none"/>'),
 "Git":      ('<circle cx="15" cy="11" r="4"/><circle cx="15" cy="37" r="4"/><path d="M15 15V33M15 28C15 21 33 24 33 15"/>', '<circle cx="33" cy="11" r="4" stroke="var(--acc)"/>'),
}
def stack(th):
    css = ""  # static on purpose: icons always rest visible
    b = [T("THE STACK", 0, 14, 11, "mono", "var(--muted)", 2), '<rect y="24" width="600" height="1" fill="var(--faint)"/>']
    for n, (name, (ink, acc)) in enumerate(ICONS.items()):
        col, row = n % 5, n // 5
        x, y = col * 120 + 36, 44 + row * 108
        b.append(f'<g class="i" style="animation-delay:{n*0.12:.2f}s"><g transform="translate({x} {y})" fill="none" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round">'
                 f'<g stroke="var(--ink)">{ink}</g><g stroke="var(--acc)">{acc}</g></g>'
                 + T(name.upper(), x + 24, y + 72, 10, "mono", "var(--muted)", 1.6, "middle") + '</g>')
    return wrap(600, 228, "".join(b), th, css)

# 10. Small glyphs for the link row, 16 grid.
GLYPHS16 = {
 "g-phone":  '<rect x="4.5" y="1.5" width="7" height="13" rx="1.5"/><path d="M7 12.5H9" stroke="var(--acc)"/>',
 "g-gallery":'<rect x="1.5" y="2.5" width="13" height="11" rx="1"/><path d="M2 12L6 8L9 11L11 9L14 12"/><circle cx="11" cy="5.5" r="1" stroke="var(--acc)"/>',
 "g-zoom":   '<circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14.5 14.5" stroke="var(--acc)"/>',
 "g-doc":    '<path d="M3.5 1.5H9.5L12.5 4.5V14.5H3.5Z"/><path d="M6 8H10M6 11H10" stroke="var(--acc)"/>',
 "g-globe":  '<circle cx="8" cy="8" r="6.5"/><path d="M1.5 8H14.5"/><path d="M8 1.5C5.5 4 5.5 12 8 14.5C10.5 12 10.5 4 8 1.5" stroke="var(--acc)"/>',
}
def glyph(th, k):
    t = THEMES[th]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><g fill="none" stroke="{t["ink"]}" stroke-width="1.2" '
            f'stroke-linecap="round" stroke-linejoin="round">{GLYPHS16[k].replace("var(--acc)", ACC)}</g></svg>')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
for th in THEMES:
    open(f"{out}/masthead-{th}.svg", "w").write(masthead(th))
    open(f"{out}/vedrino-{th}.svg", "w").write(vedrino(th))
    for k, fn in {"signature": signature, "stack": stack}.items():
        open(f"{out}/{k}-{th}.svg", "w").write(fn(th))
    for k in GLYPHS16:
        open(f"{out}/{k}-{th}.svg", "w").write(glyph(th, k))
print("built")
