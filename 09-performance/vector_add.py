import time
import numpy as np

N = 2_000_000
left = list(range(N))
right = list(range(N, 2 * N))
a = np.array(left, dtype=np.int64)
b = np.array(right, dtype=np.int64)

t0 = time.perf_counter()
looped = [left[i] + right[i] for i in range(N)]
loop_s = time.perf_counter() - t0

t0 = time.perf_counter()
vectored = a + b
vec_s = time.perf_counter() - t0

print(f"N = {N}")
print(f"Python loop: {loop_s:.3f} s, first three {looped[:3]}")
print(f"NumPy add:   {vec_s:.3f} s, first three {vectored[:3]}")
print("same result:", looped[0] == int(vectored[0]) and looped[-1] == int(vectored[-1]))
