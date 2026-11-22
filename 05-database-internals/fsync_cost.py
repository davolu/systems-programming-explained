import os, time

def append_many(n, sync):
    with open("fsync_test.log", "w") as f:
        t0 = time.perf_counter()
        for i in range(n):
            f.write(f"set key{i} {i}\n"); f.flush()
            if sync: os.fsync(f.fileno())   # wait until it's on disk
        return time.perf_counter() - t0

for sync in (False, True):
    secs = append_many(1000, sync)
    print(f"fsync={sync}: 1000 log writes in {secs * 1000:.0f} ms",
          f"({secs * 1e6 / 1000:.0f} µs each)")
