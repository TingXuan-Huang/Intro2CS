# Lesson 12 — Instructor Notes
### Visualization with Matplotlib · Intro to CS for non-CS students

This plan is the teaching companion for a future
`notebooks/Lesson12_Visualization_with_Matplotlib.ipynb` and
`lesson12_exercise/`. It assumes the course's pinned retail and FRED data, so
every demonstration can run offline and produce the same result in class.

---

## 1. What this lesson is really for

Students already know how to turn raw data into a trustworthy table. This
lesson teaches them to make one comparison in that table easy to see without
distorting it.

The target sentence, said in their own words, is:

> "I choose the chart from the question: change over ordered time means a line;
> category comparison means bars; two numeric variables mean a scatter plot;
> a distribution's shape means a histogram; and a compact distribution summary
> means a box plot. Then I label the units, inspect the scale, and state only
> what the chart supports."

The through-line is:

```text
question → tidy data → visual mapping → honest labels and scale → saved figure → cautious claim
```

A chart is not decoration and it is not proof. It is an argument made by
mapping data properties to visual properties such as position, length, and
shape. The code may run perfectly while that argument is still misleading.

When time is short, protect chart choice, distributions, and the misleading-
chart audit. Cut styling options before cutting reasoning.

## 2. Learning outcomes

By the end, students should be able to:

1. Choose a line, bar, scatter, histogram, or box plot from the analytical
   question and the types of variables involved.
2. Build a figure with the explicit Matplotlib pattern: create `fig` and `ax`,
   draw on the `Axes`, label it, and save from the `Figure`.
3. Prepare data for a chart by aggregating categories and parsing and sorting
   dates before plotting.
4. Explain how histogram bins, skew, outliers, and axis limits affect what a
   viewer sees.
5. Audit a chart for missing units, an inappropriate baseline, cherry-picked
   ranges, overclaiming, and inaccessible use of color.
6. Write one accurate observation and one limitation for a figure.

Evidence of success is not "the student made a pretty chart." It is that the
student can justify the mapping, reproduce the figure from code, and avoid
claiming more than the data shows.

## 3. Prerequisites and setup

Students should already know:

- pandas selection, derived columns, `groupby`, sorting, and dates from Lesson 2;
- functions and validation from Lesson 5;
- FRED time-series data from Lesson 6; and
- retail aggregates from Lessons 8–9.

Use only local, pinned data:

- `course_data/online_retail_sample.csv` for categorical comparisons and a
  two-variable relationship;
- `lesson6_exercise/fixtures/UNRATE.json` for a monthly time series;
- `lesson6_exercise/fixtures/CPIAUCSL.json` for a second monthly series in the
  subplot demonstration; and
- `lesson6_exercise/fixtures/DGS10.json` for a larger empirical distribution.

Use this explicit unit mapping; the fixtures' top-level `"units": "lin"` field
describes a FRED transformation, not the real-world measurement unit:

- UNRATE: percent;
- DGS10: percent; and
- CPIAUCSL: seasonally adjusted index, 1982–1984 = 100.

Call CPIAUCSL a price index, not "inflation." Inflation would be a rate of
change computed from that index.

Matplotlib is already part of the course setup. The notebook should run top to
bottom without an API key or network request. Save generated images under a
runtime output folder rather than committing them as source data.

## 4. Recommended split into two sessions

Plan for two 85–90 minute meetings, followed by a 75–90 minute exercise or
studio block.

- **Session A (~85 min): Units 1–2.** Anatomy of a figure, the explicit API,
  and choosing a chart from the question.
- **Session B (~90 min): Units 3–5.** pandas plotting, dates, subplots,
  distributions, misleading charts, and reproducible output.
- **Exercise (~75–90 min).** Four retail/FRED questions, four justified
  figures, and short interpretations.

If this must fit one 120-minute meeting, use this compressed schedule:

