# Teaching Notes — Why Data Properties Matter

## The high-level idea

A data type answers **“what does one value mean, and what operations make sense?”**
A data structure answers **“how are many values arranged, and how will we use them?”**

These properties predict what a program can do easily, what it should forbid, and what
kinds of bugs may appear.

## Properties of individual values

### Category: numeric, text, boolean, datetime, or categorical

**Intuition.** The category tells Python how to interpret a value. The characters `"12"`
look numeric to a person, but Python treats them as text until we convert them. That is why
`"12" + "3"` produces `"123"`, while `12 + 3` produces `15`.

**Why it matters.** A wrong category produces either an error or, more dangerously, a
plausible but wrong result.

**Real-world examples.**

- Prices and quantities are numeric because arithmetic is meaningful.
- ZIP codes, phone numbers, and account IDs are text because leading zeros matter and
  arithmetic is meaningless.
- `is_fraud` is boolean because the intended operation is a yes/no filter.
- Transaction time is datetime because ordering and time differences matter.
- Industry sector is categorical because it comes from a controlled set of labels.

### Valid operations

**Intuition.** A type is partly a promise about which questions make sense. We can average
prices, sort dates, concatenate names, and negate booleans. “Average customer name” has no
meaning even if names were encoded as numbers.

**Why it matters.** Choosing operations by meaning—not merely by what software permits—is
the difference between valid analysis and nonsense.

**Real-world example.** A stock ticker may use letters or numeric database codes, but it
remains a label. Counting tickers is meaningful; averaging them is not.

### Measurement scale

- **Nominal:** labels with no ranking, such as sector or country.
- **Ordinal:** ordered labels whose gaps are not measurable, such as low/medium/high risk.
- **Interval:** differences are meaningful but zero is arbitrary, such as calendar dates or
  Celsius temperature.
- **Ratio:** differences, ratios, and a true zero are meaningful, such as price or shares.

**Intuition.** The scale is a permission slip for statistics. A bar chart of customer counts
by sector is meaningful; a mean sector is not. Median credit rating can make sense because
ratings are ordered, but saying AAA is “twice” BBB does not.

**Real-world application.** Analytics software may store revenue and a credit-rating code
as numbers. Their storage type is the same, but their measurement scales—and therefore their
valid analyses—are different.

### Falsy values and missing values

**Intuition.** Python uses several empty or zero-like values as “no” inside a condition:
`False`, `None`, `0`, `0.0`, `""`, and empty containers. They are falsy, but they do not
mean the same thing.

**Why it matters.** Revenue of `0` is observed data; revenue of `None` is missing data.
Writing `if revenue:` confuses the two. Use `if revenue is not None:` when presence is the
question.

**Real-world application.** In billing, a zero balance means the customer owes nothing. A
missing balance means the system does not know what the customer owes.

### Casting and dynamic typing

**Intuition.** Casting explicitly changes representation, such as `int("12")`. Dynamic
typing means a Python name may later refer to a value of another type; it does not mean
values have no types.

**Why it matters.** Data commonly arrives from CSV files or web forms as text. Casting is
the bridge from imported representation to intended meaning. Dynamic typing is convenient,
but it shifts more responsibility to testing and clear naming.

**Real-world application.** A checkout form sends quantity as `"3"`. The server must validate
and cast it before calculating a total. An invalid value such as `"three"` should be rejected.

## Properties of containers

### Shape and dimensionality

**Intuition.** Shape describes how many directions are needed to locate a value: scalar
(0D), sequence (1D), table (2D), or tensor (nD).

**Why it matters.** Shape determines which operations line up. A table column can be compared
with another column row by row; matrices can multiply only when their dimensions fit.

**Real-world applications.**

- One temperature is a scalar.
- Daily temperatures are a 1D sequence.
- Temperatures for many cities over many days form a 2D table.
- Video is commonly a 4D tensor: frame × height × width × color channel.

### Ordering

**Intuition.** Ordering answers whether “before,” “after,” or “the third item” has meaning.

**Why it matters.** If order carries information, losing it changes the data. If order does
not matter, a membership-oriented structure may express the problem more clearly.

**Real-world applications.** Browser history, a playlist, and stock prices are sequences
because order matters. A set of users who accepted terms needs membership, not a “third user.”

### Mutability

**Intuition.** Mutable objects can change in place; immutable objects cannot. Immutability
acts like a seal: once created, the value remains stable.

**Why it matters.** Mutation is convenient for evolving state, but aliases can cause distant
code to observe unexpected changes. Immutable values are safe as dictionary keys, cache
keys, coordinates, and configuration constants.

