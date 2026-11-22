"""Many cooks: the same 20 simulated downloads with a ThreadPoolExecutor (about 1 s)."""
import time
from concurrent.futures import ThreadPoolExecutor


def download(n):
    time.sleep(1)  # pretend: wait 1 second for the network
    return f"file {n} done"


if __name__ == "__main__":
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(download, range(1, 21)))
    print(results[:3], "...")
    print(f"Many cooks: {time.perf_counter() - start:.1f} seconds")
