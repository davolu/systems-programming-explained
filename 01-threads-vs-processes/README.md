# Threads vs Processes Explained
**Make Your Python Code 20x Faster** · Systems Programming Explained, part 1  
David Oluyale | Agentic AI Hub

Think of a program as a restaurant. A thread is a cook sharing the same kitchen (memory); a process is a separate kitchen. An async task is a table served by one organised waiter. A lock is a bathroom key: only one holder may enter.

## Run it

Python 3.10+; no third-party packages, keys or accounts required. Standard GIL-enabled CPython is assumed for the GIL comparison. Use Python 3.10–3.13 in a normal script for the closest reproduction of the recorded run.

```bash
python 01_one_cook_downloads.py
python 02_many_cooks_threads.py
python 03_gil_threads_vs_processes.py
python 04_race_condition_and_lock.py
python 05_deadlock.py
python 06_asyncio_downloads.py
python 07_agent_parallel_tools.py
```

Or open `Threads_vs_Processes.ipynb` in Colab or Jupyter and run it top to bottom. `Threads_vs_Processes_EXECUTED.ipynb` contains the real recorded outputs. The process-pool cell may require running the separate script on Windows/macOS or newer Python using a non-fork start method, because workers must be able to import their target function. Do not wrap notebook `await` calls with `asyncio.run` (the notebook already has an event loop). The scripts use the proper `if __name__ == "__main__":` guard and `asyncio.run`.

## What you'll learn

1. Concurrency = juggling overlapping tasks; parallelism = truly doing tasks simultaneously.
2. `ThreadPoolExecutor`: many cooks overlap network waits.
3. The Global Interpreter Lock (GIL): one Python-code rule book per kitchen. Processes have separate interpreters and can calculate on multiple cores.
4. A race condition: workers overwrite shared read-modify-write state. `threading.Lock` protects the complete update.
5. A deadlock: workers each hold something the other needs. Take locks in the same global order. The demo uses a timeout so it cannot wait forever.
6. `asyncio`: one waiter switches cooperatively while tasks wait.
7. Independent AI-agent tools can run together; dependent or side-effecting actions still require ordering and permission.

## Real measurements shown in the video

Linux, CPython 3.13.5, 8 logical CPUs, standard GIL-enabled build. Recorded 22 November 2026, WAT (Africa/Lagos). These are one illustrative run, not a controlled benchmark suite. See `recorded_outputs.json` for stdout and output timestamps. Your machine, CPU quota, start method and background load change the numbers.

| Workload | Measured result (rounded, as printed) |
|---|---|
| 20 sequential simulated 1-second downloads | 20.0 s |
| Same 20 downloads, 20 threads | 1.0 s |
| 8 × 10,000,000 pure-Python square-sum jobs, sequential | 2.3 s |
| Same CPU jobs, 8 threads | 2.5 s |
| Same CPU jobs, 8 processes | 0.4 s |
| 5 × 1,000 unsafe shared increments | 1,006 instead of 5,000 |
| Same increments with a lock | 5,000 |
| 20 async simulated 1-second downloads | 1.0 s on one thread |
| Simulated tools (1.0 + 1.5 + 2.0 s), sequential | 4.5 s |
| Same tools together | 2.0 s |

The headline **20 s → 1 s** uses rounded values for simulated I/O waits. No real download endpoint is contacted. The exact cell elapsed times were 20.003 s and 1.016 s; that ratio is about 19.69× before rounding. It is not a promise of 20× acceleration for all Python code. A real network has bandwidth limits, server limits and failures. The video compresses longer waiting periods and labels the playback speed-up; printed results remain the measured results.

The race demonstration deliberately calls `time.sleep(0)` between read and write to expose a possible interleaving. The incorrect total and deadlock timeout winner vary by run. The GIL does not make a whole multi-step update safe. Optional free-threaded Python builds and libraries that release the GIL (for example NumPy) have different performance rules. Small process jobs can be slower due to startup and data transfer; free Colab may provide fewer cores than this recording.

The weather/calendar/search tools are **simulated sleeps**, not live APIs, model calls or real calendar access. Do not parallelise actions that depend on each other's results or bypass approval requirements.

## Links

- [Code folder](https://github.com/davolu/systems-programming-explained/tree/main/01-threads-vs-processes)
- [Agentic AI Hub](https://www.youtube.com/@AgenticAIHub1)
- [Python Crash Course](https://youtu.be/ZaY_l07IZSo)

Next: **Lock-Free Code Explained: How Fast Programs Share Data Without Locks**.
