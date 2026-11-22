"""An AI agent's tool calls, one by one vs in parallel. The tools are simulated waits (1.0 s, 1.5 s, 2.0 s)."""
import asyncio
import time


async def call_tool(name, seconds):
    await asyncio.sleep(seconds)  # pretend the tool is busy
    return f"{name} ready"


tools = {"weather": 1.0, "calendar": 1.5, "web_search": 2.0}


async def agent(parallel):
    start = time.perf_counter()
    if parallel:
        await asyncio.gather(*(call_tool(n, s) for n, s in tools.items()))
    else:
        for n, s in tools.items():
            await call_tool(n, s)
    print("Parallel:  " if parallel else "One by one:", f"{time.perf_counter() - start:.1f} s")


async def main():
    await agent(parallel=False)
    await agent(parallel=True)


if __name__ == "__main__":
    asyncio.run(main())
