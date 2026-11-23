import time
import numpy as np

N = 4_000
grid = np.arange(N * N, dtype=np.float64).reshape(N, N)

def sum_rows(a):
    total = 0.0
    for i in range(a.shape[0]):
        total += a[i, :].sum()           # walk along each row
    return total

def sum_cols(a):
    total = 0.0
    for j in range(a.shape[1]):
        total += a[:, j].sum()           # walk down each column
    return total

t0 = time.perf_counter(); row_total = sum_rows(grid); row_s = time.perf_counter() - t0
t0 = time.perf_counter(); col_total = sum_cols(grid); col_s = time.perf_counter() - t0
print(f"grid: {N} x {N}, dtype={grid.dtype}, C-order={grid.flags['C_CONTIGUOUS']}")
print(f"sum rows:    {row_s:.3f} s, total={row_total:.0f}")
print(f"sum columns: {col_s:.3f} s, total={col_total:.0f}")
print(f"same total: {row_total == col_total}")
