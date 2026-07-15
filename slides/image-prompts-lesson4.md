# Image prompts — Lesson 4 slide deck (Algorithms & Big-O)

Same workflow as Lesson 1: generate each image, save it as a **PNG with the exact filename**
into `slides/assets/`, reload `Lesson4_Algorithms_and_BigO_Slides.html`, and it replaces its
placeholder automatically. Press **P** in the deck to hide unfilled placeholders.

**Deck motif:** a market of data structures — every promise from Lesson 1 wears a price tag.
Keep every image inside this one market scene-world.

## Shared style block (prepend to every prompt — same as Lesson 1)

> Flat editorial textbook illustration with a screen-print / risograph feel and subtle paper
> grain. Warm cream background (#F7F2E9). Limited palette: warm amber (#C2762B), deep teal
> (#2E7D74), muted violet (#6B5CA5), slate gray (#4A5560), dark ink outlines (#221D15).
> Generous negative space, calm and precise, mid-century science-textbook mood.
> **No words, no letters, no numbers anywhere in the image.**

---

## IMG L4-01 — Title hero ★ core

- **File:** `assets/l4-img-01-hero.png` · **Slide 1** (right panel) · **Aspect 4:5 portrait**, ≥1100 px wide
- **Prompt:** A wooden market stall with a striped awning, displaying clean geometric objects
  for sale: a row of open boxes, a ring of circles, a small cabinet with many tiny drawers,
  a neat stack of cards, a coiled rope. From each object hangs a small blank paper price tag
  on twine — some tags small, one conspicuously large and heavy-looking (hanging from the
  stack of cards). Morning light, amber and teal accents, shopkeeper absent.

## IMG L4-02 — The coat check ★ core

- **File:** `assets/l4-img-02-coatcheck.png` · **Slide 6** (right panel) · **Aspect 1:1**, ≥900 px
- **Prompt:** A theater coat-check counter seen slightly from above. A guest's hand offers a
  small brass token across the counter; behind the attendant stretches a long wall of hundreds
  of identical hooks with coats, receding in perspective. The attendant's arm reaches
  confidently toward exactly one hook, a thin amber line of light connecting token to hook.
  No searching, no hesitation — the line goes straight there. Violet coats, teal wall, warm
  lamplight at the counter.

## IMG L4-03 — Closing time ★ core

- **File:** `assets/l4-img-03-sold.png` · **Slide 13** (bottom banner) · **Aspect 2:1 wide**, ≥1400 px wide
- **Prompt:** The same market stall at closing time, awning half-rolled, warm evening light.
  Most price tags now flipped face-down or removed; on the counter stands a small receipt
  spike stacked with paid paper tags. One lantern lit. Quiet, satisfied end-of-day mood.

---

### Generation tips

- Ask for **flat illustration / risograph / screen-print**; reject photorealistic or
  glow-heavy outputs.
- L4-01 and L4-03 are the same stall, morning and evening — matching architecture and awning
  between them is the visual payoff.
- The in-deck growth chart and cost tables are precise SVG built into the slides — the images
  are scene-setting only, so keep them free of any digits or letterforms.
- Generate slightly larger than needed; the deck crops with `object-fit: cover`.
- All three are core; the deck has no optional garnish slots.
