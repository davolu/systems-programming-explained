# Part 2: Lock-Free Code Explained

Companion code for the video **"Lock-Free Code Explained: How Fast Programs Share Data Without Locks"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Video 1 (threads, processes and locks): https://youtu.be/dLdfrp02n6A
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The idea in one analogy

A **lock** is like the single key to a shared bathroom. Only one person can hold it, and everyone else waits in the queue. When many threads want the same key at once (that's called *contention*), they spend more time waiting than working.

**Lock-free** code skips the key. Each thread makes one small, unbreakable change (an *atomic* operation). If someone else changed the value first, it simply tries again: *compare-and-swap (CAS) in a retry loop*.

## What's in here

| File | What it shows |
|---|---|
| `lock_baseline.py` | Python baseline: 1 vs 4 threads adding to a counter under a `threading.Lock` (2,000,000 additions) |
| `src/bin/mutex_counter.rs` | Rust: N threads share 8,000,000 additions through a `Mutex<u64>` |
| `src/bin/atomic_counter.rs` | Same job with an `AtomicU64` and `fetch_add`; no lock at all |
| `src/bin/cas_counter.rs` | A hand-written CAS retry loop (`compare_exchange_weak`) that also counts how often it had to retry |
| `src/bin/stack.rs` | A lock-free Treiber stack: 4 threads push 100,000 items each, then 4 threads pop them all |
| `src/bin/ordering.rs` | Memory ordering for beginners: write the "meal" (`Relaxed`), ring the "bell" (`Release` / `Acquire`) |

Everything uses only the Rust standard library (`std::sync::atomic`); there are no external crates.

## Run it

You need Rust (any recent stable; recorded with rustc 1.85.1) and Python 3.

```bash
cd 02-lock-free
cargo build --release

# Python lock baseline
python3 lock_baseline.py

# Mutex vs atomic (the argument is the thread count; default 8)
./target/release/mutex_counter 8
./target/release/atomic_counter 8

# The benchmark loop from the video
for t in 1 2 4 8; do
  ./target/release/mutex_counter $t
  ./target/release/atomic_counter $t
done

# CAS retry loop, lock-free stack, memory ordering
./target/release/cas_counter
./target/release/stack
./target/release/ordering
```

## Real measurements from the video

Recorded on 2026-11-22 on an 8-CPU Intel Xeon (x86-64) Linux machine, with rustc 1.85.1 (`--release`) and CPython 3.13.5. Each number comes from one run of the exact code in this folder. Timings vary between machines and runs, so treat them as an example, not a promise.

**Python, 2,000,000 additions under a lock:** 1 thread 0.18 s, 4 threads 0.19 s (more threads did not help).

**Rust, 8,000,000 additions (benchmark loop):**

| Threads | `Mutex` | `AtomicU64` |
|---|---|---|
| 1 | 89 ms | 37 ms |
| 2 | 685 ms | 111 ms |
| 4 | 915 ms | 122 ms |
| 8 | 1007 ms | 126 ms |

On their own, the single runs shown in the video gave Mutex 983 ms and atomic 114 ms with 8 threads.

**CAS counter (8 threads × 1,000,000):** `counter = 8000000`, `retries = 4489106`. Every addition landed, but threads had to retry about 4.5 million times because others changed the value first.

**Lock-free stack:** `pushed 400000, popped 400000, empty now: true`.

**Memory ordering:** `bell rang, meal = 42`.

## Notes and honest caveats

- **The stack leaks on purpose.** `pop` never frees nodes. That keeps the demo short and memory-safe: freed memory can't be reused, so the **ABA problem** can't happen here. Real lock-free structures use version tags, or safe memory reclamation such as epoch-based reclamation or hazard pointers (for example, the `crossbeam` crate).
- **ABA in plain English:** you see plate A on top, look away, someone takes A, adds B, then puts A back. A plain CAS sees "still A" and wrongly assumes nothing changed. The video explains this with an animated diagram, not a measured demo.
- **Memory ordering on x86:** x86 CPUs are strongly ordered, so code with weaker orderings often *happens* to work there. `Release` / `Acquire` make the meal-then-bell rule **guaranteed** on every CPU (including ARM). Don't rely on "it worked on my laptop".
- **When not to go lock-free:** if a plain `Mutex` is fast enough, keep it. Lock-free code is harder to write, test and review. Use proven libraries (Rust's atomics, `crossbeam`, Tokio's queues, Java's `java.util.concurrent`) before writing your own.