**Real-world applications.** A shopping cart is mutable because items change. A coordinate
is often a tuple because latitude and longitude form one fixed value. An audit record may be
immutable so past events cannot be silently rewritten.

### Uniqueness

**Intuition.** Uniqueness turns “many occurrences” into “which distinct values exist?”

**Why it matters.** Duplicate identifiers can cause double billing, incorrect counts, or
ambiguous lookup. Sets and dictionary keys express a no-duplicates rule.

**Real-world applications.** Deduplicate email recipients with a set; enforce one database
record per customer ID; use set intersection to find users reached by two campaigns.

### Access pattern

**Intuition.** Choose by the question asked most often: “what is at position 3?”, “what
belongs to customer 103?”, or “has this ID appeared?”

**Why it matters.** The right access pattern makes code clearer and often much faster.
Scanning a million-item list repeats work; a dictionary or set is designed for lookup.

**Real-world applications.**

- List: process transactions in arrival order.
- Dictionary/hash map: retrieve an account by account ID.
- Set: block requests from known malicious IP addresses.
- pandas Series: select observations by a meaningful row label.

### Homogeneity

**Intuition.** A homogeneous container stores values of one effective type. With the same
layout for every item, numerical libraries can process a whole memory block efficiently.

**Why it matters.** Python lists trade speed and compactness for flexibility. NumPy arrays
and pandas columns gain fast vectorized operations by using a consistent dtype.

**Real-world applications.** NumPy efficiently transforms millions of image pixels. A pandas
price column can be multiplied, averaged, and checked for missing values at once.

## Structures as combinations of properties

| Structure | Shape | Ordering | Mutable | Duplicates | Main access | Homogeneity |
|---|---|---:|---:|---:|---|---|
| Scalar | 0D | N/A | Usually no | N/A | Direct | One value |
| List | 1D | Yes | Yes | Yes | Position | Mixed allowed |
| Tuple | 1D | Yes | No | Yes | Position | Mixed allowed |
| Set | Collection | No position | Yes | No | Membership | Mixed hashable values |
| Dict / hash map | Key–value | Insertion order | Yes | Keys unique | Key | Mixed values |
| NumPy array | nD | Axis-based | Usually yes | Yes | Integer position | One dtype |
| pandas Series | 1D | Labeled order | Yes | Yes | Label or position | One effective dtype |
| pandas DataFrame | 2D | Labeled axes | Yes | Rows may repeat | Labels | One dtype per column |
| Stack | 1D | LIFO | Yes | Yes | Most recent item | Depends on implementation |
| Queue | 1D | FIFO | Yes | Yes | Oldest item | Depends on implementation |
| Tree | Hierarchical | Depends on tree | Usually yes | Depends | Parent/child path | Mixed allowed |

## Operations as evidence of properties

**Intuition.** A property is invisible until an operation makes it visible. Saying "tuples
are immutable" is abstract; watching `coordinate.append(...)` raise an `AttributeError` is
concrete. The operations a type permits *are* its properties in executable form, and the
operations it forbids are the properties it lacks.

**Why it matters.** This gives a reliable way to reason about an unfamiliar type: don't
memorize a property list — ask which operations it offers. It also turns error messages
from frustrations into diagnoses.

### What each operation says about a data type

| Type | Operation | Property it reflects |
|---|---|---|
| int / float | `+ - * / // % **`, `round`, `abs` | Numeric: arithmetic is meaningful |
| int / float | `10 / 2` returns `5.0` (a float) | The result type is part of the operation |
| str | `s[0]`, slicing, `len`, `in`, `+`, `*` | A string is an ordered *sequence* of characters |
| str | `.upper()` / `.strip()` / `.replace()` return **new** strings; `s[0] = "A"` raises `TypeError` | Immutable: every "change" builds a new value |
| bool | produced by `== != < >`; combined with `and or not`; `sum()` counts them (`True == 1`) | A yes/no answer that can be combined and counted |
| None | only `is None` / `is not None`; `None + 1` raises `TypeError` | Absence of a value: nothing to operate on |

### What each operation says about a native structure

| Structure | Operation | Property it reflects |
|---|---|---|
| List | `sales[0]`, `sales[-1]`, slicing | Ordered: positions are meaningful, including "from the end" |
| List | `append insert remove pop`; `sort()` mutates in place and returns `None` | Mutable: the same object changes |
| List | `sales.count(150)` | Duplicates allowed: counting occurrences is meaningful |
| Tuple | indexing and slicing work | Ordered, like a list |
| Tuple | no `append`/`remove` at all — only `.count` and `.index` exist | Immutable: mutating methods are not merely forbidden, they are absent |
| Tuple | unpacking `lat, lon = coordinate` | Fixed size with a fixed meaning per position |
| Set | fast `in`; `& \| - ^`; subset `<=` | Membership-based, with mathematical set behavior |
| Set | `ids[0]` raises `TypeError` | Unordered: there is no "first element" |
| Set | `len({10, 20, 20}) == 2` | Uniqueness enforced at creation |
| Dict | `d[key]`, `.get(key, default)`, assignment adds keys, `.pop(key)` | Everything is accessed by key, never by position |
| Dict | `in` tests keys (not values); keys must be hashable | The keys form a set: unique and immutable |

