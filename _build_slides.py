#!/usr/bin/env python3
"""
Build the lecture slide deck for:

    Session 3 — AI for Presentations & Design (Gamma & Figma AI)

Content lives here (one place). Run this to regenerate the HTML:

    python _build_slides.py

Output:
    index.html                 <- the full presentation (open / share this)
Shared look & behaviour:
    assets/slides.css , assets/slides.js
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Archivo:wght@700;800;900&"
         "family=IBM+Plex+Sans:wght@400;500;600&"
         "family=IBM+Plex+Mono:wght@400;500;600&display=swap")

INK, PEN, RED, YEL, MUT, LINE, GRN = (
    "#17233B", "#2B4FD8", "#E4572E", "#FFE066", "#6E7688", "#E7E4DB", "#2E9E5B")
PUR = "#7C4DFF"   # accent for design/Figma

# ---------- render helpers ----------
def slide(*body, cls=""):
    return f'<section class="slide {cls}"><div class="inner">' + "".join(body) + "</div></section>"

def eyebrow(tag):   return f'<p class="eyebrow">Session 3 <span class="dot">•</span> {tag}</p>'
def h1(t):   return f"<h1>{t}</h1>"
def h2(t):   return f"<h2>{t}</h2>"
def lead(t): return f'<p class="lead">{t}</p>'
def p(t):    return f"<p>{t}</p>"
def muted(t):return f'<p class="muted">{t}</p>'

def cards(items, cols=3):
    inner = "".join(
        f'<div class="card">{("<span class=k>"+k+"</span>") if k else ""}'
        f'<h3>{t}</h3><p>{d}</p></div>' for k, t, d in items)
    return f'<div class="cards c{cols}">{inner}</div>'

def tick(items):  return '<ul class="tick">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def steps(items): return '<ol class="steps">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def rows(pairs):
    r = "".join(f'<div class="row"><span class="lbl">{k}</span><span>{v}</span></div>' for k, v in pairs)
    return f'<div class="rows">{r}</div>'
def arch(txt):   return f'<div class="arch">{html.escape(txt)}</div>'
def flash(txt):  return f'<div class="flash">{txt}</div>'
def two(a, b):   return f'<div class="two"><div>{a}</div><div>{b}</div></div>'
def tags(items, on=()):
    return '<div class="tags">' + "".join(
        f'<span class="tag {"on" if t in on else ""}">{t}</span>' for t in items) + "</div>"
def prompt(text, tag="prompt"):
    return (f'<div class="prompt-box"><span class="pl">{tag}</span>'
            f'<span class="pt">{html.escape(text)}</span></div>')
def handoff(title, note, chip):
    return ('<div class="handoff"><p class="eyebrow">Now — hands-on</p>'
            f'<div class="big">{title}</div><p class="muted">{note}</p>'
            f'<span class="file">{chip}</span></div>')

def shot(src, url, cap="", crop=False):
    """A real-website screenshot in a browser frame (image self-hosted in assets/img)."""
    dots = "".join(f'<i style="background:{c}"></i>' for c in ("#E4572E", "#FFC93C", "#2E9E5B"))
    cap = f'<div class="cap">{cap}</div>' if cap else ""
    cls = "imgwrap crop" if crop else "imgwrap"
    return (f'<div class="shot"><div class="bar">{dots}<span class="url">{url}</span></div>'
            f'<div class="{cls}"><img src="assets/img/{src}" alt="{url} screenshot"></div>{cap}</div>')

# ---------- viz helpers ----------
def viz(svg, cap="", legend=None):
    leg = ""
    if legend:
        leg = '<div class="viz-legend">' + "".join(
            f'<span><i style="background:{c}"></i>{t}</span>' for c, t in legend) + "</div>"
    cap = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<div class="viz">{svg}{cap}{leg}</div>'

def _defs():
    return (f'<defs>'
            f'<marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{MUT}"/></marker>'
            f'<marker id="ap" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{PUR}"/></marker>'
            f'<marker id="ag" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="{GRN}"/></marker>'
            f'</defs>')

def _arrow(x1, y1, x2, y2, color=MUT, mid="a"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#{mid})"/>'

def _winframe(x, y, w, h, fill="#fff", stroke=LINE, title=None):
    """A little browser/app window with three dots."""
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="22" rx="9" fill="#EFEDE5"/>'
    s += f'<rect x="{x}" y="{y+11}" width="{w}" height="11" fill="#EFEDE5"/>'
    for i, c in enumerate(["#E4572E", "#FFC93C", "#2E9E5B"]):
        s += f'<circle cx="{x+14+i*14}" cy="{y+11}" r="4" fill="{c}"/>'
    if title:
        s += f'<text x="{x+w/2}" y="{y+15}" text-anchor="middle" font-size="10" fill="{MUT}" class="mono">{title}</text>'
    return s

def viz_compare():
    def panel(x, title, color, icon, lines):
        s = f'<rect x="{x}" y="20" width="300" height="234" rx="14" fill="#fff" stroke="{color}" stroke-width="2"/>'
        s += f'<text x="{x+24}" y="62" font-size="30">{icon}</text>'
        s += f'<text x="{x+70}" y="55" font-size="18" font-weight="700" fill="{INK}">{title}</text>'
        yy = 100
        for ln in lines:
            s += f'<circle cx="{x+28}" cy="{yy-4}" r="3" fill="{color}"/>'
            s += f'<text x="{x+42}" y="{yy}" font-size="13.5" fill="{INK}">{ln}</text>'
            yy += 34
        return s
    g = panel(30, "Gamma", PEN, "📊",
              ["Presentations, docs &amp; webpages", "Generate from a prompt or outline",
               "Instant themes &amp; layouts", "Export to PDF / PPT / link"])
    f = panel(390, "Figma AI", PUR, "🎨",
              ["Interface &amp; visual design", "Wireframes → mockups → prototypes",
               "AI: generate, rename, fill content", "The industry design standard"])
    svg = f'<svg viewBox="0 0 720 274">{g}{f}</svg>'
    return viz(svg, "Gamma writes &amp; designs your content. Figma is where interfaces are designed and prototyped.",
               [(PEN, "Gamma — content &amp; decks"), (PUR, "Figma AI — UI / UX design")])

def viz_gamma_flow():
    s = _defs()
    s += f'<rect x="16" y="70" width="170" height="70" rx="10" fill="#fff" stroke="{LINE}"/>'
    s += f'<text x="101" y="98" text-anchor="middle" font-size="13" fill="{INK}">Your topic</text>'
    s += f'<text x="101" y="118" text-anchor="middle" font-size="11" fill="{MUT}" class="mono">+ a short outline</text>'
    s += _arrow(188, 105, 246, 105, MUT, "a")
    s += f'<rect x="248" y="72" width="150" height="66" rx="12" fill="{PEN}"/>'
    s += f'<text x="323" y="102" text-anchor="middle" font-size="16" fill="#fff" font-weight="700">Gamma</text>'
    s += f'<text x="323" y="122" text-anchor="middle" font-size="10.5" fill="#cdd8ff" class="mono">generates &amp; designs</text>'
    s += _arrow(400, 105, 458, 105, PEN, "ap")
    # deck of slide thumbnails
    for i in range(4):
        x = 466 + i*56
        s += _winframe(x, 60+i*4, 210-i*0, 92, "#fff", LINE) if False else ""
        s += f'<rect x="{x}" y="{62+i*3}" width="200" height="86" rx="8" fill="#fff" stroke="{LINE}"/>'
    # front slide content
    fx = 466
    s += f'<rect x="{fx}" y="62" width="200" height="86" rx="8" fill="#fff" stroke="{PEN}" stroke-width="1.6"/>'
    s += f'<rect x="{fx+14}" y="78" width="120" height="12" rx="3" fill="{INK}"/>'
    s += f'<rect x="{fx+14}" y="98" width="150" height="7" rx="3" fill="{LINE}"/>'
    s += f'<rect x="{fx+14}" y="110" width="130" height="7" rx="3" fill="{LINE}"/>'
    s += f'<rect x="{fx+150}" y="98" width="36" height="34" rx="4" fill="rgba(43,79,216,.15)"/>'
    svg = f'<svg viewBox="0 0 700 200">{s}</svg>'
    return viz(svg, "Type a topic + a rough outline → Gamma writes the copy and lays out a full deck in seconds.")

def viz_fidelity():
    def phone(x, style):
        s = f'<rect x="{x}" y="24" width="120" height="200" rx="16" fill="#fff" stroke="{LINE}" stroke-width="1.6"/>'
        if style == "wire":
            s += f'<rect x="{x+16}" y="44" width="88" height="14" rx="3" fill="#E7E2D6"/>'
            s += f'<rect x="{x+16}" y="66" width="88" height="52" rx="4" fill="none" stroke="{MUT}" stroke-dasharray="4 3"/>'
            s += f'<line x1="{x+16}" y1="70" x2="{x+104}" y2="114" stroke="{MUT}" stroke-dasharray="3 3"/>'
            s += f'<line x1="{x+104}" y1="70" x2="{x+16}" y2="114" stroke="{MUT}" stroke-dasharray="3 3"/>'
            for i in range(3): s += f'<rect x="{x+16}" y="{128+i*20}" width="88" height="12" rx="3" fill="#EEEAE0"/>'
            s += f'<rect x="{x+16}" y="192" width="60" height="18" rx="6" fill="#E7E2D6"/>'
        elif style == "mock":
            s += f'<rect x="{x+16}" y="44" width="88" height="14" rx="3" fill="{INK}"/>'
            s += f'<rect x="{x+16}" y="66" width="88" height="52" rx="4" fill="rgba(124,77,255,.18)"/>'
            s += f'<circle cx="{x+40}" cy="92" r="12" fill="{PUR}"/>'
            for i,c in enumerate(["#EEEAE0","#EEEAE0","#EEEAE0"]): s += f'<rect x="{x+16}" y="{128+i*20}" width="88" height="12" rx="3" fill="{c}"/>'
            s += f'<rect x="{x+16}" y="192" width="60" height="18" rx="6" fill="{PUR}"/>'
        else:  # proto
            s += f'<rect x="{x+16}" y="44" width="88" height="14" rx="3" fill="{INK}"/>'
            s += f'<rect x="{x+16}" y="66" width="88" height="52" rx="4" fill="rgba(124,77,255,.18)"/>'
            s += f'<circle cx="{x+40}" cy="92" r="12" fill="{PUR}"/>'
            for i in range(3): s += f'<rect x="{x+16}" y="{128+i*20}" width="88" height="12" rx="3" fill="#EEEAE0"/>'
            s += f'<rect x="{x+16}" y="192" width="60" height="18" rx="6" fill="{PUR}"/>'
            s += f'<circle cx="{x+90}" cy="201" r="10" fill="none" stroke="{GRN}" stroke-width="2"/>'
            s += f'<path d="M{x+86} 201 l4 4 l7 -8" fill="none" stroke="{GRN}" stroke-width="2"/>'
        return s
    s = _defs()
    labels = ["Wireframe", "Mockup", "Prototype"]
    subs = ["structure only", "colour + style", "clickable + flow"]
    xs = [40, 230, 420]
    styles = ["wire", "mock", "proto"]
    for x, st, lb, sb in zip(xs, styles, labels, subs):
        s += phone(x, st)
        s += f'<text x="{x+60}" y="248" text-anchor="middle" font-size="14" font-weight="700" fill="{INK}">{lb}</text>'
        s += f'<text x="{x+60}" y="266" text-anchor="middle" font-size="11" fill="{MUT}" class="mono">{sb}</text>'
    s += _arrow(168, 130, 224, 130, MUT, "a")
    s += _arrow(358, 130, 414, 130, MUT, "a")
    s += f'<text x="300" y="292" text-anchor="middle" font-size="12" fill="{PUR}" class="mono">low fidelity  →  high fidelity</text>'
    svg = f'<svg viewBox="0 0 560 300">{s}</svg>'
    return viz(svg, "Design grows in fidelity: sketch the structure, then style it, then make it clickable.")

def viz_wireframe():
    x, y, w, h = 60, 20, 470, 250
    s = _winframe(x, y, w, h, "#fff", LINE, "your-app.com")
    # nav
    s += f'<rect x="{x+16}" y="{y+34}" width="70" height="14" rx="3" fill="{INK}"/>'
    for i in range(3):
        s += f'<rect x="{x+w-160+i*50}" y="{y+36}" width="38" height="10" rx="3" fill="#E7E2D6"/>'
    # hero
    s += f'<rect x="{x+16}" y="{y+62}" width="250" height="20" rx="4" fill="#DfDbd0"/>'
    s += f'<rect x="{x+16}" y="{y+90}" width="200" height="10" rx="3" fill="#EEEAE0"/>'
    s += f'<rect x="{x+16}" y="{y+106}" width="220" height="10" rx="3" fill="#EEEAE0"/>'
    s += f'<rect x="{x+16}" y="{y+128}" width="90" height="24" rx="6" fill="{PUR}"/>'
    # image placeholder
    ix, iy, iw, ih = x+290, y+62, 160, 90
    s += f'<rect x="{ix}" y="{iy}" width="{iw}" height="{ih}" rx="6" fill="none" stroke="{MUT}" stroke-dasharray="5 4"/>'
    s += f'<line x1="{ix}" y1="{iy}" x2="{ix+iw}" y2="{iy+ih}" stroke="{MUT}" stroke-dasharray="4 4"/>'
    s += f'<line x1="{ix+iw}" y1="{iy}" x2="{ix}" y2="{iy+ih}" stroke="{MUT}" stroke-dasharray="4 4"/>'
    # cards
    for i in range(3):
        cx = x+16+i*150
        s += f'<rect x="{cx}" y="{y+168}" width="132" height="72" rx="6" fill="#F7F6F1" stroke="{LINE}"/>'
        s += f'<rect x="{cx+12}" y="{y+180}" width="60" height="9" rx="3" fill="#DfDbd0"/>'
        s += f'<rect x="{cx+12}" y="{y+196}" width="108" height="7" rx="3" fill="#EEEAE0"/>'
        s += f'<rect x="{cx+12}" y="{y+208}" width="96" height="7" rx="3" fill="#EEEAE0"/>'
    # numbered badges pinned to each block (explained in the list beside the viz)
    def badge(n, bx, by):
        return (f'<circle cx="{bx}" cy="{by}" r="13" fill="{PUR}"/>'
                f'<text x="{bx}" y="{by+4.5}" text-anchor="middle" font-size="13" '
                f'font-weight="700" fill="#fff">{n}</text>')
    s += badge(1, x+w-36, y+41)      # nav
    s += badge(2, x+150, y+72)       # headline
    s += badge(3, x+60, y+140)       # call-to-action
    s += badge(4, ix+iw-18, iy+18)   # image
    s += badge(5, x+w-36, y+204)     # cards
    svg = f'<svg viewBox="0 0 590 290">{s}</svg>'
    return viz(svg, "A wireframe is the skeleton — where things go, before any colour.")

def wireframe_legend():
    return rows([
        ("1 · nav", "logo + links — how users move around; keep it on every screen"),
        ("2 · headline", "one sentence that says what the page is; biggest text on screen"),
        ("3 · CTA", "the call-to-action button — the ONE thing you want the user to do"),
        ("4 · image", "the dashed box = an image placeholder; content comes later"),
        ("5 · cards", "repeating blocks for features, products or options"),
    ])

def viz_prototype():
    s = _defs()
    def screen(x, label):
        t = _winframe(x, 40, 150, 150, "#fff", LINE)
        t += f'<rect x="{x+16}" y="72" width="80" height="12" rx="3" fill="{INK}"/>'
        t += f'<rect x="{x+16}" y="94" width="118" height="8" rx="3" fill="{LINE}"/>'
        t += f'<rect x="{x+16}" y="150" width="70" height="22" rx="6" fill="{PUR}"/>'
        t += f'<text x="{x+75}" y="208" text-anchor="middle" font-size="12" fill="{INK}" class="mono">{label}</text>'
        return t
    s += screen(30, "Home")
    s += screen(275, "Details")
    s += screen(520, "Success")
    s += _arrow(180, 155, 273, 155, PUR, "ap")
    s += f'<text x="226" y="145" text-anchor="middle" font-size="11" fill="{PUR}" class="mono">tap card</text>'
    s += _arrow(425, 155, 518, 155, PUR, "ap")
    s += f'<text x="471" y="145" text-anchor="middle" font-size="11" fill="{PUR}" class="mono">submit</text>'
    svg = f'<svg viewBox="0 0 690 220">{s}</svg>'
    return viz(svg, "A prototype links screens: each button is wired to the next screen, so you can 'click through' the idea.")

def viz_slide_anatomy():
    x, y, w, h = 70, 20, 460, 250
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff" stroke="{LINE}" stroke-width="1.6"/>'
    s += f'<rect x="{x+28}" y="{y+30}" width="250" height="26" rx="5" fill="{INK}"/>'          # title
    s += f'<rect x="{x+28}" y="{y+74}" width="180" height="12" rx="3" fill="#E7E2D6"/>'         # one point
    s += f'<rect x="{x+28}" y="{y+96}" width="150" height="12" rx="3" fill="#EEEAE0"/>'
    s += f'<rect x="{x+28}" y="{y+118}" width="160" height="12" rx="3" fill="#EEEAE0"/>'
    s += f'<rect x="{x+250}" y="{y+74}" width="180" height="130" rx="8" fill="rgba(43,79,216,.12)" stroke="{PEN}"/>'
    s += f'<text x="{x+340}" y="{y+144}" text-anchor="middle" font-size="13" fill="{PEN}" class="mono">one visual</text>'
    s += f'<rect x="{x+28}" y="{y+222}" width="90" height="8" rx="3" fill="#EEEAE0"/>'          # footer
    def call(tx, ty, txt, lx, ly):
        return (f'<line x1="{lx}" y1="{ly}" x2="{tx}" y2="{ty}" stroke="{RED}" stroke-width="1.2"/>'
                f'<circle cx="{lx}" cy="{ly}" r="3" fill="{RED}"/>'
                f'<text x="{tx}" y="{ty}" font-size="11.5" fill="{RED}" class="mono">{txt}</text>')
    s += call(548, 44, "one clear title", x+w-180, y+43)
    s += call(548, 100, "3 short points", x+188, y+96)
    s += call(548, 210, "footer / source", x+118, y+226)
    svg = f'<svg viewBox="0 0 600 290">{s}</svg>'
    return viz(svg, "A slide that lands: one idea, one title, a few words, one strong visual. Let AI draft it — you trim it.")

def viz_prompt_anatomy():
    parts = [("who it's for", "For 2nd-year students,", PUR),
             ("the task", "make a 10-slide deck", PEN),
             ("the topic", "on cloud computing,", RED),
             ("the style", "minimal, one visual per slide.", INK)]
    s = ""; x = 20
    for lbl, txt, col in parts:
        w = 8 + len(txt)*7.6
        s += f'<rect x="{x}" y="40" width="{w}" height="40" rx="8" fill="{col}" opacity="0.14"/>'
        s += f'<rect x="{x}" y="40" width="{w}" height="40" rx="8" fill="none" stroke="{col}"/>'
        s += f'<text x="{x+w/2}" y="65" text-anchor="middle" font-size="13.5" fill="{INK}" class="mono">{txt}</text>'
        s += f'<text x="{x+w/2}" y="105" text-anchor="middle" font-size="11.5" fill="{col}" class="mono">{lbl}</text>'
        x += w + 10
    svg = f'<svg viewBox="0 0 {int(x)} 130">{s}</svg>'
    return viz(svg, "A strong generation prompt names the audience, the task, the topic and the style.")

def viz_taskflow():
    s = _defs()
    steps_ = [("Topic", "#fff", INK), ("Gamma deck", PEN, "#fff"),
              ("Refine", "#fff", INK), ("Export PDF", "rgba(46,158,91,.14)", INK)]
    x = 20
    prev = None
    for i,(t, fill, tc) in enumerate(steps_):
        w = 150
        s += f'<rect x="{x}" y="60" width="{w}" height="66" rx="12" fill="{fill}" stroke="{GRN if i==3 else (PEN if i==1 else LINE)}" stroke-width="{2 if i in (1,3) else 1.4}"/>'
        s += f'<text x="{x+w/2}" y="98" text-anchor="middle" font-size="15" fill="{tc}" font-weight="700">{t}</text>'
        if prev is not None:
            s += _arrow(prev, 93, x-2, 93, MUT, "a")
        prev = x+w
        x += w+42
    svg = f'<svg viewBox="0 0 {x} 150">{s}</svg>'
    return viz(svg, "The lab in one line: pick a topic → generate with Gamma → refine theme &amp; visuals → export a PDF to submit.")

# ============================================================
#  SLIDES
# ============================================================
SLIDES = [
  # 1 — title
  slide(
    eyebrow("Smart Learning Series"),
    h1("AI for Presentations<br>&amp; Design"),
    lead("Type your idea → get a <mark>finished deck</mark> and a <mark>clean app design</mark> "
         "in minutes — with Gamma and Figma AI."),
    tags(["Tools: Gamma + Figma AI", "Mode: hands-on lab", "Deliverable: a seminar deck"],
         on=["Mode: hands-on lab"]),
    muted("Press → / Space to advance · ← to go back · F for fullscreen"),
  ),
  # 2 — why + objectives
  slide(
    eyebrow("Why &amp; what"),
    h2("Presenting well is a career skill"),
    two(
      p("<b>Professional communication and visual presentation</b> are core academic "
        "<i>and</i> industry skills — and layout/polish usually eats the time you meant "
        "to spend on the message. AI flips that.") +
      flash("Today: AI handles the <b>layout and polish</b>; you own the <b>message</b>."),
      tick([
        "Generate a <b>presentation or report</b> with Gamma.",
        "Know <b>Figma AI</b> and where interface design happens.",
        "Tell apart <b>wireframe · mockup · prototype</b>.",
        "Ship a <b>seminar deck</b> you built and refined yourself.",
      ]),
    ),
  ),
  # 4 — two tools, two jobs
  slide(
    eyebrow("The toolkit · visualize it"),
    h2("Two tools, two jobs"),
    viz_compare(),
    muted("Use Gamma when the output is a deck, doc or page. Reach for Figma when you design a screen or an app."),
  ),
  # 5 — gamma flow
  slide(
    eyebrow("Gamma · visualize it"),
    h2("How Gamma builds a deck"),
    viz_gamma_flow(),
    cards([
      ("1", "From a prompt", "Describe the topic → a full first-draft deck."),
      ("2", "From your text", "Paste notes → Gamma structures them into slides."),
      ("3", "Themes", "One click restyles the whole deck consistently."),
      ("4", "Export", "Share a link, or export to PDF / PowerPoint — docs &amp; webpages too."),
    ], cols=4),
  ),
  # 6 — inside gamma: steps 1-2 (real UI)
  slide(
    eyebrow("Gamma · inside the tool"),
    h2("Step by step — start to outline"),
    two(
      shot("gamma_step_mode.jpg", "gamma.app → Create with AI",
           "STEP 1 · sign in → Create with AI → pick “Generate” (or paste / import your own notes)."),
      shot("gamma_step_prompt.jpg", "gamma.app → Generate",
           "STEP 2 · choose Presentation, set the card count, type your topic → “Generate outline”."),
    ),
    muted("Real screens from Gamma (source: Gamma Help Center) — this is exactly what you'll see in the lab."),
  ),
  # 7 — inside gamma: steps 3-4 (real UI)
  slide(
    eyebrow("Gamma · inside the tool"),
    h2("Step by step — cards, visuals, done"),
    two(
      shot("gamma_step_review.jpg", "gamma.app → review cards",
           "STEP 3 · review the outline it built, adjust the number of cards → “Continue”."),
      shot("gamma_step_images.jpg", "gamma.app → image source",
           "STEP 4 · pick where visuals come from — AI images, web images or illustrations."),
    ),
    flash("STEP 5 · select any card → <b>Edit with AI</b> (improve writing, translate, make longer) "
          "· then <b>Share → Export → PDF / PowerPoint</b>."),
  ),
  # 6 — gamma prompts
  slide(
    eyebrow("Gamma"),
    h2("Prompts you can steal today"),
    two(
      prompt("Create a 10-slide seminar presentation on 'Edge Computing' for 2nd-year "
             "CSE students. One idea per slide, minimal text, a visual on each.", "presentation") +
      prompt("Turn these notes into a 12-slide deck with an agenda, sections and a "
             "summary slide. [paste notes]", "from notes"),
      prompt("Write a 2-page project report on my mini-project: problem, approach, "
             "results, conclusion. Formal tone. [paste details]", "report") +
      prompt("Restyle this deck with a clean, minimal theme and consistent heading "
             "sizes.", "refine"),
    ),
    flash("Name the <b>audience, task, topic and style</b> — vague prompts give generic decks."),
  ),
  # 8 — fidelity ladder
  slide(
    eyebrow("Design basics · visualize it"),
    h2("Wireframe → Mockup → Prototype"),
    viz_fidelity(),
    muted("Fidelity just means level of detail. Wireframe = where things go · Mockup = how it looks · Prototype = how it behaves. You do all three in Figma — free for students, runs in the browser."),
  ),
  # — inside figma: steps 1-2 (real UI)
  slide(
    eyebrow("Figma · inside the tool"),
    h2("Step by step — frame, then wireframe"),
    two(
      shot("figma_step1_frame.jpg", "figma.com → new design file",
           "STEP 1 · press F (Frame tool) and pick a screen size — that frame IS your screen."),
      shot("figma_step2_layout.jpg", "figma.com → canvas + layers",
           "STEP 2 · block out the wireframe inside the frame — boxes, text, buttons. Layers list on the left."),
    ),
    muted("Real screens from Figma (source: Figma Help Center) — style it into a mockup once the blocks feel right."),
  ),
  # — inside figma: steps 3-4 (real UI)
  slide(
    eyebrow("Figma · inside the tool"),
    h2("Step by step — make it clickable"),
    two(
      shot("figma_step3_connect.jpg", "figma.com → Prototype mode",
           "STEP 3 · in the Prototype tab, drag the blue arrow from a button to the next screen — that's a connection."),
      shot("figma_step4_present.jpg", "figma.com → Prototype settings",
           "STEP 4 · pick a device for the preview, then press ▶ Present and tap through your flow."),
    ),
    flash("A prototype is just screens <b>wired together</b>: tap a button → next screen. That's the whole ladder in one tool: <b>frame → wireframe → mockup → clickable prototype</b>."),
  ),
  # 9 — screen anatomy
  slide(
    eyebrow("Design basics · visualize it"),
    h2("Anatomy of a screen (wireframe)"),
    two(viz_wireframe(), wireframe_legend()),
    muted("Start every design here — block out these five pieces before styling anything."),
  ),
  # 11 — hands-on
  slide(
    eyebrow("Hands-on"),
    h2("Activity — build your seminar deck"),
    viz_taskflow(),
    two(
      steps([
        "On <code>gamma.app</code>: generate a <b>10–12 slide</b> deck on your seminar topic "
        "(audience + one idea per slide + a visual on each).",
        "Refine: pick a clean <b>theme</b>, trim text to phrases, add title &amp; summary slides.",
        "In <b>Figma</b>: sketch a wireframe / mockup of your title screen.",
        "<b>Export as PDF</b> (8–12 slides).",
      ]),
      flash("📸 Keep screenshots as you go — title slide, one content slide, and your "
            "Figma sketch. You'll submit them."),
    ),
  ),
  # 12 — submission + best practice
  slide(
    eyebrow("Deliverable"),
    h2("What to submit — and the bar to clear"),
    two(
      tick([
        "The <b>Gamma share link</b> to your deck",
        "The deck <b>exported as PDF</b> (8–12 slides)",
        "Screenshots: <b>title slide</b> + one <b>content slide</b>",
        "One <b>Figma wireframe / mockup</b> screenshot",
        "3-line <b>reflection</b>: what AI did well, what you fixed by hand",
      ]),
      flash("<b>One idea per slide.</b> Strong contrast, consistent fonts, a visual "
            "beats a paragraph — and never ship placeholder text.<br><br>"
            "Bundle into one PDF → <b>RollNo_Name_Session3.pdf</b>"),
    ),
  ),
  # 13 — wrap up
  slide(
    handoff("From blank page to polished deck — in one session.",
            "Recap — Gamma for decks, docs &amp; pages · Figma AI for screens · "
            "wireframe → mockup → prototype · submit one seminar deck.",
            "gamma.app  ·  figma.com"),
    muted("Submission deadline as announced in class — ask your doubts now or during the lab."),
    cls="handoff-slide",
  ),
]

# ============================================================
#  PAGE SHELL + WRITE
# ============================================================
def page():
    body = "\n".join(SLIDES)
    nav = ('<div class="nav"><button class="up" title="Previous (↑)">↑</button>'
           '<button class="down" title="Next (↓)">↓</button></div>')
    chrome = ('<div class="margin-line"></div><div class="progress"></div>'
              '<div class="counter"></div>'
              '<div class="brand">KIET · Smart Learning · Session 3</div>' + nav)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Session 3 — AI for Presentations &amp; Design (Gamma &amp; Figma AI)</title>
<meta name="description" content="Hands-on lecture slides: build presentations with Gamma and design interfaces with Figma AI.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/slides.css">
</head><body>
<div class="stage">
{body}
</div>
{chrome}
<script src="assets/slides.js"></script>
</body></html>"""

def main():
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
        f.write(page())
    print("wrote index.html  (", len(SLIDES), "slides )")

if __name__ == "__main__":
    main()
