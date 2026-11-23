# Part 10: Catch Bugs Before You Run

Companion code for the video **"Catch Bugs Before You Run: Types, Static Analysis and Program Verification"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub). This is the last part of the series.

- Videos 1–5: https://youtu.be/dLdfrp02n6A · https://youtu.be/FL4Ts9LfBJk · https://youtu.be/2NCCn2o42EA · https://youtu.be/fni53-4dPGk · https://youtu.be/-l_xC6ECaoc
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

- **Types:** labelled boxes. A box marked "only socks" should not accept a cat. A checker can stop you at the door.
- **Static analysis:** a careful friend who reads your recipe without cooking, and spots "you never bought eggs."
- **Tests:** bake a few cakes. **Verification:** try to show the recipe cannot go wrong for any cake, like a maths proof.

## What's in here

| File | What it shows |
|---|---|
| `greet.py` | A function that works for `"Maya"` and crashes at runtime with `None` |
| `greet_typed.py` | The same function with type hints, still calling `greet(None)` so a checker can flag it |
| `tiny_linter.py` | Walks a Python AST and flags an unused variable and a missing return |
| `withdraw.py` | A `withdraw` rule that must never go negative. Three handwritten tests miss a bug that an exhaustive check of 121 cases finds |

`greet.py`, `tiny_linter.py` and `withdraw.py` are standard-library Python 3.8+. `greet_typed.py` is meant to be checked with mypy (`pip install mypy`).

## Run it

```bash
cd 10-static-analysis
python3 greet.py
python3 -m mypy --no-error-summary greet_typed.py
python3 tiny_linter.py
python3 withdraw.py
```

## Observed results from the video

Recorded on 2026-11-23 at 11:48 WAT with CPython 3.13.5 and mypy on an 8-CPU Intel Xeon Linux cloud machine. Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `greet("Maya")` | `Hello, Maya!` |
| `greet(None)` | `TypeError: can only concatenate str (not "NoneType") to str` |
| mypy on `greet_typed.py` | `greet_typed.py:5: error: Argument 1 to "greet" has incompatible type "None"; expected "str"  [arg-type]` |
| `tiny_linter.py` | line 2: unused variable `'leftover'` in `'add'`; line 7: function `'greet'` has no return; line 7: unused variable `'message'` in `'greet'` |
| handwritten tests | `(10, 3)`, `(10, 0)`, `(5, 5)` looked fine for both versions |
| exhaustive check | 11 balances × 11 amounts = 121 cases; buggy failures: 55, first `(0, 1, -1)`; ok failures: 0 |

## Notes and honest caveats

- mypy does not run the function. It flagged `None` from the type hints alone. Running `python3 greet_typed.py` would still crash, because CPython does not enforce those hints at runtime.
- The linter is a miniature: it looks for unused assigned names and missing `return`s. It does not understand control flow in depth, and a function that is meant to return `None` would also be flagged.
- The "verification" demo checks every pair of values in a small integer range. That is not a formal proof about all integers, and it does not replace a real verifier. It does show a bug that three easy tests missed.
- Beginner rule: add types and run a checker on every change. Tests show some bugs exist. Types and analysis try to show whole classes of bugs do not.
- Full formal verification shows up in compilers, CPUs, and safety-critical software. We met the idea at a small scale.
