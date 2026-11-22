# Part 5: Write-Ahead Logs Explained

Companion code for the video **"How Databases Survive Crashes: Write-Ahead Logs and Recovery Explained"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Video 1: https://youtu.be/dLdfrp02n6A
- Video 2: https://youtu.be/FL4Ts9LfBJk
- Video 3: https://youtu.be/2NCCn2o42EA
- Video 4: https://youtu.be/fni53-4dPGk
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

Before you rearrange a bookshelf, you write each move in a diary. If the lights go out halfway, you read the diary from the top and finish the job.

- **Write-ahead log (WAL):** the diary. Write the change to the log first, make sure it's on disk, and only then change the real data.
- **Memory vs disk:** memory is your desk (fast, wiped by a crash). The disk is the filing cabinet (slower, survives).
- **Crash recovery:** after a restart, replay the log to rebuild the data.
- **Checksum:** a number made from each entry, so a torn or changed last entry is usually spotted.
- **Checkpoint:** a photo of the whole shelf. Recovery starts from the photo and replays only the entries after it.

## What's in here

| File | What it shows |
|---|---|
| `forget.py` | Two tiny key-value stores. Each runs in a child process that is crashed with `os._exit(1)`. The memory-only store comes back empty. The store that appends to `wal.log` (with `flush` + `os.fsync`) replays it and gets every value back |
| `torn_write.py` | A **simulated** torn write: two full entries, then only the first 12 characters of a third, then a crash. A naive replay crashes with `JSONDecodeError`. A replay that checks a CRC32 checksum and a trailing newline stops at the broken entry and keeps the good ones |
| `fsync_cost.py` | Times 1,000 small log appends with and without `os.fsync` after each one |
| `checkpoint.py` | Builds a 500,000-entry log, times a full replay, writes a checkpoint (data + log position), adds 1,000 more entries, then times recovery from the checkpoint and checks it matches a full replay |

Standard library only (Python 3.8+).

## Run it

```bash
cd 05-database-internals
python3 forget.py        # creates wal.log in this folder
python3 torn_write.py    # creates torn.log
python3 fsync_cost.py    # creates fsync_test.log
python3 checkpoint.py    # creates big.log (about 10 MB) and checkpoint.json
```

The `.log` files and `checkpoint.json` are demo data. They're ignored by git, and each script overwrites its own file on the next run.

## Observed results from the video

Recorded on 2026-11-23 at 00:01 WAT with CPython 3.13.5 on an 8-CPU Intel Xeon Linux cloud machine (ext4 on a virtual disk). Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `forget.py`, before the crash | both stores held `{'ada': 70, 'bob': 50}` |
| `forget.py`, `MemStore` after restart | exit code 1, `{}` (everything lost) |
| `forget.py`, `LogStore` after restart | exit code 1, `{'ada': 70, 'bob': 50}` (replayed from the log) |
| `torn_write.py`, end of the log | `'["bob", 50]\n1276601663 ['` (the third entry is cut off) |
| `torn_write.py`, naive replay | crashed with `JSONDecodeError` |
| `torn_write.py`, checked replay | kept 2 good entries: `{'ada': 100, 'bob': 50}` |
| `fsync_cost.py` | 1,000 writes: 1 ms without fsync (about 1 µs each), 80 ms with fsync (about 80 µs each) |
| `checkpoint.py` | full replay of 500,000 entries: 0.42 s; recovery from the checkpoint: 0.001 s; same result: True |

## Notes and honest caveats

- **These are process crashes, not power cuts.** `os._exit(1)` kills the program while the machine keeps running. Data the program had already handed to the operating system would usually survive that, even without `fsync`. A real power cut can lose anything that hasn't reached the disk, which is why `LogStore` calls `os.fsync` before it changes memory. This repo doesn't run a power-loss test.
- **The torn write is simulated** by writing part of an entry on purpose. Real torn writes depend on the disk and file system.
- **A CRC32 checksum catches accidental damage**, like a torn or garbled entry, almost always. It is not a security check against someone tampering with the file.
- **fsync timings depend heavily on the disk.** These numbers come from one cloud machine's virtual disk. Laptops, servers and network disks can be much faster or much slower, and some disks or virtual machines can report a write as saved before it truly is. Real databases often batch many changes into one fsync (group commit).
- **The checkpoint is a toy.** It isn't fsynced and isn't written atomically, and it is taken while no other writer is running. For crash safety, write it to a new file, fsync it, rename it into place, then fsync the folder, and keep the old log until all of that completes.
- **Log entries are "set this value" changes**, so replaying an entry twice is harmless (idempotent). Logs of "add 20" changes need extra care.
- **No transactions here.** Real databases also log commit records: after a crash, committed work is redone, and uncommitted work is undone or ignored.
- For real data, use a real database such as SQLite or PostgreSQL.
