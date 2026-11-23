# Part 8: How Compression Works

Companion code for the video **"How Compression Works: DEFLATE, Huffman and LZ77 Explained"** from the *Systems Programming Explained* series by David Oluyale (Agentic AI Hub).

- Videos 1–5: https://youtu.be/dLdfrp02n6A · https://youtu.be/FL4Ts9LfBJk · https://youtu.be/2NCCn2o42EA · https://youtu.be/fni53-4dPGk · https://youtu.be/-l_xC6ECaoc
- Playlist: https://www.youtube.com/playlist?list=PLZaDePzkCIxo

## The ideas in everyday terms

- **Lossless:** unpack the exact clothes you put in. **Lossy:** leave the heavy shoes at home (a smaller photo).
- **Run-length:** write "5 apples" instead of "apple" five times.
- **LZ77:** instead of writing a phrase again, point back to where you already wrote it.
- **Huffman:** common letters get short codes, rare letters get long ones, like Morse code.
- **DEFLATE** (zip, gzip, PNG) is LZ77 plus Huffman. A codec is the pack and unpack pair.

## What's in here

| File | What it shows |
|---|---|
| `run_length.py` | Encodes a string with lots of repeats, then a sentence with almost no repeats. Decodes both back and compares a rough packed size |
| `pointers_and_codes.py` | Replaces the second "peanut butter" with a pointer `(offset, length)`, then builds Huffman codes for `SHE SELLS SEA SHELLS` |
| `deflate_real.py` | Uses Python's `zlib` (this is DEFLATE) on a 28,000-byte repeated log and on 28,000 random bytes. Prints sizes, ratios, times, and whether the original comes back |

Standard library only (Python 3.8+; `secrets` for the random file).

## Run it

```bash
cd 08-compression
python3 run_length.py
python3 pointers_and_codes.py
python3 deflate_real.py    # creates repeats.txt and random.bin
```

`repeats.txt` and `random.bin` are demo data, ignored by git.

## Observed results from the video

Recorded on 2026-11-23 at 11:48 WAT with CPython 3.13.5 on an 8-CPU Intel Xeon Linux cloud machine. Each result is one run of the exact code in this folder (see `recorded_outputs.json`).

| Demo | Result |
|---|---|
| `run_length.py` repeats `AAAAAABBBBCC` | length 12, packed size 6, decoded exactly |
| `run_length.py` `THE QUICK BROWN FOX` | length 19, packed size 38 (bigger), decoded exactly |
| `pointers_and_codes.py` | `peanut butter and <18,13> toast`, pointer `(18, 13)`, decoded exactly |
| Huffman frequencies | S 6, E 4, L 4, H 2, A 1 |
| Huffman codes | E `01`, L `10`, S `11`, A `000`, H `001` (common letters got 2 bits, rarer ones 3) |
| `deflate_real.py` `repeats.txt` | 28,000 → 94 bytes (0.003 of original), compress 0.23 ms, decompress 0.04 ms, match True |
| `deflate_real.py` `random.bin` | 28,000 → 28,016 bytes (1.001 of original), compress 0.43 ms, decompress 0.02 ms, match True |

## Notes and honest caveats

- `packed_size` for run-length is a rough "character plus digits of the count" size, not a real file format.
- The LZ77 demo only replaces one known repeated phrase. Real LZ77 searches a window for the best match.
- The Huffman tree is a miniature: it assigns shorter codes to more frequent letters. A real encoder also makes sure no short code is a prefix of a longer one, and then packs the bits into a file.
- **Always measure on your real data.** On this run, the repeated log shrank a lot, and the random file got slightly bigger. Both unpacked to the exact original (lossless).
- Times are from one run on this machine. Yours will differ.
- JPEG and MP3 are lossy cousins: they throw away some detail on purpose.
