# Lesson 3 Assignment — Algorithms and Big-O

Two parts, in this order:

- **Part 1 — Seven coding problems**, solved on [leetcode.com](https://leetcode.com). Each one is a daily analyst task wearing an interview costume, and each maps to a unit of Lesson 3.
- **Part 2 — Thirteen Big-O questions**, answered in writing or out loud. Answers are hidden under each question — genuinely try first.

**The grading standard for everything here** (same as class): the plain-English sentence, not the label. A correct O(n) with no reason is worth less than a wrong guess with good reasoning about what the code examines and how often.

**After every solved problem, run the 30-second spoken loop:**

> *the algorithm in plain English → its Big-O → why the naive version is worse.*

That loop — not the green checkmark — is the actual interview skill.

---

## Part 1 — Coding problems

| # | Problem | Difficulty | Lesson connection | Analyst translation |
| --- | --- | --- | --- | --- |
| 1 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) (LC 121) | Easy | Unit 1 — scan with carried state | best entry/exit point in a time series |
| 2 | [Two Sum](https://leetcode.com/problems/two-sum/) (LC 1) | Easy | Unit 3 — dict lookup beats scanning | trade memory for speed |
| 3 | [High Five](https://leetcode.com/problems/high-five/) (LC 1086) ⭐ | Easy | Unit 4 — groupby-aggregate by hand | `groupby().mean()` without pandas |
| 4 | [Moving Average from Data Stream](https://leetcode.com/problems/moving-average-from-data-stream/) (LC 346) | Easy | Unit 1 + Lesson 1's queue | rolling metrics |
| 5 | [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) (LC 347) | Medium | Unit 4 Counter + Unit 3 sorting | top 10 products by volume |
| 6 | [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) (LC 3) ⚠️ | Medium | stretch — sliding window (new technique) | longest streak of distinct events |
| 7 | [Merge Intervals](https://leetcode.com/problems/merge-intervals/) (LC 56) | Medium | Unit 3 — sort first, then one scan | sessionizing activity windows |

Solve them in this order — it follows the lesson, and the difficulty ramps.

---

### 1. Best Time to Buy and Sell Stock — [LC 121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

`prices[i]` is a stock's price on day `i`. Buy on one day, sell on a **later** day; return the maximum profit (or `0` if no profitable trade exists).

**Why this problem:** it is literally "find the best entry/exit point in a metric" — Unit 1's linear scan, carrying **two** pieces of state: the *lowest price seen so far* and the *best profit seen so far*.

**Before coding, answer out loud:** why can't you just do `max(prices) - min(prices)`? (What if the maximum comes *before* the minimum?)

<details><summary><b>Target complexity (check after solving)</b></summary>

O(n) — one pass, two carried values. The naive version checks every buy/sell pair: O(n²), dead on a year of tick data.
</details>

### 2. Two Sum — [LC 1](https://leetcode.com/problems/two-sum/)

Return the **indices** of the two entries that add up to `target` (exactly one solution exists).

**Why this problem:** the single most reused trick in the trade — **trade memory for speed with a dictionary** (Unit 3, and Unit 4's matching in miniature).

**Do it twice.** First the nested-loop O(n²) way — feel the Unit 2 shape. Then the real version: one scan carrying `{value_seen: its_index}`, asking at each number: *have I already seen `target - number`?*

<details><summary><b>Target complexity</b></summary>

O(n) — one scan, each dict ask/insert O(1) average. The price paid: O(n) extra memory for the dict. Say that trade out loud — it's the point of the problem.
</details>

### 3. High Five — [LC 1086](https://leetcode.com/problems/high-five/) ⭐ the centerpiece

Given `(student_id, score)` pairs, return each student's **average of their top 5 scores** (integer division).

> **Note:** LC 1086 requires LeetCode Premium. No Premium? Solve it in a plain Python file — the spec above is complete. Example:
> `[[1,91],[1,92],[2,93],[2,97],[1,60],[2,77],[1,65],[2,100],[1,87],[1,100],[2,76]]` → `{1: 87, 2: 88}`
> (Student 1's top five: 100, 92, 91, 87, 65 → 435 // 5 = 87.)

**Why this problem:** this is `df.groupby("student").apply(top5mean)` in pure Python — **the pandas mental model without pandas** — and a frequent DS-interview ask. If you can narrate this one, Unit 4 stuck. If you do only one problem on this sheet, do this one.

**The plan is two lesson moves glued together:** Unit 4 aggregation (one scan building `{student_id: [scores...]}`), then Unit 3 sorting (per student: sort descending, slice five, average).

<details><summary><b>Target complexity</b></summary>

O(n log n) with a per-student sort, O(n) if you keep only a fixed-size top-5 while scanning. Either answer is fine — *the reasoning is the answer.*
</details>

### 4. Moving Average from Data Stream — [LC 346](https://leetcode.com/problems/moving-average-from-data-stream/)

A class that receives values one at a time; after each, return the average of the last `size` values.

**Why this problem:** rolling metrics are daily analyst work (7-day active users, 30-day revenue); the interview version tests whether you can *maintain a window*. The right container is an old friend — **Lesson 1's queue** (`collections.deque`). Recall why a plain list is wrong here: `list.pop(0)` shifts every remaining element.

**Stretch:** carry a running sum so `next()` never re-sums the window.

<details><summary><b>Target complexity</b></summary>

O(1) **per call** with the running-sum trick (append + at most one popleft + one update). Note the unit of analysis: per call, not per stream. Re-summing the window each call would be O(window).
</details>

### 5. Top K Frequent Elements — [LC 347](https://leetcode.com/problems/top-k-frequent-elements/)

Return the `k` most frequent values, any order.

**Why this problem:** "top 10 products by order volume" as an algorithm question — Lesson 2's `value_counts().head(10)`, rebuilt by hand.

**The plan:** Unit 4's frequency count (`Counter`, or your own dict) + Unit 3's sort-by-a-field (`key=`) + a slice.

**The conversation interviewers want afterwards** — be ready to say it: sorting all counts is O(n log n), but you only need the top k; a *heap* keeps just k candidates for O(n log k), which matters when n is huge and k is 10. You don't need to implement the heap — you need to be able to have this conversation.

<details><summary><b>Target complexity</b></summary>

O(n log n) for count-then-sort (fully acceptable); O(n log k) with a heap. Both defensible.
</details>

### 6. Longest Substring Without Repeating Characters — [LC 3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) ⚠️ stretch

Length of the longest stretch of **consecutive** characters with no repeats. (`"pwwkew"` → 3, from `"wke"` — substring, not subsequence.)

**Why this problem:** the single most common medium in DS/DA coding rounds. Think "longest streak of distinct daily events."

**⚠️ Technique preview — the sliding window** (one move the lesson didn't teach):

1. Two positions, `left` and `right`, mark a window; both only ever move forward.
2. Extend `right` one character at a time, keeping the window's characters in a **set** (Lesson 1: uniqueness + O(1) membership).
3. On a duplicate, shrink from `left` (removing from the set) until the duplicate is gone.
4. Track the largest window ever seen — Unit 1's best-so-far.

If this takes real struggle, that is normal — it's the hardest idea on the sheet. Trace `"pwwkew"` on paper before coding, and test your code on `"dvdf"` (the classic shrink-too-far trap).

<details><summary><b>Target complexity</b></summary>

O(n) — each character enters the window once and leaves at most once: two passes' worth of *sequential* work, and sequential work **adds**. It is not O(n²) despite two pointers; checking every substring naively would be.
</details>

### 7. Merge Intervals — [LC 56](https://leetcode.com/problems/merge-intervals/)

Merge every group of overlapping `[start, end]` intervals. (`[[1,3],[2,6],[8,10],[15,18]]` → `[[1,6],[8,10],[15,18]]`; touching intervals like `[1,4],[4,5]` merge too.)

**Why this problem:** this is **sessionization** — collapsing overlapping user-activity windows into sessions, a real preprocessing step before retention analysis.

**The plan is pure Unit 3 — organize first, then scan:** sort by start time (`key=`, the preparation trade-off), then one scan carrying the current merged interval: extend its end while the next interval starts at or before it; otherwise close it and start a new one.

**Say out loud before coding:** why does sorting make a single scan sufficient — what goes wrong on unsorted input?

<details><summary><b>Target complexity</b></summary>

O(n log n) — the sort dominates; the merge scan after it is O(n). Sorting turned "compare every interval with every interval" into "compare neighbors."
</details>

---

## Part 2 — Big-O questions

Thirteen questions in four tiers. Write the class **and one plain-English sentence**. Try before opening any answer.

### Tier 1 — the core moves

**Q1. The doubling question.** The dataset doubles. For each class, what happens to the amount of work?
O(1) · O(log n) · O(n) · O(n log n) · O(n²)

<details><summary>Answer</summary>

O(1): unchanged · O(log n): **one more step** · O(n): ×2 · O(n log n): slightly more than ×2 · O(n²): **×4**. This one question is the whole vocabulary — the ×2-vs-×4 fingerprint is how you identify classes from measurements.
</details>

**Q2. Sequential loops.** Two separate `for` loops over the same list, one after the other. What class — and why isn't the answer "O(2n)"?

<details><summary>Answer</summary>

O(n). Sequential loops **add** (n + n = 2n), and Big-O drops the constant because 2n and n have the same growth *shape* — both double when the data doubles. Only the shape survives at scale.
</details>

**Q3. Nested loops.** A loop over all customers *inside* a loop over all customers. What class — and name a real analytics task that accidentally takes this shape.

<details><summary>Answer</summary>

O(n²) — nested loops **multiply**. The classic accident: matching two datasets by scanning one inside the other (Unit 4), or naive duplicate-hunting. 1,000 customers → 1,000,000 comparisons.
</details>

**Q4. The hidden scan (trap).** Only one visible loop:

```python
for order in orders:
    if order["customer_id"] in customer_id_list:   # a plain list
        matched += 1
```

What class? Then: change **one word** to make the whole thing O(n).

<details><summary>Answer</summary>

O(n²). `in` on a **list** is a hidden inner scan — an invisible second loop. Fix: make it `in customer_id_set` — a set membership test is O(1) average (Lesson 1's uniqueness property paying rent). One word, one complexity class.
</details>

**Q5. The fixed loop (trap).** A loop over `prices[:5]` — always the first five rows, however large the file grows. What class?

<details><summary>Answer</summary>

O(1). The work never grows with n. A loop is not automatically O(n) — the question is always *how many items does it touch as the data grows*, not *is there a `for`*.
</details>

### Tier 2 — scaling in numbers

**Q6. Forward estimate.** A report takes 3 seconds on 1 million rows. Estimate its time on 10 million rows if the code is O(n) — and if it is O(n²).

<details><summary>Answer</summary>

O(n): 10× data → 10× work → **~30 seconds**. O(n²): 10× data → 100× work → **~300 seconds, about 5 minutes**. Same code today, very different futures.
</details>

**Q7. Reverse identification.** You measure a script: 10,000 rows → 2 s · 20,000 rows → 8 s · 40,000 rows → 32 s. Which class, and what's the fingerprint?

<details><summary>Answer</summary>

O(n²): each **doubling** of the data **quadruples** the time (2 → 8 → 32). An O(n) script would have gone 2 → 4 → 8. You can diagnose complexity from measurements alone, without reading a line of code.
</details>

### Tier 3 — decisions

**Q8. Lookup structure.** You must perform 10,000 customer lookups by ID against 1 million records. List or dictionary — and roughly what does each cost in total? When would the list be perfectly fine?

<details><summary>Answer</summary>

Dictionary: build once O(n), then O(1) average per lookup → ~1M + 10K operations. List: an O(n) scan *per lookup* → ~10,000 × 1,000,000 = 10¹⁰ comparisons — hours vs. instants. For a **single** lookup, the list is fine: building the dict would cost more than the one scan it saves.
</details>

**Q9. The preparation trade-off.** When is it worth sorting data before searching it — and which database feature is this exact idea?

<details><summary>Answer</summary>

Worth it when there are **many repeated searches**: pay O(n log n) once, then every search is O(log n) instead of O(n). For one search, the preparation costs more than it saves. This is what a database **index** is — a prepared, ordered companion structure; preparation paid once, savings collected on every future query.
</details>

**Q10. When efficiency doesn't matter.** A one-off script, 150 rows, nested loops, finishes in 0.02 seconds. A colleague says to rewrite it with dictionaries. Verdict?

<details><summary>Answer</summary>

Ship it. O(n²) on tiny, fixed-size data is harmless — 150² is 22,500 operations, nothing. The skill Big-O buys you is **recognizing** the shape and knowing what you'd change *if* the data grew; it is not a duty to optimize everything. Knowing when efficiency doesn't matter is part of the interview answer too.
</details>

### Tier 4 — transfer and traps

**Q11. pandas and the constant.** Your hand-written Python loop and `df["amount"].sum()` are both O(n). Why is pandas ~100× faster anyway — and why doesn't Big-O see the difference?

<details><summary>Answer</summary>

pandas runs the scan in compiled code over a homogeneous column (Lesson 1's homogeneity property) — a far smaller **constant** per row. Big-O deliberately ignores constants because it keeps only the growth shape: both versions double when the data doubles. Same class, very different car on the same road.
</details>

**Q12. The spoken loop (recurring).** Pick any one of the seven problems above and deliver, out loud, in under 30 seconds: *the algorithm in plain English → its Big-O → why the naive version is worse.* Repeat with a different problem each study session until all seven are effortless.

<details><summary>Example of the standard (LC 121)</summary>

"One scan over the prices, carrying the cheapest buy seen so far and the best profit seen so far — O(n). The naive version checks every buy/sell pair, which is O(n²) and dies on a year of tick data."
</details>

**Q13. Fix the statement.** Each of these is subtly wrong. Correct each in one sentence:

- (a) "`max()` is free — it's built in."
- (b) "O(n) means it takes n seconds."
- (c) "Binary search is faster, so just point it at the list."

<details><summary>Answer</summary>

(a) Built-ins hide the procedure, not the price — `max()` still runs an O(n) scan, just in compiled code. (b) Big-O is the **shape of growth**, not a stopwatch — hardware and constants set the seconds. (c) Binary search is only *legal* on **sorted** data; on an unsorted list it discards halves that may contain the target and answers wrong with full confidence.
</details>

---

## Suggested pacing

- **Session warm-up:** Q1–Q5 (five minutes, verbal).
- **After each LeetCode solve:** the 30-second spoken loop (Q12), plus one question from Tiers 2–3.
- **Before Lesson 4:** Q13 as the exit check — if all three statements get fixed cleanly, Big-O stuck.
