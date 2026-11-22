"""Thinking (CPU-bound) work: one cook vs 8 threads vs 8 processes.
Threads don't help here because of the GIL; processes do, up to the number of CPU cores you have."""
import os
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def chop(n):
    total = 0
    for i in range(n):
        total += i * i  # pure thinking work, no waiting
    return total


jobs = [10_000_000] * 8  # 8 big jobs

if __name__ == "__main__":  # needed: each new process re-imports this file
    print("CPU cores on this machine:", os.cpu_count())

    start = time.perf_counter()
    for n in jobs:
        chop(n)
    print(f"One cook:    {time.perf_counter() - start:.1f} s")

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(chop, jobs))
    print(f"8 threads:   {time.perf_counter() - start:.1f} s")

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=8) as pool:
        list(pool.map(chop, jobs))
    print(f"8 processes: {time.perf_counter() - start:.1f} s")
