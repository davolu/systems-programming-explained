import struct

MAGIC = b"LBOX"                          # 4 bytes that say "this is our format"

def write_box(path, payload):
    with open(path, "wb") as f:
        f.write(MAGIC)
        f.write(struct.pack(">I", len(payload)))  # 4-byte length, big-endian
        f.write(payload)

def read_box(path):
    with open(path, "rb") as f:
        magic = f.read(4)
        if magic != MAGIC:
            raise ValueError(f"bad magic: {magic!r}")
        n = struct.unpack(">I", f.read(4))[0]
        payload = f.read(n)
        if len(payload) != n:
            raise ValueError("truncated payload")
        return payload

def hexdump(data):
    return " ".join(f"{b:02x}" for b in data)

payload = b"hello"
write_box("note.lbox", payload)
raw = open("note.lbox", "rb").read()
print("file bytes:", hexdump(raw))
print("whole file as text:", ascii(raw.decode("latin-1")))
print("read_box (uses the header):", read_box("note.lbox"))

# a file with the wrong magic must be rejected
open("bad.lbox", "wb").write(b"XXXX" + struct.pack(">I", 5) + b"hello")
try:
    read_box("bad.lbox")
except ValueError as e:
    print("wrong magic:", e)
