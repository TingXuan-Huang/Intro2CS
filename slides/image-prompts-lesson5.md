# Image prompts — Lesson 5 slide deck (Code Quality & Testing)

Same workflow as Lesson 1: generate each image, save it as a **PNG with the exact filename**
into `slides/assets/`, reload `Lesson5_Code_Quality_Slides.html`, and it replaces its
placeholder automatically. Press **P** in the deck to hide unfilled placeholders.

**Deck motif:** a craftsman's workshop where documents become sealed contracts — quality as
craft, testing as the seal of approval. Keep every image inside this one workshop scene-world.

## Shared style block (prepend to every prompt — same as Lesson 1)

> Flat editorial textbook illustration with a screen-print / risograph feel and subtle paper
> grain. Warm cream background (#F7F2E9). Limited palette: warm amber (#C2762B), deep teal
> (#2E7D74), muted violet (#6B5CA5), slate gray (#4A5560), dark ink outlines (#221D15).
> Generous negative space, calm and precise, mid-century science-textbook mood.
> **No words, no letters, no numbers anywhere in the image.**

---

## IMG L5-01 — Title hero ★ core

- **File:** `assets/l5-img-01-hero.png` · **Slide 1** (right panel) · **Aspect 4:5 portrait**, ≥1100 px wide
- **Prompt:** A craftsman's workbench in warm lamplight. On one side, a neat stack of paper
  contracts, each closed with a red-amber wax seal. On the wall above, hand tools hung in
  precise silhouette order, smallest to largest. In the center, one document lies open under
  a round magnifier on a brass arm, mid-inspection. Violet shadows, teal blotter, quiet
  concentration — a workshop where nothing ships unchecked.

## IMG L5-02 — The reveal ★ core

- **File:** `assets/l5-img-02-reveal.png` · **Slide 10** (right panel) · **Aspect 4:5 portrait**, ≥1000 px
- **Prompt:** A heavy theater curtain pulled halfway open by a rope — but behind it, instead
  of a stage, stands tidy exposed clockwork: interlocking gears, a hanging weight, and a row
  of five small stamp-arms rising and falling in sequence over a strip of paper, each leaving
  a simple round mark. Amber curtain, teal and slate machinery, one violet gear. The mood is
  friendly demystification, not menace — the magic was a mechanism all along.

## IMG L5-03 — Sealed and shipped ★ core

- **File:** `assets/l5-img-03-sealed.png` · **Slide 13** (bottom banner) · **Aspect 2:1 wide**, ≥1400 px wide
- **Prompt:** The workbench at end of day, lamp dimmed low. A single finished document lies
  centered, bearing one red-amber wax seal and, down its margin, a neat vertical row of small
  teal check-stamps. The magnifier is swung aside; the wall tools all hang back in their
  silhouette order. Calm, resolved, everything in its place.

---

### Generation tips

- Ask for **flat illustration / risograph / screen-print**; reject photorealistic or
  glow-heavy outputs.
- L5-01 and L5-03 are the same workbench, working vs finished — matching lamp, magnifier,
  and tool wall between them is the visual payoff. The check-stamps in L5-03 should read as
  marks, not characters.
- Generate slightly larger than needed; the deck crops with `object-fit: cover`.
- All three are core; the deck has no optional garnish slots.
