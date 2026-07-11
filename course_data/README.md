# Course data snapshots

`build_samples.py` creates the small extracts used in the course notebooks.
They come from the [UCI Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail),
which is licensed under CC BY 4.0.

Run this from the repository root to rebuild the deterministic extract:

```bash
python course_data/build_samples.py
```

The script caches the upstream ZIP in this directory. Use `--refresh` only when
you intentionally want to retrieve the source again.

Generated files:

- `online_retail_sample.csv`: compact real transaction extract
- `lesson2_customers_base.csv`: customer view derived without names
- `lesson2_transactions_base.csv`: transaction view for Lessons 2 and 3
- `manifest.json`: source metadata, retrieval timestamp, row counts, and checksums

Lesson 2 deliberately transforms the base files into controlled examples of
missing values, malformed text, duplicates, orphan keys, refunds, and invalid
dates. Those modifications are teaching fixtures, not claims about the source
data.
