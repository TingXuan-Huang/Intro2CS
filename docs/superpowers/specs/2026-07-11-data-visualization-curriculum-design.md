# Data Visualization Curriculum Integration Design

## Status

Approved design for a staged curriculum update.

This pass will revise the course sequence and create instructor-facing lesson
designs. It will not create notebooks, student exercise code, fixtures, or
automated tests.

## Context

The course is a Python-, pandas-, and data-centered introduction to computer
science for non-CS learners. Lessons 1–11 have notebooks and exercises in
various stages of completion. Lessons 12–24 are currently curriculum plans
rather than implemented teaching packages, so they can be renumbered with
limited migration cost.

The repository already contains a detailed
`Lesson12_Instructor_Notes.md` for introductory Matplotlib, chart choice,
distribution plots, and misleading-chart critique. The new visualization
curriculum should extend that work rather than duplicate it.

The learner wants statistical methods to precede formal visualization
instruction so that confidence intervals, residuals, forecasts, and similar
quantities have technical meaning before students learn to present them.
Machine-learning diagnostics and explanation should follow the ML sequence.

## Decisions

1. Use a full curriculum reflow rather than lettered lesson insertions.
2. Move formal visualization instruction to immediately after probability,
   inference, and regression.
3. Replace the current single visualization lesson with three required lessons.
4. Add one required model-diagnostics and explainability lesson after the main
   ML sequence.
5. Teach SHAP in the required ML explanation lesson, with strict scope and
   interpretation cautions.
6. Keep PCA, t-SNE, UMAP, deeper XAI, and specialized visualization optional.
7. Keep the required toolchain Python-first:
   - Matplotlib for explicit static-figure fundamentals.
   - Altair/Vega-Lite for grammar-of-graphics and interaction.
   - SHAP for a small, controlled model-explanation example.
8. Treat Tableau and Power BI as optional job-search translation labs, not as
   required parallel implementations.
9. Preserve the course's offline-first, pinned-data, deterministic-assessment
   design.

## Goals

Students should be able to:

- choose a chart from the analytical task and variable types;
- prepare and validate the data and metric before plotting;
- use perceptually effective and accessible visual encodings;
- build reproducible static and interactive Python visualizations;
- identify misleading scales, denominators, aggregation, and rhetoric;
- communicate a finding, uncertainty, and limitation to a stakeholder;
- diagnose model performance and subgroup failures visually;
- explain model behavior globally and locally without confusing attribution
  with causation; and
- translate core visualization concepts to Tableau or Power BI when preparing
  a portfolio.

## Non-goals for this pass

- Implementing the lesson notebooks.
- Implementing student starter code or answer keys.
- Creating or refreshing datasets and fixtures.
- Adding pytest suites or image-comparison tests.
- Requiring Tableau, Power BI, a cloud account, or network access.
- Teaching every paper or specialized visualization technique in full.

## Revised required sequence

### Phase 1 — Fundamentals

Lessons 1–5 remain unchanged.

### Phase 2 — APIs, Databases, Distributed Data, and LLMs

Lessons 6–11 remain unchanged.

### Phase 3 — Statistical Methods

- Lesson 12 — Probability and Monte Carlo
- Lesson 13 — Inference Through A/B Testing
- Assignment A5 — A/B Test
- Lesson 14 — Linear and Logistic Regression

These lessons may use supplied plots to teach the statistical method. They do
not assess chart construction. Instructors identify what each plot encodes,
state units, and avoid unexplained visual conventions, but formal visual design
begins in Lesson 15.

### Phase 4 — Visualization and Communication

- Lesson 15 — Choosing Visual Representations and Matplotlib Foundations
- Lesson 16 — Building Trustworthy Visualizations
- Lesson 17 — Dashboards, Storytelling, Interaction, and Uncertainty

### Phase 5 — LLM Systems

- Lesson 18 — RAG: Embeddings and Retrieval
- Lesson 19 — LLM Tools and Agents
- Lesson 20 — Cost-Aware Routing

### Phase 6 — Machine Learning

- Lesson 21 — ML Foundations
- Lesson 22 — Evaluation Before Complexity
- Assignment A6 — Churn Model
- Lesson 23 — Neural Networks, Conceptual
- Lesson 24 — Model Diagnostics and Responsible Explanation

### Phase 7 — Statistical Extensions

