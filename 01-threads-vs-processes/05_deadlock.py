"""Deadlock: two cooks, two tools (locks), taken in opposite orders. A 2-second timeout stops the demo freezing forever.
The fix: always take locks in the same order."""
import threading
import time

knife, board = threading.Lock(), threading.Lock()


def cook(name, first, second):
    with first:                        # grab the first tool
        time.sleep(0.1)
        if second.acquire(timeout=2):  # wait at most 2 s for the other
            second.release()
            print(name, "finished")
        else:
            print(name, "is stuck: deadlock!")


def kitchen(a_tools, b_tools):
    a = threading.Thread(target=cook, args=("Cook A", *a_tools))
    b = threading.Thread(target=cook, args=("Cook B", *b_tools))
    a.start(); b.start(); a.join(); b.join()


if __name__ == "__main__":
    print("Opposite order:")
    kitchen((knife, board), (board, knife))
    print("Same order:")
    kitchen((knife, board), (knife, board))
