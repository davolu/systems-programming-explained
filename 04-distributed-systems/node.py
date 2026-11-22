import json, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

port, folder = int(sys.argv[1]), sys.argv[2]
disk = os.path.join(folder, f"node_{port}.json")   # this node's own disk
data = json.load(open(disk)) if os.path.exists(disk) else {}

class Node(BaseHTTPRequestHandler):
    def do_GET(self):                          # read: /order
        self.reply(data.get(self.path[1:]))
    def do_PUT(self):                          # write: [version, value]
        n = int(self.headers["Content-Length"])
        version, value = json.loads(self.rfile.read(n))
        key = self.path[1:]
        if version > data.get(key, [0])[0]:    # keep only newer versions
            data[key] = [version, value]
            json.dump(data, open(disk, "w"))
        self.reply("ok")
    def reply(self, obj):
        self.send_response(200); self.end_headers()
        self.wfile.write(json.dumps(obj).encode())
    def log_message(self, *args): pass         # keep the output quiet

HTTPServer(("127.0.0.1", port), Node).serve_forever()