- Lesson 25 — Time-Series Forecasting
- Lesson 26 — Markov Chains and Bayesian Updating

### Phase 8 — Capstone

- Lesson 27 — Capstone: Economic Question Agent

Assignments A1–A4 retain their current placements. A5 follows Lesson 13, A6
follows Lesson 22, and the capstone becomes Lesson 27.

## Required visualization lesson designs

### Lesson 15 — Choosing Visual Representations and Matplotlib Foundations

#### Purpose

Teach students that a chart is a representation chosen to support a task, not
decoration or automatic proof.

#### Prerequisites

- pandas selection, grouping, sorting, joins, and dates;
- functions, validation, and reproducible file output;
- probability distributions, confidence intervals, and regression concepts;
- familiarity with the pinned retail and FRED datasets.

#### Learning outcomes

Students can:

- classify nominal, ordinal, quantitative, temporal, and geographic variables;
- match comparison, trend, relationship, distribution, and exact-value tasks
  to suitable views;
- explain why shared position and length support more accurate comparisons than
  angle, area, volume, or color intensity;
- use color, size, orientation, position, enclosure, and connection
  deliberately;
- apply proximity, similarity, enclosure, connection, and continuity to chart
  grouping;
- construct and save explicit Matplotlib figures with `fig` and `ax`;
- identify misleading baselines, scales, colors, time windows, denominators,
  and causal titles; and
- justify a chart and state one supported claim and one limitation.

#### Session structure

Use two 75–90 minute sessions plus a 75–90 minute exercise studio.

Session A:

- representation versus decoration;
- variable types and analytical tasks;
- graphical-perception hierarchy;
- preattentive attributes and essential Gestalt principles;
- chart-selection critique.

Session B:

- explicit Matplotlib Figure/Axes model;
- line, sorted bar, scatter, histogram, and box plots;
- labels, units, ordering, bins, baselines, and saved output;
- misleading-versus-repaired chart pairs.

The instructor notes also provide a compressed 120-minute route that protects
chart selection, distributions, and the misleading-chart audit.

#### Assessment design

Students create:

- one comparison chart;
- one distribution chart; and
- one relationship chart.

For each, students state the question, chart rationale, visible observation,
and limitation. They also redesign one weak supplied chart.

Future automated checks inspect transformed values, Matplotlib object types,
expected marks, labels, axes count, and saved files. They do not compare image
pixels. Human review evaluates chart choice, perceptual effectiveness,
readability, and interpretation.

#### Boundary

Lesson 15 introduces enough data preparation to make each plot correct but does
not reteach the complete pandas pipeline, grammar of graphics, dashboards, or
interactive design.

### Lesson 16 — Building Trustworthy Visualizations

#### Purpose

Teach students to transform raw data into a defensible visual claim without
changing the metric's meaning.

#### Learning outcomes

Students can:

- move from a business question through raw data, transformation, metric,
  encoding, validation, and communication;
- filter, sort, group, aggregate, join, reshape, normalize, and handle missing
  values for a stated visual purpose;
- distinguish totals, averages, percentages, rates, and time aggregations;
- identify denominator errors and explain Simpson's paradox conceptually;
- describe a visualization as data, transformation, mark, encoding, scale, and
  facet;
- construct declarative Altair charts;
- choose linear or logarithmic scales, baselines, bins, tick density, sort
  order, and shared scales deliberately;
- select categorical, sequential, and diverging color systems accessibly; and
- replace overloaded views with small multiples.

#### Session structure

Use two 75–90 minute sessions plus a studio.

Session A:

- question-to-chart pipeline;
- metric definitions, aggregation, denominators, reshaping, and validation;
- conceptual Simpson's paradox example;
- grammar of graphics;
- first Altair chart and mapping types.

Session B:

- scales, axes, sorting, time intervals, and bin sensitivity;
- color purpose and accessibility;
- shared scales and small multiples;
- compare one honest and one technically valid but misleading transformation.

#### Assessment design

Students submit one polished analytical chart and one rejected alternative.
The accepted chart includes a takeaway title, units, accessible colors,
justified scale, and a note defining the transformation and denominator. The
rejection note explains why the alternative is weaker.

Automated checks focus on data transformations and declarative chart structure.
Human review evaluates whether the metric, denominator, scale, and visual
hierarchy answer the intended question.

#### Tableau and Power BI supplement

An optional portfolio lab asks students to reproduce the accepted chart in
Tableau or Power BI and write a short translation note:

- which field roles correspond to Altair encodings;
- where aggregation occurs;
- how filters and current state are exposed; and
- what changed because of tool defaults.

No proprietary workbook is required for course completion. A static export and
reflection may be used for portfolio review.

### Lesson 17 — Dashboards, Storytelling, Interaction, and Uncertainty

#### Purpose

Teach students to turn analysis into a focused explanation that supports a
stakeholder decision while making uncertainty and limitations visible.

#### Learning outcomes

Students can:

- distinguish exploratory from explanatory visualization;
- structure an analytical story as context, finding, evidence, explanation,
  implication, and action;
- write takeaway titles and concise annotations;
- design a small dashboard with clear visual hierarchy;
- use filtering, tooltips, highlighting, sorting, drill-down, and linked views
  only when they support a defined task;
- expose filter state and reset behavior;
- distinguish observed values, estimates, forecasts, confidence intervals,
  prediction intervals, and scenario ranges;
- avoid cherry-picked periods, hidden missingness, false precision, causal
  overclaiming, and selective annotation; and
- present a three-minute stakeholder briefing.

#### Session structure

Use two 75–90 minute sessions plus a project studio.

Session A:

- exploration versus explanation;
- audience, decision, and narrative structure;
- descriptive versus takeaway titles;
- direct labels, reference lines, benchmarks, and selective annotation;
- dashboard hierarchy and task-centered layout.

Session B:

- interaction as a question-answering mechanism;
- visible state, reset, and overview-plus-detail;
- confidence and prediction intervals;
- uncertainty language and ethical claims;
- redesign of an overloaded, misleading dashboard.

Because formal time-series forecasting is not taught until Lesson 25, this
lesson may show how to *read* a supplied forecast band but does not assess
forecast construction or detailed forecast diagnostics. Lesson 25 revisits
forecast visualization after students learn the underlying methods.

#### Assessment design

The core project requires students to:

1. define one business question and stakeholder decision;
2. clean and transform a pinned dataset;
3. explore at least three visual alternatives;
4. select one primary visualization;
5. build a small Altair dashboard or analytical report;
6. include meaningful uncertainty or a specific limitation;
7. write a stakeholder-facing conclusion; and
8. present the result in three minutes.

The project rubric separates numeric correctness, visual reasoning,
interaction, uncertainty, communication, and reproducibility.

An optional Tableau or Power BI version may replace the Altair presentation
artifact for portfolio purposes, but the submitted transformation and metric
checks remain Python-based.

## Required ML explanation lesson

### Lesson 24 — Model Diagnostics and Responsible Explanation

#### Purpose

Teach students to diagnose where a model succeeds or fails and to explain model
behavior without presenting attribution as causation.

#### Prerequisites

- regression and classification;
- train/test splits, baselines, cross-validation, leakage, and distribution
  shift;
- regression and classification metrics;
- decision trees, ensembles, and neural-network concepts;
- visualization principles from Lessons 15–17.

#### Learning outcomes

Students can:

- choose diagnostic plots from a model-evaluation question;
- interpret predicted-versus-actual, residual, learning-curve, confusion-matrix,
  precision–recall, ROC, and calibration views;
- compare errors by meaningful subgroup while reporting sample size;
- distinguish model performance, global explanation, local explanation, and
  causal explanation;
- use coefficients, tree structure, and permutation importance appropriately;
- explain the SHAP baseline and additive feature contributions;
- interpret one global SHAP summary and one local SHAP explanation;
- identify leakage, correlated-feature, background-sample, instability, and
  distribution-shift limitations; and
- write a concise model card with evidence and limitations.

#### Session structure

Use two 75–90 minute sessions plus a studio.

Session A:

- diagnostic question hierarchy;
- predicted-versus-actual and residual analysis;
- confusion matrix, threshold trade-offs, and calibration;
- learning curves and train/validation gaps;
- subgroup error slices.

Session B:

- transparent-model explanations first;
- permutation importance and its failure modes;
- SHAP baseline, global summary, and local explanation;
- correlated features and background-sample sensitivity;
- explanation versus causal claim;
- model-card synthesis.

PDP/ICE may be an optional extension within the notebook. ALE and
counterfactual explanations remain in O6.

#### SHAP scope control

Use one small pinned churn model with a fixed train/test split, deterministic
seed, and fixed background sample. Students use the library API rather than
derive Shapley values. They must explain:

- what prediction is being explained;
- the reference or expected model output;
- which features move the prediction up or down;
- whether the view is global or local; and
- why the attribution is not a causal effect.

The lesson must show at least one instability or correlated-feature caution.

#### Assessment design

Students submit a model card or diagnostic report containing:

- selected performance diagnostics;
- one threshold or calibration decision;
- one subgroup error analysis with sample sizes;
- one global explanation;
- one local SHAP explanation; and
- specific limitations and monitoring recommendations.

Automated checks validate metric arrays, confusion counts, calibration inputs,
subgroup counts, deterministic model outputs, and saved artifacts. Human review
evaluates diagnostic selection and explanation quality.

## Optional advanced lesson designs

### O5 — High-Dimensional Projection Visualization

PCA, t-SNE, and UMAP are taught after ML foundations.

Required cautions:

- a two-dimensional gap may be projection-created;
- visible clusters are not proof of natural classes;
- global distances and apparent cluster sizes may be misleading;
- parameters, initialization, random seed, scaling, and preprocessing matter;
- multiple seeds and methods must be compared; and
- visual patterns must be checked against labels, distances, or clustering
  metrics.

The activity applies all three methods to the same pinned dataset and requires
a justified-versus-unjustified conclusions section.

### O6 — Explainable ML in Depth

This module extends Lesson 24 with:

- ALE and PDP/ICE comparison;
- local versus global explanation aggregation;
- counterfactual explanations and feasibility constraints;
- SHAP background sensitivity;
- explanation stability across folds, seeds, and model families;
- correlated-feature attribution ambiguity; and
- subgroup and fairness cautions.

The assessment compares explanations for at least two defensible model
specifications and identifies conclusions that are stable versus method
dependent.

### O7 — Specialized Visualization Modules

O7 is modular rather than one mandatory survey.

Available modules:

- custom D3 and declarative-versus-imperative interaction;
- geospatial maps, projections, normalization, and region-size bias;
- networks, adjacency matrices, force layouts, and hierarchy views;
- animation, continuity, and change blindness; and
- automated chart recommendation and constraint checking.

Each module includes a "when not to use this" section. D3 is recommended only
when declarative Python or BI tools cannot express the required interaction.

## Pedagogical through-line

The required sequence repeatedly uses:

```text
question
→ variable and metric definition
→ validated transformation
→ visual encoding
→ scale and interaction audit
→ uncertainty and limitation
→ stakeholder implication
```

Visualization lessons reuse the course's pinned retail, FRED, A/B test, and
churn data so students spend time on reasoning rather than learning unrelated
domains.

## Reading strategy

Each required lesson assigns:

- one short required research excerpt;
- one concise instructor-provided summary of a second source;
- one optional full reading; and
- one practical chart critique or coding exercise.

Sources are labeled as:

- peer-reviewed research;
- book or textbook excerpt;
- official tool documentation; or
- practitioner essay.

Practitioner essays may motivate discussion but are not presented as equivalent
to empirical research. Exact titles, authors, venues, and stable links must be
verified before the instructor notes are finalized.

The reading families are:

- Lesson 15: Franconeri and collaborators; Cleveland and McGill; Norman;
  optional Healey, Tufte, and the visualization-zoo survey.
- Lesson 16: Brewer on color; Tufte on density and small multiples;
  Wattenberg and Viégas on redesign; Altair/Vega-Lite documentation.
- Lesson 17: Segel and Heer; Heer and Shneiderman; Hullman; selected
  practitioner critiques of interaction.
- Lesson 24: model-evaluation documentation, permutation-importance guidance,
  and Lundberg and Lee on SHAP.
- O5: Wattenberg, Viégas, and Johnson on t-SNE, plus original or authoritative
  PCA, t-SNE, and UMAP references.
- O6: authoritative SHAP, ALE, counterfactual, and explanation-stability
  references.
- O7: authoritative references matched to the selected module.

## Tool and dependency strategy

Required Python tools planned for the complete course:

- pandas and NumPy for transformation;
- Matplotlib for static foundations;
- Altair/Vega-Lite for declarative and interactive visualization;
- scikit-learn for statistical and ML examples; and
- SHAP for Lesson 24.

Tableau and Power BI are supplements because:

