# Lesson 3 — Bash, Virtual Environments, Git · Terminal demo notes

*Instructor notes for a live terminal demo. 5 units over 3 sessions. All expected outputs below are real outputs from this machine against the actual course files — if the screen matches the notes, you're on script.*

**Through-line:** your computer is also a data structure. The filesystem, a virtual environment, and a git history are all trees of properties — Lesson 1's framing, one level down.

---

## Before class — prep checklist

- [ ] Fresh terminal window, font size bumped (⌘+ a few times).
- [ ] `rm -rf ~/Desktop/lesson3_demo` if left over from rehearsal.
- [ ] Start in the course folder: `cd ~/Desktop/"Intro to CS"` — the quotes are needed because of the space, and that's itself a Unit 2 talking point. Don't explain it yet; just type it and move on.
- [ ] Know your two Pythons: `python3` is Anaconda 3.11.8, `python3.12` is the python.org 3.12.2 the course standardizes on. Unit 3 uses this contrast deliberately.

---

# Session 1

## Unit 1 — The shell as a REPL for your computer · ~45 min

**Say:** "Jupyter is a conversation with Python. The terminal is the same kind of conversation — but with the whole computer."

### 1.1 Where am I, what's here

```bash
pwd
```
```
/Users/tingxuanhuang/Desktop/Intro to CS
```

```bash
ls
ls course_data
```
```
README.md
build_samples.py
lesson2_customers_base.csv
lesson2_transactions_base.csv
manifest.json
online_retail_sample.csv
online_retail_source.zip
```

**Say:** "Folders inside folders — this is a tree, the same shape as the nested dictionaries from Lesson 1. `pwd` tells you which node of the tree you're standing on."

### 1.2 Look at data without opening anything

```bash
head -3 course_data/online_retail_sample.csv
```
```
invoice_id,StockCode,Description,Quantity,InvoiceDate,UnitPrice,source_customer_id,Country
536381,21166,COOK WITH WINE METAL SIGN ,1,2010-12-01 09:41:00,1.95,15311,United Kingdom
536381,21169,YOU'RE CONFUSING ME METAL SIGN ,3,2010-12-01 09:41:00,1.69,15311,United Kingdom
```

```bash
wc -l course_data/online_retail_sample.csv
```
```
      61 course_data/online_retail_sample.csv
```

**Ask her:** "61 lines. How many transactions?" → 60. The header is a line but not a row. This is the Lesson 2 "interview the file before trusting it" habit, now doable in one second, before Python even starts.

### 1.3 Search without loading

```bash
grep -c "15311" course_data/online_retail_sample.csv
```
```
6
```

**Say:** "Customer 15311 appears 6 times." Then immediately undercut it: "Actually — grep found the *string* 15311 anywhere on a line. If a product code contained 15311, it would count too. grep knows strings; it does not know columns. Remember that thought."

### 1.4 Pipes — and a trap I'm setting on purpose

**Say:** "The `|` symbol feeds one command's output into the next — like nesting function calls, `sort(cut(file))`, but read left to right."

```bash
cut -d, -f8 course_data/online_retail_sample.csv | tail -n +2 | sort | uniq -c | sort -rn
```
```
  46 United Kingdom
   6 Netherlands
   6 EIRE
   1 14298
   1 0.83
```

Walk the pipe first: `cut` takes field 8 splitting on commas → `tail -n +2` drops the header → `sort | uniq -c` counts each value → `sort -rn` ranks.

**Then point at the bottom two lines and wait.** A customer ID and a price of £0.83 are apparently countries.

**The reveal:** two rows have a comma *inside* the quoted product description. `cut` splits on every comma — it doesn't know CSV quoting rules. So field 8 shifts on exactly those rows.

**Say:** "CSV quoting is a *property* of the format, and every tool either knows it or doesn't. `cut` doesn't. pandas does — and in Session 3 we'll ask pandas the same question and get the honest answer: UK is 48, not 46. Storage is not neutral, and neither are tools."

*(Verified: `pd.read_csv` on this file → United Kingdom 48, EIRE 6, Netherlands 6.)*

---

## Unit 2 — Paths and "where am I" · ~35 min

