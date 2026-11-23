# Part 7: Memory, Allocators, File Formats and Protocols

Companion code for the video **"Systems Programming Explained: Memory, Allocators, File Formats and Protocols"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Video 1: https://youtu.be/dLdfrp02n6A
- Video 2: https://youtu.be/FL4Ts9LfBJk
- Video 3: https://youtu.be/2NCCn2o42EA
- Video 4: https://youtu.be/fni53-4dPGk
- Video 5: https://youtu.be/-l_xC6ECaoc
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

- **Memory:** a wall of numbered lockers (addresses). The stack is a neat pile of trays. The heap is lockers you rent and must give back.
- **Allocator / arena:** the locker attendant. An arena pre-rents a whole row, hands out slices by bumping an offset, then frees the row at once by resetting the offset.
- **File format:** a labelled lunch box. A header says what is inside, then the payload follows in a fixed order.
- **Network protocol:** a phone script both sides agreed on, like REQUEST / RESPONSE.

## What's in here

| File | What it shows |
|---|---|
| `lunchbox.py` | Writes and reads a tiny binary format: magic `LBOX`, a 4-byte big-endian length, then a payload. Prints the raw bytes, the whole file as text, a correct read, and a rejected wrong magic |
| `arena.py` | A bump allocator on a `bytearray`. Times 50,000 allocations of 16 bytes against 50,000 separate `bytearray`s, then resets |
| `arena.c` | The same idea in C: a static buffer, an offset, `arena_alloc` and `arena_reset` |
| `protocol.py` | A short text protocol over a localhost socket: `REQUEST hello` / `RESPONSE hello`, with a threaded server |

`lunchbox.py` and `arena.py` are standard-library Python 3.8+. `protocol.py` uses `socket` and `threading`. `arena.c` needs `gcc`.

## Run it

```bash
cd 07-low-level-systems
python3 lunchbox.py      # creates note.lbox and bad.lbox
python3 arena.py
gcc -O0 -o arena_c arena.c && ./arena_c
python3 protocol.py
```

The `.lbox` files and `arena_c` are demo outputs. They're ignored by git.

## Observed results from the video

Recorded on 2026-11-23 at 11:49 WAT with CPython 3.13.5 on an 8-CPU Intel Xeon Linux cloud machine. The C demo was compiled with gcc `-O0`. Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `lunchbox.py` file bytes | `4c 42 4f 58 00 00 00 05 68 65 6c 6c 6f` (LBOX, length 5, hello) |
| `lunchbox.py` whole file as text | `'LBOX\x00\x00\x00\x05hello'` |
| `lunchbox.py` `read_box` | `b'hello'` |
| `lunchbox.py` wrong magic | `ValueError: bad magic: b'XXXX'` |
| `arena.py` | 50,000 blocks of 16 bytes: arena 30.5 ms (used 800,000 bytes); separate bytearrays 5.4 ms; after reset, used=0 |
| `arena.c` | `a at offset 0, b at offset 8, used 16`; after reset, used 0 |
| `protocol.py` | sent `REQUEST hello`; reply `RESPONSE hello`; parsed command=`RESPONSE`, body=`hello` |

## Notes and honest caveats

- **On this run, creating 50,000 separate Python bytearrays was faster (5.4 ms) than the arena (30.5 ms).** In Python, a small `bytearray` is already cheap, and this arena also builds a `memoryview` for every hand-out. The arena still wins on cleanup: one reset frees the whole row. We report the numbers we measured, not a promised speed-up. Your machine will differ.
- Real allocators are usually written in C. The C file is the same idea, not a production allocator (no alignment, no thread safety, no growth).
- The file format is a toy: no version field, no checksum, no streaming. The lesson is: always check the header.
- The protocol demo listens first, then accepts one connection on localhost. It is not a production server.
- `malloc`, PNG and WAV headers, HTTP and DNS are the real-world neighbours of these ideas.