- their licenses, accounts, platform support, and offline behavior differ;
- Power BI Desktop is not natively available on macOS;
- Tableau Public may require network access and public sharing; and
- proprietary workbooks are harder to test reproducibly.

The course therefore teaches transferable concepts in Python and supplies BI
translation prompts for portfolio development.

## Data and validation strategy

- Reuse pinned course data wherever possible.
- No required exercise makes a network request.
- Record dataset provenance, date range, row count, and checksum.
- Make units, denominators, date frequency, missingness, and filters explicit.
- Use deterministic seeds for simulation, projection, and model examples.
- Do not silently delete unusual observations.
- Expose filter state in interactive views.
- Keep source transformations inspectable as DataFrames before rendering.

## Assessment and test strategy

Automated checks may validate:

- transformation outputs and metric definitions;
- row counts, groups, denominators, and ordering;
- chart object or declarative-spec structure;
- expected marks, encodings, labels, scales, and facets;
- deterministic model and projection outputs within appropriate tolerances; and
- artifact creation.

Automated checks must not:

- compare rendered images pixel-for-pixel;
- require one exact harmless style choice;
- infer semantic correctness only from artist class names; or
- grade stakeholder interpretation as a string-equality problem.

Human review covers:

- chart choice and perceptual effectiveness;
- misleading or ethical communication;
- uncertainty and limitation quality;
- dashboard hierarchy and interaction usefulness;
- model-explanation caution; and
- stakeholder-facing conclusions.

## Files changed in the staged implementation

1. `README.md`
   - reflow and renumber Lessons 12–27;
   - update phases, assignment references, capstone references, and optional
     lesson list;
   - document the Python-first and BI-supplement strategy;
   - add planned Altair and SHAP dependencies.
2. `Lesson12_Instructor_Notes.md`
   - replace with `Lesson15_Instructor_Notes.md`;
   - preserve useful existing content while adding perception, variable types,
     critique, and the post-statistics prerequisite framing.
3. `Lesson16_Instructor_Notes.md`
   - add the complete trustworthy-visualization design.
4. `Lesson17_Instructor_Notes.md`
   - add the complete dashboard, narrative, interaction, and uncertainty
     design.
5. `Lesson24_Instructor_Notes.md`
   - add the required diagnostics and SHAP design.
6. `Optional_Advanced_Visualization_Instructor_Notes.md`
   - add O5–O7 as modular advanced plans.

No other current lesson notebooks, exercises, fixtures, tests, or user changes
are modified in this pass.

## Risks and mitigations

### Statistics before formal visualization

Risk: students must read histograms, intervals, and residual plots before
Lesson 15.

Mitigation: Lessons 12–14 use instructor-provided, plainly labeled plot
templates and assess statistical interpretation only. Lesson 15 revisits those
same plots to make the encoding choices explicit.

### Course-length growth

Risk: replacing one lesson with three and adding Lesson 24 increases the
required course from 24 to 27 lessons.

Mitigation: every new lesson includes a compressed route. Optional specialized
topics remain optional. Reused datasets reduce setup overhead.

### Tool overload

Risk: Matplotlib, Altair, Tableau, Power BI, and SHAP can become an ecosystem
tour.

Mitigation: Python is required; BI tools are translation labs. Each required
tool has a distinct conceptual role.

### SHAP overinterpretation

Risk: students may describe feature attribution as causation or stable truth.

Mitigation: require baseline, global/local, correlation, background-sample, and
instability cautions in both teaching and assessment.

### Subjective visualization grading

Risk: pixel tests reward imitation and punish valid alternatives.

Mitigation: test data and structural contracts automatically; grade semantics
with a transparent human rubric.

## Acceptance criteria for this pass

- The root README presents one internally consistent 27-lesson sequence.
- All old Lesson 12–24 references affected by the reflow are updated.
- A5, A6, phase headings, optional lessons, and capstone references agree with
  the new numbering.
- Lesson 15 retains the valuable existing Matplotlib and offline-data design.
- Lessons 15–17 have distinct purposes with no major duplicated unit.
- Lesson 24 includes required SHAP content and explicit non-causal cautions.
- O5–O7 are clearly optional and prerequisite-aware.
- Python requirements and BI supplements are unambiguous.
- Every instructor note specifies outcomes, prerequisites, session structure,
  assessment, misconceptions or cautions, future exercise contracts, and
  readings.
- No notebook, exercise, test, fixture, or unrelated user change is modified.
