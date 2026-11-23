import time

class Arena:
    def __init__(self, size):
        self.buf = bytearray(size)       # one rented row of lockers
        self.off = 0
    def alloc(self, n):
        if self.off + n > len(self.buf):
            raise MemoryError("arena full")
        start = self.off
        self.off += n                    # bump the offset
        return memoryview(self.buf)[start:start + n]
    def reset(self):
        self.off = 0                     # free the whole row at once

N, SIZE = 50_000, 16

t0 = time.perf_counter()
arena = Arena(N * SIZE)
slices = [arena.alloc(SIZE) for _ in range(N)]
arena_ms = (time.perf_counter() - t0) * 1000
print(f"arena: {N} blocks of {SIZE} bytes in {arena_ms:.1f} ms, used={arena.off}")

t0 = time.perf_counter()
many = [bytearray(SIZE) for _ in range(N)]
many_ms = (time.perf_counter() - t0) * 1000
print(f"separate bytearrays: {N} blocks in {many_ms:.1f} ms")

arena.reset()
print(f"after reset, used={arena.off} (the row is free again)")
print(f"sanity: first arena block is {len(slices[0])} bytes,",
      f"first separate block is {len(many[0])} bytes")