**Say:** "Half of all beginner errors are the computer and the human disagreeing about where 'here' is."

### 2.1 Absolute vs. relative

```bash
pwd
head -1 course_data/online_retail_sample.csv                                  # relative: from here
head -1 "/Users/tingxuanhuang/Desktop/Intro to CS/course_data/online_retail_sample.csv"   # absolute: from the root
```

Same file, two addresses. Relative paths are shorter but only valid from the right starting point. Also introduce `~` (home), `.` (here), `..` (up one).

### 2.2 Break it live

```bash
cd course_data
head -1 course_data/online_retail_sample.csv
```
```
head: course_data/online_retail_sample.csv: No such file or directory
```

**Say:** "The file didn't move. *We* moved. The relative path is now wrong." Fix it both ways:

```bash
head -1 online_retail_sample.csv     # correct relative path from here
head -1 ../course_data/online_retail_sample.csv   # or: go up, then down — silly but legal
cd ..
```

**Connect to her experience:** "When a notebook says `FileNotFoundError` on a file you can *see*, this is almost always why — the notebook's 'here' isn't your 'here'."

### 2.3 Quality of life

- **Tab completion:** type `head -1 course_d⇥` — the shell finishes it. "Never type a full filename again; tab also *proves the path exists* as you build it."
- **Spaces in names:** `cd ~/Desktop/Intro to CS` fails — the shell reads three separate words. That's why we quote: `cd ~/Desktop/"Intro to CS"`. (This is the mystery from the prep step, now resolved.)
- **Bridge to Finder:** `open .` opens the current folder in Finder — the terminal and Finder are two views of the same tree.

**End Session 1. Homework thought:** "Find any file on your computer in Finder, then reach the same file in the terminal with `cd` and tab completion."

---

# Session 2

## ⏱️ Session 2 warm-up · 5 questions from last time

1. What does `pwd` tell you, in tree language?
2. `wc -l` said 61 — why is the number of transactions 60?
3. What does `|` do?
4. Our country count listed `0.83` as a country. What actually happened?
5. Your notebook throws `FileNotFoundError` on a file you can see in Finder. What's the first hypothesis?

<details><summary>Answers</summary>

1. Which node of the filesystem tree you're currently standing on.
2. The header line counts as a line but isn't a data row.
3. Feeds the left command's output into the right command — function composition, read left to right.
4. Two descriptions contain commas; `cut` splits on every comma and doesn't know CSV quoting, so field 8 shifted on those rows.
5. The notebook's working directory isn't what you think — the relative path starts from the wrong "here".
</details>

---

## Unit 3 — Virtual environments · ~40 min

### 3.1 Whose Python is this?

```bash
which python3
python3 --version
```
```
/opt/anaconda3/bin/python3
Python 3.11.8
```

**Say:** "I have *several* Pythons on this machine and so will you, eventually. This one belongs to Anaconda. The course uses another:"

```bash
which python3.12
python3.12 --version
```
```
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12
Python 3.12.2
```

**The problem venvs solve:** every `pip install` lands in *some* Python's shared library folder. Project A needs pandas 2.x, project B needs 3.x → they fight. A venv gives each project its own private copy of Python's library folder.

### 3.2 Make one

```bash
mkdir ~/Desktop/lesson3_demo
cd ~/Desktop/lesson3_demo
python3.12 -m venv .venv
source .venv/bin/activate
```

Prompt now shows `(.venv)`. Then the punchline:

```bash
which python3
```
```
/Users/tingxuanhuang/Desktop/lesson3_demo/.venv/bin/python3
```

**Say:** "Activation didn't install anything — it just changed which Python answers when I call. 'Here' for commands, like 'here' for paths."

### 3.3 Install, snapshot, leave

```bash
pip list                       # nearly empty — a newborn environment
pip install pandas
pip freeze > requirements.txt
cat requirements.txt
deactivate
which python3                  # back to /opt/anaconda3/bin/python3
```

**Property framing (say this):** "An environment is a *named snapshot of dependencies*. `requirements.txt` is its schema — the checklist that lets anyone rebuild it with one command: `pip install -r requirements.txt`. Same move as Lesson 2: exporting in a format that preserves the properties you care about."

---

