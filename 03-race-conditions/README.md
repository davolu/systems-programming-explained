# Part 3: Why Concurrent Programs Break

Companion code for the video **"Why Concurrent Programs Break: Race Conditions, Deadlocks and Linearizability"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Video 1 (threads, processes and locks): https://youtu.be/dLdfrp02n6A
- Video 2 (lock-free code): https://youtu.be/FL4Ts9LfBJk
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

- **Race condition:** two people check a shared bank account at the same moment. Both see $100, both take $80, and the account ends at -$60. The answer depends on who goes first, not on what you wrote.
- **Deadlock:** two people each hold one key the other needs, and neither lets go. Both wait forever.
- **Livelock:** two people in a hallway keep stepping aside the same way. They're busy, but nobody gets through.
- **Starvation:** one person never gets the bathroom key, because others keep cutting in.
- **Linearizability:** a bakery ticket machine. Even if a crowd presses at once, the tickets must look as if one person pressed at a time, and if you finished before I arrived, my number must be bigger.

## What's in here

| File | What it shows |
|---|---|
| `counter.py` | Two threads add 1,000 each to a shared counter: unsafe vs with a `threading.Lock` |
| `bank.py` | Two people withdraw $80 from $100 at once, for 1,000 "days": check-then-act vs with a lock |
| `src/bin/atomic_bank.rs` | Rust: the same bank with atomics. Plain `load` + `fetch_sub` still races; a `compare_exchange` (CAS) loop fixes it. 20,000 days each |
| `transfer.py` | Two bank transfers in opposite lock order deadlock (detected with a 2 s timeout); same lock order fixes it |
| `tickets.py` | A ticket dispenser used by 8 threads, plus a small **linearizability checker** for its recorded history |

The Python files use only the standard library. The Rust program uses only `std`.

## Run it

You need Python 3 (recorded with CPython 3.13.5) and Rust (recorded with rustc 1.85.1).

```bash
cd 03-race-conditions
python3 counter.py
python3 bank.py
python3 transfer.py
python3 tickets.py

cargo build --release
./target/release/atomic_bank
```

## Real measurements from the video

Recorded on 2026-11-22 at 22:00 WAT on an 8-CPU Intel Xeon (x86-64) Linux machine. Each result is one run of the exact code in this folder (see `recorded_outputs.json`). Results vary between machines and runs.

| Demo | Without the fix | With the fix |
|---|---|---|
| `counter.py` (2 threads × 1,000) | got 1,000 (expected 2,000) | got 2,000 |
| `bank.py` (1,000 days) | 1,000 of 1,000 days went negative, always -$60 | 0 of 1,000; balance always $20 |
| `atomic_bank` (20,000 days, Rust atomics) | 2,056 of 20,000 went negative | 0 of 20,000 (compare-and-swap) |
| `transfer.py` | opposite order: `['stuck', 'done']`, Ada 110, Bob 90, 2.1 s | same order: `['done', 'done']`, Ada 80, Bob 120, 0.2 s |
| `tickets.py` (8 threads × 200) | 1,378 duplicates, 1,202 out of order: NOT linearizable | 0 duplicates, 0 out of order: linearizable |

## Notes and honest caveats

- **The sleeps are deliberate.** `time.sleep(0.001)` in `bank.py` stands in for a slow database lookup, and `time.sleep(0)` in `counter.py` and `tickets.py` deliberately lets another thread run between the read and the write. They widen the gap so the bug shows up every time. Without them, these races can be rare under CPython (a plain `counter += 1` with 4 threads came out exact in my quick tests), which is worse: tests pass, production fails.
- **The Rust demo has no sleep.** Both threads wait at a "starting line" (a spin on an atomic counter) so they really run at the same moment. Even so, plain atomics overdrew about one day in ten here.
- **The deadlock is detected, not endless.** `acquire(timeout=2)` lets the program notice and carry on. With a plain `acquire()`, it would wait forever. In the opposite-order run, one transfer gave up after 2 s, and only then could the other finish.
- **The linearizability checker checks one recorded history.** Passing doesn't prove the code is always correct; a single failure proves it's broken. For a counter-style dispenser, it checks that tickets are exactly 1..N with no duplicates, and that nobody who finished before someone else started got a bigger number.
- **Livelock and starvation** are explained with analogies in the video, not measured demos.
- **Data race vs race condition:** safe Rust refuses to compile data races, but `atomic_bank.rs` compiles fine and still has a race condition. The compiler can't check your logic.