| Time | Segment |
| --- | --- |
| 0–5 min | Hook: two charts, one dataset |
| 5–25 min | Figure/Axes and the explicit pattern |
| 25–55 min | Chart-choice matrix plus provided code templates for all five chart types |
| 55–80 min | Guided DGS10 histogram and box plot |
| 80–100 min | Audit three misleading charts: truncated bars, shuffled dates, and a causal title |
| 100–115 min | Guided UNRATE exercise figure |
| 115–120 min | Exit ticket |

Cut the pandas wrapper, CPI subplot, optional log scale, and extra misleading-
chart pairs. Assign the other three exercise figures with scaffolded function
signatures and plotting calls.

## 5. Timing reference

| Session | Segment | Time | Protect this idea |
| --- | --- | ---: | --- |
| A | Hook: two charts, one dataset | 5 min | A chart can change the apparent story. |
| A | Unit 1 — Figure, Axes, and explicit code | 25 min | Know which object owns the plot and the saved output. |
| A | Unit 2 — Match the chart to the question | 45 min | The question chooses the visual mapping. |
| A | Exit ticket and discussion | 10 min | Justify a chart without writing code. |
| B | Retrieval warm-up | 10 min | Recall the decision rules from Session A. |
| B | Unit 3 — pandas, dates, and subplots | 30 min | Convenience does not replace correct preparation. |
| B | Unit 4 — Distributions, skew, and outliers | 30 min | A distribution has shape, not just an average. |
| B | Unit 5 — Honest charts and saved evidence | 20 min | Correct code can still communicate a false impression. |

## 6. The chart-selection rule

Keep this table visible throughout both sessions. Ask for the reason before
showing the syntax.

| Question | Good first chart | Data preparation | Main trap |
| --- | --- | --- | --- |
| How did one value change over ordered time? | Line | Parse and sort time; aggregate to a meaningful frequency. | Connecting unsorted dates or unordered categories. |
| Which categories are larger or smaller? | Bar, often sorted horizontal bars | Aggregate to one value per category. | A truncated baseline or too many categories. |
| Do two numeric variables vary together? | Scatter | Keep paired measurements on the same row. | Claiming correlation or causation from a visual pattern. |
| What shape does one numeric variable have? | Histogram | Remove or explain missing values; choose bins deliberately. | Treating one bin choice as the only true picture. |
| How do distributions compare compactly? | Box plot | Keep a numeric value and optional grouping category. | Calling every point beyond a whisker an error. |

Subplots are a layout choice, not a sixth analytical question. Use them when
related views deserve separate scales or when a histogram and box plot explain
the same distribution in complementary ways.

## 7. Teaching notes per unit

### Unit 1 — Figure, Axes, and the explicit API · ~25 min

Open with an unlabeled line. Ask: "What can we safely say from this?" Students
should notice that they do not know the variable, unit, date range, or source.
The line has geometry but not meaning.

Draw the anatomy on the board:

- **Figure:** the whole canvas and the object that gets saved.
- **Axes:** one plotting region; it owns the plotted data, title, labels, and
  coordinate system.
- **Axis:** an individual x- or y-scale inside an Axes.
- **Artist:** a visible item such as a line, bar, label, or legend. Name this
  briefly; students do not need the class hierarchy.

Use one pattern for the entire lesson:

```python
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(dates, values)
ax.set(
    title="U.S. unemployment rate",
    xlabel="Month",
    ylabel="Unemployment rate (%)",
)
fig.savefig(output_path, dpi=150)
```

Show `plt.plot(...)` once so students can read examples found elsewhere, but
teach the explicit `fig, ax` interface as the default. It makes multiple plots,
reuse, testing, and saving easier to reason about.

**Live prediction.** Create two figures and then use an implicit `plt.title` or
`plt.savefig`. Ask which figure changes or gets saved. Repeat with explicit
`ax.set_title` and `fig.savefig`, where ownership is visible in the code.

> **Unit 1 takeaway:** create the Figure and Axes explicitly, draw and label on
> that Axes, then save the Figure.

### Unit 2 — Match the chart to the question · ~45 min

Do not present five plotting methods as an API tour. Present five questions.
Before each code cell, have students vote on a chart and give a one-sentence
reason.

Use this sequence:

