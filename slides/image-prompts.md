# Image prompts — Lesson 1 slide deck

How this works: generate each image, save it as a **PNG with the exact filename below** into
`slides/assets/`, then reload `Lesson1_Representation_Slides.html`. Each image replaces its
dashed placeholder automatically — no HTML editing. Press **P** in the deck to hide unfilled
placeholders for a clean dry run.

## Shared style block (prepend to every prompt)

> Flat editorial textbook illustration with a screen-print / risograph feel and subtle paper
> grain. Warm cream background (#F7F2E9). Limited palette: warm amber (#C2762B), deep teal
> (#2E7D74), muted violet (#6B5CA5), slate gray (#4A5560), dark ink outlines (#221D15).
> Generous negative space, calm and precise, mid-century science-textbook mood.
> **No words, no letters, no numbers anywhere in the image.**

(IMG 02 is the one exception on numbers — see its note.)

---

## IMG 01 — Title hero ★ core

- **File:** `assets/img-01-hero.png` · **Slide 1** (right panel) · **Aspect 4:5 portrait**, ≥1100 px wide
- **Prompt:** Four translucent glass-like layers stacked vertically with air between them, seen
  in gentle isometric view. Top layer carries tiny everyday objects — a calendar page, a price
  tag, an envelope, a small coin. Second layer carries clean geometric containers — a row of
  open boxes, a ring of circles, a small keyed cabinet. Third layer shows round nodes connected
  by curved threads to little blank name-tags. Bottom layer dissolves into a dense, fine grid of
  tiny slate squares, like a punch card fading into darkness. A single thin thread of warm light
  falls vertically through all four layers, connecting them. Composition weighted low, lots of
  cream space at the top.

## IMG 02 — The vanishing zeros ★ core

- **File:** `assets/img-02-zeros.png` · **Slide 2** (right card) · **Aspect 1:1**, ≥900 px
- **Prompt:** A vintage mechanical letter-sorting machine over a conveyor belt. On the left, a
  paper luggage tag enters the machine carrying a neat row of five small brass rings and shapes.
  On the right, the tag exits with only some shapes remaining — three brass rings are tumbling
  off the edge of the conveyor into a dark rectangular gap below. Slight comic melancholy; the
  falling rings should clearly read as zeros being lost.
- **Note:** if your model handles short text reliably, you may instead put the literal string
  **“00123”** on the entering tag and **“123”** on the exiting tag — retry until the digits are
  exact, otherwise keep the no-text ring version.

## IMG 03 — Three levels strata ★ core

- **File:** `assets/img-03-strata.png` · **Slide 6** (left half) · **Aspect 3:2 landscape**, ≥1200 px wide
- **Prompt:** Clean geological cross-section of the ground, three distinct strata. Surface
  stratum: a tidy desk scene in daylight — a few everyday objects (book, cup, envelope) on a
  teal ground line, warm amber light. Middle stratum: round violet nodes tied by threads to
  small hanging blank name-tags, floating in soft violet-tinted earth. Deepest stratum: a dense,
  regular grid of tiny slate-gray squares, growing darker with depth. Thin roots run from the
  desk objects down through all three strata, connecting surface to depth.

## IMG 04 — Two tags, one crate (optional garnish)

- **File:** `assets/img-04-nametags.png` · **Slide 7** (small corner card) · **Aspect 1:1**, ≥700 px
- **Prompt:** Two leather name tags hanging from strings, both strings clearly converging and
  tied to one single wooden crate. The crate sits centered; the two strings enter from the upper
  left and upper right. Violet and amber accents on the tags, warm cream background, strong
  simple silhouette.

## IMG 05 — Four ways to pack ★ core

- **File:** `assets/img-05-crates.png` · **Slide 8** (wide strip under the title) · **Aspect 4:1 wide strip**, ≥1600 px wide
- **Prompt:** Four wooden shipping crates in a single row, each containing the same small set of
  ceramic objects, packed four different ways. First crate: stuffed with crumpled newspaper,
  contents visibly jumbled and one piece deformed. Second crate: neat labeled-looking
  compartments (blank labels) holding smaller nested boxes. Third crate: a vacuum-formed foam
  mold hugging its contents exactly. Fourth crate: tight columnar honeycomb cells, dense and
  orderly. Even spacing, side view, museum-catalog calm.

## IMG 06 — Lens over bytes (optional garnish)

- **File:** `assets/img-06-lens.png` · **Slide 10** (small corner card) · **Aspect 1:1**, ≥700 px
- **Prompt:** A large brass magnifying lens hovering over an endless field of uniform tiny
  slate-gray squares. Seen through the lens, the same squares resolve into an ordered grid of
  colored cells — neat rows and columns in teal and amber. A small blank paper specification tag
  is clipped to the lens handle with a tiny brass clip.

## IMG 07 — The round trip ★ core

- **File:** `assets/img-07-roundtrip.png` · **Slide 14** (bottom banner) · **Aspect 2:1 wide**, ≥1400 px wide
- **Prompt:** One suitcase shown twice on either side of an open doorway. Left of the door: the
  suitcase being packed, small household items floating in an orderly descending line into it.
  Right of the door: the same suitcase unpacked, the items rising out in a mirrored ascending
  line. At the door's threshold, in shadow, one single small forgotten item rests alone.
  Symmetrical composition, warm light on both sides, melancholy detail at the center.

---

### Generation tips

- Ask for **flat illustration / risograph / screen-print**; reject outputs that come back
  photorealistic or with gradients-and-glow "AI art" lighting — they will clash with the deck.
- The palette hexes matter less than the *relationship*: cream ground, ink lines, and amber /
  teal / violet / slate used sparingly. Regenerate if the model floods the frame with color.
- Generate slightly larger than needed and let the deck crop (`object-fit: cover`).
- Core images: 01, 02, 03, 05, 07. Optional garnish: 04, 06 (the deck reads fine without them —
  press **P** to hide their placeholder cards while presenting).
