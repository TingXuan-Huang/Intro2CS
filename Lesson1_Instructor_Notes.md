# Lesson 1 — Instructor Notes
### Data Types and Data Structures · Intro to CS for non-CS students

This companion goes with two notebooks, one intuition guide, and one helper file:

- `notebooks/Lesson1_Data_Types_and_Structures.ipynb` — the runnable teaching demo (present top-to-bottom).
- `Lesson1_Exercises.ipynb` — student exercises (concept-first).
- `note.md` — intuition, importance, and real-world applications for each property.
- `test_lesson1.py` — the auto-checker the exercise notebook imports. Keep it in the same folder.

---

## 1. What this lesson is really for

Students should leave able to *reason* about representation, not recite methods. The target
sentence, said in their own words, is:

> "This is one customer, so a **dictionary**. Many customers, so a **list of dictionaries**
> or a **DataFrame**. IDs must be unique, so a **set**. Fast lookup by ID, so a **dictionary**."

Everything in the notebook builds toward that reasoning. When you're short on time, protect
the 🧭 "why" callouts and Unit 8 Task 6 — cut examples, not reasoning.

## 2. Recommended split into two sessions

The full plan is 4–5 hours. That is too long for one sitting with this audience. Split at the
Unit 4/5 boundary:

- **Session A (~2 hrs): Units 1–4.** Values/variables/types/structures, scalars, the four
  collections, mutability. This is the conceptual core and stands on its own.
- **Session B (~2 hrs): Units 5–8.** Stacks/queues, arrays/DataFrames, CSV/JSON, and the
  integrated exercise as the payoff that shows where the core leads.

If you must do one session, present Units 1–3 and Unit 8 fully and treat Units 5–7 as a
guided skim.

## 3. Timing (single-session reference)

| Unit | Topic | Time | Notes |
|------|-------|------|-------|
| 1 | Values, variables, types, structures | 25 min | Anchor on the "one vs. 1,000 customers" discussion. |
| 2 | Scalar types | 35 min | Spend the time on `None` vs `0`/`""`/`False` and the falsy trap. |
| 3 | List / tuple / set / dict | 70 min | The heart of the lesson. Don't over-invest in tuples. |
| 4 | Mutability & copying | 30 min | Run the predict-then-reveal alias cell live. |
| 5 | Stacks & queues | 30 min | Concept only; keep it brisk. |
| 6 | Records, arrays, DataFrames | 50 min | Emphasize *why* each structure exists, not its API. |
| 7 | CSV & JSON | 25 min | The `"00123"` → `123` example lands well. |
| 8 | Integrated exercise | 45 min | Task 6 (explain the choices) is the assessment that matters. |

## 4. Teaching notes per unit

**Unit 1.** Draw the four-word frame on the board: *value → variable → type → structure*.
Ask the "one vs. 1,000 customers" question before showing code; let them propose before you
reveal the list-of-dicts.

**Unit 2.** Two things reliably confuse beginners and are worth extra time: (a) *digits ≠
number* — ZIP codes and IDs are strings; (b) the **falsy trap** — `if revenue:` skips a real
`0`. The notebook demonstrates both; run them live and let the surprising output land.
`0.1 + 0.2` always gets a reaction — use it, but don't rabbit-hole into IEEE 754.

**Unit 3.** Teach by the *operation*, not the definition. Keep repeating the four-line decision
rule: order → list, fixed group → tuple, uniqueness → set, lookup → dict. The set operations
(`&`, `|`, `-`) map cleanly to "reached by both / either / only email," which non-CS students
find intuitive. The "why can't a list be a dict key" cell ties immutability back to Unit 4 —
optional, but it's a nice thread to pull.

**Unit 4.** This is where the memorable bug lives. Run the aliasing cell and ask for a
prediction *before* revealing `200`. The one sentence to leave them with: *assignment gives a
second name, not a copy.*