1. **Line — change through ordered time.** Plot a tiny five-month sequence,
   then plot the pinned UNRATE observations. Deliberately shuffle the dates
   first so students see the zigzag created by connecting rows in the wrong
   order.
2. **Bar — compare categories.** Compute represented retail revenue as
   `Quantity * UnitPrice`, group by customer, sort it, and use horizontal bars.
   Load `source_customer_id` as pandas `string` (or convert it before plotting):
   the IDs identify categories and are not measured quantities. Say
   "represented revenue in this extract," because the file contains six
   retained lines per customer rather than full customer histories.
3. **Scatter — compare paired numeric measurements.** Plot unit price against
   quantity for each retail line. Ask what a point represents and what the plot
   cannot establish. A visible relationship is not evidence that one variable
   caused the other.
4. **Histogram — inspect a distribution.** Preview the question and method in
   no more than three minutes; investigate DGS10 and bins in Unit 4.
5. **Box plot — summarize a distribution.** Preview its compact summary beside
   the histogram; teach its parts in Unit 4.

Include one intentionally wrong chart: represented revenue by customer
connected by a line.
Ask what the connecting segments falsely suggest. Customer ID order is not a
continuous path.

**Pair check.** Give four new questions without code. Pairs choose the chart and
name the x- and y-variables. Require a reason tied to ordering, categories,
paired measurements, or distributions.

> **Unit 2 takeaway:** chart type follows the comparison the question asks the
> viewer to make.

### Session B warm-up · ~10 min

Ask from memory before revealing answers:

1. What is the difference between a Figure and an Axes?
2. Why is a line suitable for monthly unemployment but not customer IDs?
3. What does one point in a scatter plot represent?
4. Why should a bar chart usually start its value axis at zero?
5. Which chart shows distribution shape, and which gives a compact summary?

Expected answers: the Figure is the whole saved canvas and an Axes is one
plotting region; time is ordered while customer IDs are categories; a scatter
point is one paired observation; bar length is judged from a common baseline;
a histogram shows shape while a box plot summarizes median, spread, and points
beyond the whiskers.

### Unit 3 — pandas plotting, dates, and subplots · ~30 min

Connect pandas plotting to the same Matplotlib model:

```python
fig, ax = plt.subplots(layout="constrained")
monthly.plot(x="month", y="value", ax=ax, legend=False)
```

`DataFrame.plot` is a convenience wrapper. Passing `ax=ax` keeps ownership
explicit, and the returned object is still a Matplotlib Axes.

Make the preparation contract visible:

1. parse the date column;
2. coerce the measurement to numeric and handle missing readings honestly;
3. sort by date;
4. check the expected frequency, missing dates, and duplicate dates;
5. reindex monthly series to a complete monthly calendar so an absent month is
   represented by `NaN` rather than silently connected; and
6. only then draw the line.

Use the shuffled-date example as the planted bug. The chart renders without an
exception, but its path is false because row order was mistaken for time order.
The monthly fixtures also omit October 2025. Sorting cannot reveal an absent
row: reindex both monthly series and let the line break at the missing month, or
annotate the gap. Do not invent an interpolated value in this lesson.

For subplots, place CPI and unemployment in separate panels with a shared time
axis. Label CPI as an index (1982–1984 = 100) and unemployment as percent. A
second useful layout places a histogram above a box plot. Prefer separate panels
over a dual y-axis when variables have different units; dual axes can make
unrelated series look tightly connected through arbitrary scaling.

> **Unit 3 takeaway:** pandas shortens the plotting call, but the student still
> owns date order, missing values, scale, and meaning.

### Unit 4 — Distributions, skew, and outliers · ~30 min

This unit is the bridge into Lesson 13. An average compresses a variable into
one number; a distribution shows which values are common, rare, spread out, or
asymmetric.

Use the 1,439 raw daily DGS10 observations rather than the ten retail customers.
Do not call Lesson 6's `tidy_monthly()` here: averaging to months would change
the distribution being studied. Parse the raw fixture with a supplied,
self-contained reference loader, convert its 60 `"."` readings to missing
values, and use the remaining daily observations. This is large enough for a
histogram to reveal a shape.