## Unit 4 — Git essentials · ~60 min

**Say:** "Git is checkpoints for a folder. A commit is a snapshot you can always return to; a diff is the exact change between two snapshots."

### 4.1 A repository is born

Still in `~/Desktop/lesson3_demo` (venv active or not — doesn't matter, git doesn't care):

```bash
git init
git status
```

`git status` shows `.venv/` and `requirements.txt` as untracked.

### 4.2 First decision: what does NOT belong in history

```bash
echo ".venv/" > .gitignore
git status
```

`.venv` vanishes from the listing. **Say:** "The venv is rebuildable from `requirements.txt` — we track the *recipe*, never the *kitchen*. Same rule later for data files: track the code that makes them, not the gigabytes."

### 4.3 The add → commit rhythm

```bash
git add .gitignore requirements.txt
git commit -m "Start project: pin dependencies"
```

Then create a tiny script (any editor, or heredoc for speed):

```bash
cat > analyze.py << 'EOF'
import pandas as pd

def total_revenue(csv_path):
    df = pd.read_csv(csv_path)
    return (df["Quantity"] * df["UnitPrice"]).sum()
EOF
git add analyze.py
git commit -m "Add revenue calculation"
```

**Explain the two-step deliberately:** `add` chooses what goes into the photo; `commit` takes the photo. Feels bureaucratic with one file; is a superpower when you've touched five files and only two belong together.

### 4.4 Diff — the payoff

Edit `analyze.py`: add a line at the bottom, e.g. `# TODO: revenue by country`. Then:

```bash
git diff
```

Green `+` line, nothing else. **Say:** "Git answers 'what changed since my last checkpoint' *exactly*, down to the character. You will never again wonder what you edited at 2am."

```bash
git add analyze.py
git commit -m "Note next step"
git log --oneline
```

Three commits — the project's history as a readable story.

### 4.5 Branches, sixty seconds only

```bash
git switch -c experiment
echo "# risky idea" >> analyze.py
git add analyze.py && git commit -m "Try risky idea"
git switch main
cat analyze.py        # the risky line is GONE
git switch experiment
cat analyze.py        # ...and it's back
git switch main
git merge experiment  # decided we like it after all
```

**Say:** "A branch is a parallel timeline. Experiment freely, keep or discard. That's all we need today — sharing timelines with other people (GitHub) is a future lesson."

**End Session 2.**

---

# Session 3

## ⏱️ Session 3 warm-up · 5 questions from last time

1. What problem does a virtual environment solve?
2. After `source .venv/bin/activate`, what did `which python3` prove?
3. Which file is the "recipe" that rebuilds an environment, and what command uses it?
4. What's the difference between `git add` and `git commit`?
5. Why did we put `.venv/` in `.gitignore` but not `requirements.txt`?

<details><summary>Answers</summary>

1. Different projects need different (conflicting) library versions; a venv gives each project a private library folder.
2. That activation changes *which Python answers* — the command now resolves to the venv's copy.
3. `requirements.txt`, via `pip install -r requirements.txt`.
4. `add` stages what will be in the snapshot; `commit` actually takes the snapshot.
5. The venv is rebuildable from the recipe — track recipes, not kitchens.
</details>

---

## Unit 5 — Running Python outside Jupyter · ~30 min

**Say:** "Notebooks are for exploring. Scripts are for keeping. Today the two worlds connect."

In `~/Desktop/lesson3_demo`, venv activated, extend `analyze.py`:

```python
import sys
import pandas as pd

def total_revenue(csv_path):
    df = pd.read_csv(csv_path)
    return (df["Quantity"] * df["UnitPrice"]).sum()

if __name__ == "__main__":
    path = sys.argv[1]
    print(f"Total revenue: {total_revenue(path):.2f}")
```

Run it against the course data — note the quoted path (Unit 2 payoff):

```bash
python3 analyze.py ~/Desktop/"Intro to CS"/course_data/online_retail_sample.csv
```
```
Total revenue: 1421.09
```

Three things to name while it's on screen:

