"""asyncio: one thread, 20 simulated downloads at once (about 1 s)."""
import asyncio
import time


async def download_async(n):
    await asyncio.sleep(1)  # wait, but let others work meanwhile
    return f"file {n} done"


async def main():
    start = time.perf_counter()
    tasks = [download_async(n) for n in range(1, 21)]
    results = await asyncio.gather(*tasks)
    print(len(results), "files in", f"{time.perf_counter() - start:.1f} s, on 1 thread")


if __name__ == "__main__":
    asyncio.run(main())  # in a notebook (Colab/Jupyter) write: await main()
