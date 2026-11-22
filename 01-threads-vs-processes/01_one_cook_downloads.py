"""One cook: 20 simulated downloads, one after another (about 20 s).
Each "download" is time.sleep(1) on your own machine: a stand-in for waiting on the network. No website is contacted."""
import time


def download(n):
    time.sleep(1)  # pretend: wait 1 second for the network
    return f"file {n} done"


if __name__ == "__main__":
    start = time.perf_counter()
    for n in range(1, 21):
        print(download(n))
    print(f"One cook: {time.perf_counter() - start:.1f} seconds")