1. Draw the same values with too few, reasonable, and too many bins. Ask which
   features survive all three views.
2. Add a box plot beneath the histogram. Identify the median, middle 50%,
   whiskers, and points beyond the default whisker rule.
3. State explicitly that a point beyond a whisker is a candidate to investigate,
   not permission to delete it.
4. If showing a log scale, make it optional. Explain that it changes distances,
   requires clear labeling, and needs deliberate handling of zero or negative
   values.

Ask students to write an observation in the form "In this pinned period..." so
they do not turn one historical window into a timeless claim.

> **Unit 4 takeaway:** bin choices and summaries change the view, so inspect a
> distribution more than one way and describe it cautiously.

### Unit 5 — Honest charts and reproducible output · ~20 min

Show misleading and repaired versions side by side. In the 20-minute live
segment, prioritize the first, third, and sixth pairs; leave the others as
short notebook checks or exercise review:

- a bar chart with a truncated value axis versus one starting at zero;
- a full time range versus a cherry-picked interval;
- ordered dates versus shuffled dates;
- one convenient histogram binning versus two reasonable alternatives;
- two differently scaled lines on a dual axis versus separate panels; and
- a causal title versus a descriptive title for the same scatter plot.

Teach the baseline nuance. Bars encode magnitude through length, so the value
axis normally needs zero. A line chart does not always need a zero baseline; a
narrower range can be useful when the title, units, limits, and wider context
are clear.

End with the pre-save audit:

- Does this chart answer the stated question?
- Did I inspect the table being plotted?
- Are the title, labels, units, and time range clear?
- Is the ordering correct and the scale honest?
- Does color carry meaning, and is that meaning also available through labels,
  markers, or line styles?
- Is the claim descriptive rather than causal or universal?
- Can the figure be regenerated from a clean run?

Use readable text and restrained color. Avoid relying on a red/green distinction
alone. Put a short Markdown description beside every notebook or submitted
figure so a reader who cannot see the image still gets the chart type,
variables, period, and main visible pattern. Use markers, line styles, direct
labels, or text in addition to color when groups must be distinguished.

> **Unit 5 takeaway:** a correct plotting call is only the start; an honest
> figure makes its comparison, units, scale, and limits visible.

## 8. Formative assessment during class

Use three low-friction checks:

1. **Chart-choice vote.** Show a question and variable types; students hold up
   line, bar, scatter, histogram, or box before seeing code.
2. **Spot the problem.** Show a chart that renders correctly but has shuffled
   dates, missing units, or a truncated bar baseline.
3. **Exit ticket.** Students receive one unfamiliar question and write: chart
   choice, x-variable, y-variable, one required preparation step, and one claim
   the chart cannot support.

The exit ticket is the best signal of understanding because it separates
reasoning from syntax recall.

## 9. Exercise design — four questions, four figures

Allow 75–90 minutes and provide self-contained reference data loaders,
output-directory setup, function docstrings, and a failing checker. Do not make
Lesson 12 depend on a student's unfinished Lesson 6 `fred_client.py`. The
exercise should assess visual reasoning and plotting, not make beginners
rediscover JSON parsing or file-path plumbing.

Use a small `plots.py` module plus a supplied `REFLECTION.md` template. The
starter module should define these contracts:

```python
plot_unemployment(unrate, output_dir)          # returns (fig, ax)
plot_customer_revenue(retail, output_dir)      # returns (fig, ax)
plot_price_vs_quantity(retail, output_dir)     # returns (fig, ax)
plot_yield_distribution(dgs10, output_dir)     # returns (fig, axes)
```

Each function receives an already loaded DataFrame, returns the Figure and its
Axes object or sequence, saves one PNG, and makes no network call.

Give students the questions first and ask them to commit to a chart choice. The
view column below is the instructor key; reveal it only after that choice.

