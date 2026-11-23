# Part 9: Make Programs Faster

Companion code for the video **"Make Programs Faster: Profiling, Caches and Vectorization Explained"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Videos 1–5: https://youtu.be/dLdfrp02n6A · https://youtu.be/FL4Ts9LfBJk · https://youtu.be/2NCCn2o42EA · https://youtu.be/fni53-4dPGk · https://youtu.be/-l_xC6ECaoc
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

- **Profiling:** a stopwatch in every room, so you fix the kitchen, not the hallway.
- **Cache:** a small desk next to a huge warehouse. Locality means keeping related work on the desk.
- **Vectorization (SIMD):** carrying eight eggs in one carton — one instruction handles many numbers. In Python we usually get this from libraries such as NumPy.

Beginner rule: do not guess. Measure first, then fix the slow part.

## What's in here

| File | What it shows |
|---|---|
| `profile_me.py` | Two similar functions, `count_in_list` and `count_in_set`, timed with a stopwatch and then with `cProfile` |
| `cache_rows.py` | A 4,000 × 4,000 C-order NumPy grid, summed row by row and column by column |
| `vector_add.py` | Adds two lists of 2,000,000 numbers with a Python loop, then the same numbers with a NumPy add. Times the add, not the list-to-array conversion |

Needs Python 3.8+ and NumPy.

## Run it

```bash
cd 09-performance
python3 profile_me.py     # the list scan may take a couple of seconds
python3 cache_rows.py
python3 vector_add.py
```

## Observed results from the video

Recorded on 2026-11-23 at 11:49 WAT with CPython 3.13.5 and NumPy 2.5.5 on an 8-CPU Intel Xeon Linux cloud machine. Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `count_in_list`, N=30,000 | result 30,000 in 1,727.2 ms |
| `count_in_set`, N=30,000 | result 30,000 in 2.8 ms |
| cProfile (a separate run) | 1.711 s inside `count_in_list`, 0.003 s inside `count_in_set` |
| `cache_rows.py` | 4,000 × 4,000 float64, C-order True; sum rows 0.019 s; sum columns 0.122 s; same total 127,999,992,000,000 |
| `vector_add.py` | N=2,000,000; Python loop 0.106 s; NumPy add 0.006 s; first three `[2000000, 2000002, 2000004]`; first and last values matched |

## Notes and honest caveats

- These are single runs on one cloud machine. Your numbers will differ, sometimes a lot.
- The cProfile times are from a **separate** run after the stopwatch timings, so they are not the same as 1,727.2 ms and 2.8 ms. Both measurements agree on which function is hot.
- `count_in_list` is slow because `i in xs` scans a list of 30,000 items, 30,000 times. That is the kitchen the profiler named.
- Row vs column timing depends on the array's memory order. This grid is C-order (rows sit together). A Fortran-order array can flip the story. We measured this layout.
- The NumPy add was timed after the arrays already existed. Converting lists to arrays is extra work, not included in the 0.006 s.
- Writing raw SIMD is usually done in C or Rust. In Python we get it by using libraries that already do it.