**Errors as diagnosis.** When an operation fails, Python names the property that was
assumed wrongly: `TypeError: ... does not support item assignment` means mutability was
assumed; `AttributeError: 'tuple' object has no attribute 'append'` is the same wrong
assumption showing up as a missing method; `TypeError: 'set' object is not subscriptable`
means ordering was assumed; `KeyError` means presence was assumed. Reading errors this way
converts debugging into a review of properties.

## Abstract structures: native structures plus a rule

**Intuition.** Stacks, queues, hash maps, and trees are not new containers Python is
hiding somewhere. They are *usage patterns*: a native structure plus a rule about which
operations you allow yourself. Choosing a structure really means choosing which operations
should be cheap and which should be forbidden.

### Stack — a list used at one end only

**Relation to native structures.** Push is `list.append`, pop is `list.pop()`, peek is
`history[-1]`. The list permits more (popping from the middle is legal); the stack is the
*discipline* of touching only one end.

**Underlying property.** The list's ordering plus a LIFO (last in, first out) restriction.
By construction, the most recent item is always the next one out.

**Why useful.** Undo history, tracking nested function calls, matching brackets — any task
where the most recently seen thing must be handled first.

### Queue — a sequence consumed from the front

**Relation to native structures.** A list *can* do it (`line.pop(0)`), but a list is one
contiguous block of memory, so removing the front shifts every remaining element left.
`collections.deque` is the list-like structure engineered to be fast at both ends.

**Underlying property.** Ordering plus a FIFO (first in, first out) restriction — fairness:
whoever arrived first is served first.

**Why useful.** Request handling, print jobs, task processing, breadth-first traversal —
any task where arrival order must be honored.

### Hash map — the dictionary, literally

**Relation to native structures.** Python's dict *is* a hash map; every dict operation
(`get`, `in` on keys, key assignment) is a hash-map operation. Additionally, dict keys
behave like a set: unique, hashable, and set operators work directly on `d.keys()`.

**Underlying property.** Key-based lookup — retrieval by identifier rather than by
position, with no scanning.

**Why useful.** Any "find the record for this ID" question: price by ticker, account by
account number, configuration by name.

### Tree — dictionaries nested inside lists

**Relation to native structures.** Each node is a dict (named fields → key access); each
node's children are a list (ordered → position access). Reaching a grandchild chains the
two native operations: `tree["children"][1]["children"][0]`. Growing the tree is just
`list.append`. This nested dict+list shape is exactly what JSON stores.

**Underlying property.** Hierarchy: every item has one parent, and paths from the root
locate items.

**Why useful.** File systems, organization charts, HTML pages, nested JSON from APIs —
data whose meaning lives in its nesting.

### NumPy array — a list with the flexibility removed

**Relation to native structures.** Like a list it is ordered and positional (indexing,
slicing, `len`). Unlike a list, it holds one dtype (mixed input is silently coerced) and
has a fixed size (no `.append` method; `np.append` builds a new array — closer to tuple
thinking than list thinking).

**Underlying property.** Homogeneity plus fixed size, which lets the data live in one
uniform memory block.

**Why useful.** The rigidity buys operations no native container has: elementwise math
(`a * 1.05`), elementwise comparison (`a > 1000`), and boolean masking (`a[a > 1000]`) —
the foundation for fast bulk numeric work, and for pandas in the next lesson.

**Practical rule.** When meeting a new structure name, ask two questions: which native
structure is underneath, and which operations did the pattern restrict or accelerate?

## How structures influence file storage

Files preserve some properties and lose others:

- **CSV** preserves a 2D rectangle and row order, but has weak type information, no nesting,
  and no built-in uniqueness rule.
- **JSON** naturally preserves scalars, lists, and nested key–value structures. It does not
  directly preserve tuples, sets, NumPy dtypes, or pandas indexes.
- **NumPy `.npy`** preserves an array's shape and dtype efficiently.
- **Parquet** preserves a typed table by column and compresses homogeneous columns well.
- **A database table** can add schemas, unique constraints, and indexes for fast lookup.

Practical rule: choose an in-memory structure for the operations the program needs, then
choose a file format that preserves the important properties of that structure.
