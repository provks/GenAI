# Day 1 — Python Foundations

Quick, simple notes. No long explanations — just what you need to know and practice.

## What you need to know

### Lists, Tuples, Dictionaries

| Thing | What it is | Example |
|---|---|---|
| **List** | An ordered group of items you *can* change (add/remove/edit). | `fruits = ["apple", "banana", "mango"]` |
| **Tuple** | Same as a list, but you *cannot* change it after creating it. | `point = (10, 20)` |
| **Dictionary** | A group of `key: value` pairs — like a real dictionary (word → meaning). | `student = {"name": "Ravi", "age": 20}` |

**When to use which:** List when the data can change. Tuple when it should never change (e.g. coordinates). Dictionary when you want to look things up by name instead of by position.

### Virtual Environment (`venv`)

A **virtual environment** is a clean, separate box for one project's Python packages — so installing something for Project A doesn't break Project B.

```bash
python -m venv venv          # create it (one-time per project)
source venv/bin/activate     # turn it on (Mac/Linux)
venv\Scripts\activate        # turn it on (Windows)
```

You'll know it's on because your terminal line starts with `(venv)`.

### `pip` (installing packages)

`pip` is Python's package installer — it downloads code other people wrote so you don't have to write it yourself.

```bash
pip install requests
```

### `requirements.txt` (freezing dependencies)

A `requirements.txt` file is just a list of every package your project needs, with exact versions — so anyone else (or you, on a new laptop) can install the exact same setup.

```bash
pip freeze > requirements.txt     # save the list
pip install -r requirements.txt   # install from the list
```

## Pass criteria (what you should be able to do)

- [ ] Create and activate a clean `venv`
- [ ] Run `pip install` and `pip freeze > requirements.txt`
- [ ] Use lists, tuples, and dicts correctly without looking anything up

## Learn more

### 🎥 YouTube crash courses

**English:**
- [Python Tutorial for Beginners 4: Lists, Tuples, and Sets](https://www.youtube.com/watch?v=W8KRzm-HUcc) — Corey Schafer (~29 min)
- [Python Tutorial: VENV — How to Use Virtual Environments](https://www.youtube.com/watch?v=APOPm01BVrk) — Corey Schafer (~17 min)

**Hindi:**
- [Lecture 3: List & Tuple in Python | Python Full Course](https://www.youtube.com/watch?v=qVyvmzFxF_o) — Apna College (~41 min)
- [Lecture 4: Dictionary & Set in Python | Python Full Course](https://www.youtube.com/watch?v=078tYSD7K8E) — Apna College (~54 min)
- [Virtual Environment & Requirements.txt | Python Tutorials For Absolute Beginners #43](https://www.youtube.com/watch?v=Lah7WGW6exg) — CodeWithHarry (~21 min)

### 💻 GitHub reference projects

- [trekhleb/learn-python](https://github.com/trekhleb/learn-python) — a large, well-organized collection of annotated Python scripts (with tests) covering lists, tuples, dicts and more — great for practicing.
- [navdeep-G/samplemod](https://github.com/navdeep-G/samplemod) — a minimal example of a real Python project layout, including a proper `requirements.txt`.

### 🎓 Free certification

- [Python for Beginners — Free Course with Certification (Simplilearn SkillUp)](https://www.simplilearn.com/learn-python-basics-free-course-skillup) — completely free, 11 hours self-paced, includes a certificate of completion.