| Student question | Instructor key | Core preparation | Interpretation prompt |
| --- | --- | --- | --- |
| How did U.S. unemployment change over the pinned period? | Line | Parse and sort UNRATE dates; numeric values. | Name one visible change and the exact period covered. |
| Which customer has the largest represented revenue in this 60-line extract? | Sorted horizontal bar | Compute line revenue; group by customer; treat IDs as strings. | Compare the categories and state that this is not a full customer history. |
| Does the sample suggest a relationship between unit price and quantity purchased? | Scatter | Keep paired numeric rows and inspect unusual points. | Describe the pattern and state that it does not establish causation. |
| What is the distribution of daily 10-year Treasury yields in the pinned period? | Histogram plus box plot in one figure | Coerce DGS10 values; drop documented missing readings; use 20 bins for the final histogram. | Describe center/spread/skew cautiously and identify a limitation. |

Make the data contract explicit in the student README:

- Use all 60 rows of the pinned retail sample as supplied. It was selected to
  have positive quantities and prices; do not silently remove, deduplicate, or
  trim unusual rows.
- Read `source_customer_id` with `dtype={"source_customer_id": "string"}` (or
  convert it immediately). Revenue is `Quantity * UnitPrice`. Plot all ten IDs
  in descending represented-revenue order. Label retail prices and revenue in
  pounds (`£` or `GBP`).
- The scatter plot includes every supplied retail row. Unusual points stay in
  the figure; students may annotate them but may not delete them without a
  stated data-quality reason.
- The supplied FRED loader returns the raw `date` and `value` observations; it
  does not call `tidy_monthly()`. It converts `"."` to a missing value, coerces
  the rest to numeric, parses dates, and sorts ascending. For DGS10, drop the 60
  documented `"."` readings and retain daily frequency. For UNRATE, reindex to
  a complete monthly calendar and leave the absent October 2025 value as `NaN`
  so the line breaks rather than bridging the gap.
- UNRATE and DGS10 are percentages. CPIAUCSL, used only in the lesson subplot,
  is a seasonally adjusted index (1982–1984 = 100); the fixture's `"lin"` code
  is not a display unit.
- Use the full pinned date range. Students report its minimum and maximum date
  in ISO `YYYY-MM-DD` form rather than copying dates from this plan.
- Use 20 equal-width bins for the submitted DGS10 histogram so the checker is
  deterministic. The lesson itself still compares multiple bin choices.

Use these exact saved filenames:

- `unemployment_trend.png`
- `customer_revenue.png`
- `price_vs_quantity.png`
- `treasury_yield_distribution.png`

For each question, the `REFLECTION.md` template should request five labeled
lines: **Chart choice**, **Figure description**, **Observation**,
**Limitation**, and **Period/bin note**. The figure description names the chart
type, variables, period, and main visible pattern so the submission remains
understandable without seeing the PNG. Also include one short supplied-chart
audit: identify the problem in a truncated-baseline bar chart, explain the
impression it creates, and propose a repair.

Require every figure to include:

- a title that states what is shown rather than what allegedly caused it;
- axis labels with units where applicable;
- correct ordering and a defensible scale; and
- the exact deterministic filename above.

Use chart-specific label expectations rather than one generic rule:

- UNRATE: x = month; y = unemployment rate (%).
- Customer bars: category axis = customer ID; value axis = represented revenue
  (£/GBP).
- Scatter: x = unit price (£/GBP); y = quantity (items).
- DGS10 histogram: x = 10-year Treasury yield (%); y = observation count. The
  horizontal box plot needs a labeled yield axis but no invented unit for its
  empty category axis.

### Checker design

Do not compare image pixels. That would punish harmless styling differences and
reward charts that happen to resemble a reference.

Auto-check:

- prepared values and aggregation against pinned answers;
- returned Matplotlib Figure/Axes objects;
- chart-specific structure: a gapped date line; ten ordered category bars; one
  scatter collection with all 60 pairs; and a 20-bin histogram plus a box-plot
  summary on two Axes;
- sorted time coordinates and an explicit October 2025 gap;
- non-empty titles and the chart-specific labels above;
- expected axes count; and
- existence of the saved file.

Bars and histograms both create rectangle patches, while lines and box plots can
both create `Line2D` artists. Test the function-specific structure and plotted
coordinates instead of relying on a generic artist class. Accept direct
Matplotlib calls, pandas wrappers, and harmless style choices. Accept documented
unit variants such as `£`, `GBP`, or `pounds`; do not require one exact label
string. Keep semantic chart choice in the human review.