1. **`sys.argv`** — the script has *inputs from the terminal*, like a shell command. She just wrote a tool, not a notebook.
2. **`if __name__ == "__main__":`** — "run this part only when executed directly, not when imported." One sentence now; Lesson 5 leans on it hard when tests import her functions.
3. **The pandas rematch (promised in Unit 1):** open `python3` interactively (or a quick `-c`), run `pd.read_csv(...)["Country"].value_counts()` → **United Kingdom 48, EIRE 6, Netherlands 6**. The shell's naive comma-split said 46; pandas knows the quoting property. Right tool, right answer.

Commit the final script. `git log --oneline` one last time — the whole session is now history, literally.

---

## Exercise handoff — the broken project

Give her a folder that fails in three ways she has now seen; she fixes it using only this lesson.

**Setup (you run this before her session):** the generator script in Appendix A creates `~/Desktop/lesson3_exercise` containing:

- `report.py` — a small pandas script whose relative data path assumes the wrong working directory *(Unit 2 fix)*
- `requirements.txt` — present, but nothing is installed and no venv exists *(Unit 3 fix: create `.venv`, install from the recipe)*
- no git history, and a leftover junk file `scratch_v2_final_FINAL.py` *(Unit 4 fix: init, `.gitignore` the junk or delete it, then commit each repair separately)*

**Her success criteria (tell her these up front):**

1. `python3 report.py` runs from inside the folder and prints the revenue table.
2. `pip freeze` inside her venv matches `requirements.txt`.
3. `git log --oneline` shows ≥ 3 commits with messages that say *why*, not just *what*.

---

## Wrap-up — the property checklist, one level down

| Thing | Its properties | Command that reveals them |
|---|---|---|
| Filesystem | a tree; you always stand on one node | `pwd`, `ls` |
| A path | valid only relative to a starting point | `cd`, tab completion |
| A CSV in the shell | text lines; quoting rules invisible to `cut`/`grep` | the Unit 1 trap |
| An environment | a named snapshot of dependencies | `which python3`, `pip freeze` |
| A git repo | a chain of property snapshots | `status`, `diff`, `log` |

**Extensions:** MIT Missing Semester (shell + git lectures) · Pro Git book, ch. 1–2 · Python `venv` docs · `man` pages (`man wc` — the built-in documentation she can now read).

---

## Appendix A — Broken-project generator

Run once before her exercise session. Creates `~/Desktop/lesson3_exercise` in its intended broken state.

```bash
#!/bin/bash
set -e
EX=~/Desktop/lesson3_exercise
rm -rf "$EX"
mkdir -p "$EX"

cat > "$EX/report.py" << 'EOF'
"""Monthly revenue report. Run me and I print revenue by country."""
import pandas as pd

# BUG(paths): this assumes you launched python from ~/Desktop, not from inside this folder
df = pd.read_csv("Intro to CS/course_data/online_retail_sample.csv")

df["revenue"] = df["Quantity"] * df["UnitPrice"]
print(df.groupby("Country")["revenue"].sum().round(2).sort_values(ascending=False))
EOF

cat > "$EX/requirements.txt" << 'EOF'
pandas
EOF

echo "temporary junk, do not keep" > "$EX/scratch_v2_final_FINAL.py"

echo "Broken project created at $EX"
echo "Intended fixes: 1) data path  2) venv + install from requirements  3) git init + 3 commits"
```

Note: `report.py`'s path bug is *doubly* instructive — even fixed relative to `~/Desktop`, the space in `Intro to CS` never needs quoting *inside Python strings*, only in the shell. If she asks why, that's a gold-star question.

## Appendix B — Her cheat sheet (print or share after Session 3)

| Command | What it does |
|---|---|
| `pwd` / `ls` / `cd X` / `cd ..` | where am I / what's here / move down / move up |
| `head -n F` / `wc -l F` / `grep "s" F` | peek / count lines / search |
| `A \| B` | feed A's output into B |
| `python3.12 -m venv .venv` | create an environment |
| `source .venv/bin/activate` / `deactivate` | enter / leave it |
| `pip install -r requirements.txt` / `pip freeze` | rebuild from recipe / write recipe |
| `git status` / `add` / `commit -m` | what changed / stage / checkpoint |
| `git diff` / `log --oneline` | exact changes / the story so far |
| `open .` | escape hatch to Finder |
