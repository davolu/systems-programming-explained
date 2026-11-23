import cProfile, pstats, io

N = 30_000

def count_in_list(n):
    xs = list(range(n))
    total = 0
    for i in range(n):
        if i in xs:                      # a list scan, every time
            total += 1
    return total

def count_in_set(n):
    xs = set(range(n))
    total = 0
    for i in range(n):
        if i in xs:                      # a set lookup, every time
            total += 1
    return total

def run(label, fn):
    t0 = __import__("time").perf_counter()
    result = fn(N)
    ms = (__import__("time").perf_counter() - t0) * 1000
    print(f"{label}: result={result} in {ms:.1f} ms")
    return ms

print("N =", N)
list_ms = run("count_in_list", count_in_list)
set_ms = run("count_in_set", count_in_set)

pr = cProfile.Profile()
pr.enable(); count_in_list(N); count_in_set(N); pr.disable()
stats = pstats.Stats(pr)
print("cProfile (separate run, time inside each function):")
for func, (_cc, _nc, tottime, _cum, _callers) in stats.stats.items():
    name = func[2]
    if name in ("count_in_list", "count_in_set"):
        print(f"  {name}: {tottime:.3f} s")
