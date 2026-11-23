def rle_encode(text):
    if not text:
        return []
    out, cur, n = [], text[0], 1
    for ch in text[1:]:
        if ch == cur:
            n += 1
        else:
            out.append((cur, n)); cur, n = ch, 1
    out.append((cur, n))
    return out

def rle_decode(pairs):
    return "".join(ch * n for ch, n in pairs)

def packed_size(pairs):
    # one character plus a count, as a rough "stored size"
    return sum(1 + len(str(n)) for ch, n in pairs)

repeats = "AAAAAABBBBCC"
pairs = rle_encode(repeats)
back = rle_decode(pairs)
print("original:", repeats, "len", len(repeats))
print("encoded:", pairs, "packed size", packed_size(pairs))
print("decoded:", back, "match", back == repeats)

randomish = "THE QUICK BROWN FOX"
pairs2 = rle_encode(randomish)
back2 = rle_decode(pairs2)
print("original:", randomish, "len", len(randomish))
print("encoded:", pairs2, "packed size", packed_size(pairs2))
print("decoded:", back2, "match", back2 == randomish,
      "bigger?" , packed_size(pairs2) > len(randomish))