Human-review the chart-choice reason, interpretation, limitation, scale
honesty, readability, and supplied misleading-chart critique.

### Suggested rubric

| Criterion | Weight |
| --- | ---: |
| Data preparation and numeric correctness | 25% |
| Chart choice and visual mapping | 20% |
| Labels, units, scale, and readability | 20% |
| Evidence-based interpretation and limitation | 20% |
| Reproducibility and saved output | 10% |
| Misleading-chart audit | 5% |

For consistent human grading, full credit for labels/scale means all
chart-specific labels are present, the customer bar scale starts at zero, and
text is legible without relying on color. Full credit for interpretation means
the observation points to a visible feature and the limitation names the
specific sample or time-window constraint; generic phrases such as "more data
is needed" earn only partial credit.

## 10. Misconceptions to pre-empt

| Misconception | Better mental model |
| --- | --- |
| "The chart type is an aesthetic preference." | It determines which comparison the viewer can make accurately. |
| "A line chart works for any sequence." | A line implies meaningful order and continuity between adjacent positions. |
| "A scatter plot proves one variable affects the other." | It shows paired observations and possible association, not causation. |
| "The histogram is the distribution." | It is one binned view; different reasonable bins reveal or hide features. |
| "A box-plot outlier is bad data." | It is a point beyond a summary rule and needs investigation, not automatic deletion. |
| "Every axis must start at zero." | Bars normally should; line-chart limits depend on the question and must be transparent. |
| "More color and decoration add information." | Every visual element should carry meaning or improve legibility. |
| "Matplotlib made it, so it is objective." | Software draws exactly the mapping and scale the author chose. |
| "`.plot()` removes the need to prepare data." | The library cannot decide whether dates, missing values, aggregation, or units are meaningful. |

## 11. Scope — name briefly, do not teach

Do not turn this into a tour of the visualization ecosystem. Keep these out of
the core lesson:

- Seaborn, Plotly, Altair, dashboards, and interactive widgets;
- animation, 3D charts, geographic maps, and image plots;
- advanced typography, custom themes, and publication layout;
- formal color theory and full accessibility standards;
- statistical smoothing, confidence bands, and regression lines; and
- exhaustive Matplotlib `Artist`, backend, or style configuration details.

These are useful later. Here the goal is a correct, honest, reproducible static
figure from familiar data.

## 12. Instructor preparation checklist

- Run the notebook from a clean kernel with networking disabled.
- Verify the self-contained FRED loader from a clean checkout. Confirm that the
  monthly calendar exposes the October 2025 gap and that DGS10 remains daily.
- Pre-generate the misleading/honest chart pairs so discussion does not depend
  on live styling work.
- Check that saved figures are written to a runtime folder and can be recreated.
- Keep the small chart-selection table visible during the exercise.
- Prepare one alternate question for the exit ticket so students cannot copy a
  demonstration answer.
- Check projected colors in grayscale or with a color-vision simulator; do not
  rely on color alone. Ensure every submitted figure has an adjacent Markdown
  description.

## 13. Where this lesson leads

Lesson 13 turns the histogram's empirical distribution into probability,
expectation, variance, and Monte Carlo simulation. Lesson 14 adds uncertainty
intervals and evidence from samples. Preserve this boundary:

> A visualization helps us notice and communicate a pattern. Probability and
> inference tell us how uncertain that pattern is and what conclusions the data
> can support.

## 14. Resources

- [Matplotlib — application interfaces](https://matplotlib.org/stable/users/explain/figure/api_interfaces.html)
- [Matplotlib — Introduction to Axes](https://matplotlib.org/stable/users/explain/axes/axes_intro.html)
- [Matplotlib — line plot and saving a figure](https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html)
- [pandas — `DataFrame.plot`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.html)

### The lesson, one sentence

> A visualization maps data properties to visual properties: choose that
> mapping from the question, label it honestly, and preserve it as reproducible
> code.
