import json, os, multiprocessing as mp

LOG = "wal.log"

class MemStore:                        # keeps data only in memory
    def __init__(self): self.data = {}
    def set(self, key, value): self.data[key] = value

class LogStore(MemStore):              # diary first, then memory
    def __init__(self):
        super().__init__()
        if os.path.exists(LOG):        # restart: replay the diary
            for line in open(LOG):
                key, value = json.loads(line)
                self.data[key] = value
    def set(self, key, value):
        with open(LOG, "a") as f:
            f.write(json.dumps([key, value]) + "\n")
            f.flush(); os.fsync(f.fileno())   # make sure it's on disk
        self.data[key] = value

def session(store_class):
    s = store_class()
    s.set("ada", 100); s.set("bob", 50); s.set("ada", 70)
    print(f"  before crash: {s.data}", flush=True)
    os._exit(1)                        # crash: no goodbye, no cleanup

open(LOG, "w").close()                 # start with an empty diary
for store_class in (MemStore, LogStore):
    p = mp.Process(target=session, args=(store_class,))
    p.start(); p.join()
    print(f"{store_class.__name__}: exit code {p.exitcode},",
          f"after restart: {store_class().data}")
