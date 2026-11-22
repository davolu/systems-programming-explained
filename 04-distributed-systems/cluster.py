import json, subprocess, sys, tempfile, time, urllib.request

PORTS = [8001, 8002, 8003]
folder = tempfile.mkdtemp()      # a fresh folder for the nodes' disks

def start(port):
    node = subprocess.Popen([sys.executable, "node.py", str(port), folder])
    time.sleep(0.5)              # give it a moment to start
    return node

def send(port, method, key, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"http://127.0.0.1:{port}/{key}",
                                 data=data, method=method)
    try:
        with urllib.request.urlopen(req, timeout=0.5) as r:
            return json.loads(r.read())
    except OSError:              # refused or timed out: no answer
        return "no answer"

version = 0

def write(key, value):
    global version
    version += 1
    t0 = time.perf_counter()
    acks = sum(send(p, "PUT", key, [version, value]) == "ok" for p in PORTS)
    ok = "OK" if acks >= 2 else "FAILED"   # a majority must accept it
    print(f"write {value}: {acks}/3 acks -> {ok}",
          f"({time.perf_counter() - t0:.2f} s)")

def read(port, key):
    return send(port, "GET", key)

def majority_read(key):
    answers = [read(p, key) for p in PORTS]
    answers = [a for a in answers if a != "no answer"]
    return max(answers) if len(answers) >= 2 else "FAILED"

nodes = {p: start(p) for p in PORTS}
write("order", "pizza")

nodes[8003].terminate(); nodes[8003].wait()     # node 3 goes dark
write("order", "sushi")

nodes[8003] = start(8003)                       # node 3 comes back
print("node 3 says:   ", read(8003, "order"))
print("majority says: ", majority_read("order"))
send(8003, "PUT", "order", majority_read("order"))   # catch up
print("node 3 now:    ", read(8003, "order"))

for p in (8002, 8003): nodes[p].terminate(); nodes[p].wait()
write("order", "tacos")                         # only node 1 is left
nodes[8001].terminate()
