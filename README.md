# Session 3 — AI for Presentations & Design (Gamma & Figma AI)

Presentation slides + hands-on lab for the **Smart Learning** series. Built as a
lightweight, self-contained slide deck (a web page, **not** a notebook) so you can
present the concepts first, then run the hands-on activity.

> **Live slides:** https://kianraj.github.io/smart-learning-session3-slides/
>
> **Present locally:** open [`index.html`](index.html) in any browser.

## All sessions in this series

| Session | Topic | Live slides |
|---------|-------|-------------|
| 2 | Smart Learning with Google Gemini & NotebookLM | https://kianraj.github.io/smart-learning-session2-slides/ |
| 3 | AI for Presentations & Design (Gamma & Figma AI) | https://kianraj.github.io/smart-learning-session3-slides/ |

## What's inside

| Part | Slides | Content |
|------|--------|---------|
| Motivation & objectives | 1–2 | Why visual communication matters; session outcomes |
| The real tools | 3 | Live screenshots of gamma.app and figma.com, plus in-app step-by-step screens |
| The toolkit | 4 | Gamma vs Figma AI — two tools, two jobs |
| Gamma | 5–8 | How Gamma builds a deck; real in-app step-by-step screenshots; steal-these prompts |
| Figma AI | 9 | Where interface design happens (real screenshot) |
| Design basics | 10–14 | Wireframe → mockup → prototype; real Figma step-by-step screens; screen anatomy; linking flows |
| Hands-on | 15–16 | Build, refine and export your seminar deck; submission checklist |
| Wrap-up | 17 | Recap and links |

Every concept slide carries a **visualization** (inline SVG diagrams — wireframes,
mockups, clickable-flow maps) so students can *see* the design process while doing it.

## Present it

- **Navigate:** `→` / `Space` next · `←` back · `Home` / `End` jump · `F` fullscreen.
- **Click:** right edge of the slide = next, left edge = back. Touch = swipe.
- **Deep-link:** `index.html#8` opens slide 8 directly.

## The hands-on activity (what students submit)

**Task 1 — Generate.** On `gamma.app`, generate a 10–12 slide seminar presentation on
a branch topic (audience + one idea per slide + a visual on each).

**Task 2 — Refine + design touch.** Trim to one idea per slide, add visuals, add title
and summary slides, sketch a Figma wireframe/mockup of the title screen, export as PDF.

**Submit** one PDF (`RollNo_Name_Session3.pdf`) containing: the Gamma share link, the
exported deck, title + content slide screenshots, the Figma wireframe screenshot, and a
3-line reflection on what AI did well vs what you fixed by hand.

## Files

```
smart-learning-session3-slides/
├── index.html          <- the presentation (open / share this)
├── assets/
│   ├── slides.css       <- the "notebook aesthetic" theme
│   └── slides.js        <- keyboard / click / swipe navigation
├── _build_slides.py     <- all slide content lives here; regenerates index.html
└── README.md
```

## Editing the slides

All content lives in one place — [`_build_slides.py`](_build_slides.py). Edit the
`SLIDES` list or a `viz_*` diagram, then regenerate:

```bash
python _build_slides.py
```
