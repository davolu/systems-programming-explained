import os, time, zlib, secrets

# lots of repetition, like a log file
repeats = ("user login ok\n" * 2000).encode()
# random bytes, already disordered
random_bytes = secrets.token_bytes(len(repeats))

open("repeats.txt", "wb").write(repeats)
open("random.bin", "wb").write(random_bytes)
print("both files start at", len(repeats), "bytes")

def measure(path):
    data = open(path, "rb").read()
    t0 = time.perf_counter(); compact = zlib.compress(data); c_ms = (time.perf_counter() - t0) * 1000
    t0 = time.perf_counter(); back = zlib.decompress(compact); d_ms = (time.perf_counter() - t0) * 1000
    ratio = len(compact) / len(data)
    print(f"{path}: {len(data)} -> {len(compact)} bytes",
          f"({ratio:.3f} of original),",
          f"compress {c_ms:.2f} ms, decompress {d_ms:.2f} ms,",
          f"match {back == data}")

measure("repeats.txt")
measure("random.bin")