**Unit 5.** Concept only. Undo = stack, service line = queue. Mention that `deque` is used for
queues because popping the front of a list is slow, then move on.

**Unit 6.** The payoff unit. The contrast `[1,2,3]*2` (list repeat) vs `np.array([1,2,3])*2`
(elementwise) is the clearest way to show why a numeric structure exists. Then use the real
Iris measurements to revisit the full checklist: 2D shape, label/position access, homogeneous
numeric columns, vectorized operations, and nominal species labels.

**Unit 7.** Connect each file format to an in-memory shape. CSV represents a rectangle but
guesses types; JSON represents nested lists/dictionaries; NPY keeps array shape and dtype;
Parquet keeps typed columns; databases add schemas, unique constraints, and indexes.

**Unit 8.** Let students attempt Tasks 1–5 in pairs, then discuss Task 6 as a whole group.
Task 6 is the actual assessment of understanding; budget real time for it.

## 5. Misconceptions to pre-empt (call these out explicitly)

- "A variable *contains* the value." Better: a variable is a *name* for an object. This matters
  the moment you hit mutable lists/dicts.
- "Anything with digits should be numeric." IDs, phone numbers, ZIP codes are strings.
- "Dicts and sets are unordered." Modern dicts preserve *insertion* order, but their purpose is
  key lookup, not positional access. Sets are genuinely not positional.
- "A tuple is a list with parentheses." The real difference is immutability and intent.
- "A DataFrame is just a big list." It adds labeled columns, types, alignment, missing-value
  handling, and vectorized ops.
- "Advanced structures are always better." The best structure is the simplest one that supports
  the needed operation clearly.

## 6. Scope — name briefly, do not teach

Linked lists, graphs, hashing internals, memory allocation, object headers, advanced NumPy
broadcasting, sparse tensors, custom containers, and formal complexity analysis. Trees and
hash maps receive only a small mental-model introduction. These deeper topics distract from
the goal: representing practical data correctly.

## 7. How the assessment is designed (and why)

For a Lesson 1 whose stated goal is reasoning over syntax, a full coding autograder would test
the wrong skill and add setup friction for non-CS students. The exercises are therefore a
**hybrid**:

- **Part A — auto-checked quick checks.** `test_lesson1.py` verifies ~15 *unambiguous*
  conceptual answers (which type for a ZIP code, LIFO vs FIFO, predict-the-alias-output, etc.).
  Students get instant ✅/❌ with a one-line explanation and a running `score()`. This gives
  self-learners fast feedback without heavyweight tooling.
- **Part B — open-ended reflection.** Six "why did you choose this representation?" prompts with
  no autograder. These mirror Unit 8's Task 6 and are the real measure of understanding; grade
  them by discussion or short written response.
- **Part C — optional stretch code.** Three tiny tasks (build a set, filter by boolean, build a
  lookup dict) for students who want to type a little. Not required.

**Running the checker.** The exercise notebook does `import test_lesson1 as t`, then
`t.check("q1", "str")`. Keep `test_lesson1.py` beside the notebook. You can sanity-check the
answer key any time with `python test_lesson1.py` (it self-tests that every key answer passes).

**Grading Part B.** Look for *justification tied to an operation*, not vocabulary. A good B1
answer says a dict is chosen because fields are fetched by name and a list because records are
ordered and may repeat — and notes what breaks if swapped. Award credit for correct reasoning
even if the wording differs.

## 8. If you want to extend later

Natural Lesson 2 hooks already seeded here: the `None → NaN` flow (data cleaning), the CSV
type-loss example (file I/O), and the `scalar → list → array → tensor` chain (numerical
computing / ML).

## 9. Resources

Primary for students: Python Tutorial – Data Structures; NumPy Absolute Basics; 10 Minutes to
pandas; pandas Table-Oriented Data. Instructor reference: Python built-in types; Python classes
and aliasing; `collections.deque`; Java primitive types (for the static-vs-dynamic contrast).
