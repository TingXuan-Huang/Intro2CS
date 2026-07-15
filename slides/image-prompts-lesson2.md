# Image prompts — Lesson 2 slide deck (Files & pandas)

Same workflow as Lesson 1: generate each image, save it as a **PNG with the exact filename**
into `slides/assets/`, reload `Lesson2_Files_and_pandas_Slides.html`, and it replaces its
placeholder automatically. Press **P** in the deck to hide unfilled placeholders.

**Deck motif:** a customs house at a harbor — data crossing the disk boundary as cargo
under inspection. Keep every image inside this one scene-world.

## Shared style block (prepend to every prompt — same as Lesson 1)

> Flat editorial textbook illustration with a screen-print / risograph feel and subtle paper
> grain. Warm cream background (#F7F2E9). Limited palette: warm amber (#C2762B), deep teal
> (#2E7D74), muted violet (#6B5CA5), slate gray (#4A5560), dark ink outlines (#221D15).
> Generous negative space, calm and precise, mid-century science-textbook mood.
> **No words, no letters, no numbers anywhere in the image.**

---

## IMG L2-01 — Title hero ★ core

- **File:** `assets/l2-img-01-hero.png` · **Slide 1** (right panel) · **Aspect 4:5 portrait**, ≥1100 px wide
- **Prompt:** A small customs house on a wooden harbor dock at morning. A rowing boat below
  delivers wooden crates; one crate sits open on the inspection table under a desk lamp, its
  contents (small ceramic objects) laid out in a neat row beside it. An inspector's rubber
  stamp and a closed ledger wait at the table's edge. Teal water, amber lamplight, slate
  shadows. Composition weighted low; calm cream sky above.

## IMG L2-02 — The inspector (optional garnish)

- **File:** `assets/l2-img-02-inspector.png` · **Slide 5** (small corner card) · **Aspect 1:1**, ≥700 px
- **Prompt:** A detective's brass magnifying glass held over a large paper ledger ruled into
  a grid like a spreadsheet. Under the lens, one grid cell shows a subtle flaw (a torn corner).
  Around the ledger, small blank index cards are pinned down with round pins and connected by
  a thin red thread. Overhead view, warm lamplight.

## IMG L2-03 — The restorer (optional garnish)

- **File:** `assets/l2-img-03-restorer.png` · **Slide 8** (small corner card) · **Aspect 1:1**, ≥700 px
- **Prompt:** An art restorer's gloved hand with a fine brush working on a framed painting
  that is a spreadsheet-like grid of small cells. The cells already passed by the brush glow
  in clean teal and amber; the untouched cells ahead are faded, dusty gray. Easel view,
  three-quarter angle, one soft work lamp.

## IMG L2-04 — Cleared for export ★ core

- **File:** `assets/l2-img-04-stamped.png` · **Slide 14** (bottom banner) · **Aspect 2:1 wide**, ≥1400 px wide
- **Prompt:** The customs dock at dusk, outbound side. A single wooden crate ready for the
  boat, carrying a fresh paper band-seal around its middle and a clean inked stamp mark
  (a simple geometric emblem, not text). The inspection ledger lies closed beside it, lamp
  turned low, teal evening water behind. Quiet, resolved mood — the day's work done.

---

### Generation tips

- Ask for **flat illustration / risograph / screen-print**; reject photorealistic or
  glow-heavy outputs — they clash with the deck.
- Keep all four images in the same customs-house scene-world: same dock, same lamp, same
  crate style. Consistency between slides 1 and 14 (morning arrival → dusk departure) is
  the visual payoff.
- Generate slightly larger than needed; the deck crops with `object-fit: cover`.
- Core: L2-01, L2-04. Optional garnish: L2-02, L2-03.
