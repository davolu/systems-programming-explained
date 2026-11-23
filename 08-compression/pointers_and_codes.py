def lz_encode(text, phrase):
    first = text.find(phrase)
    second = text.find(phrase, first + 1)
    if first < 0 or second < 0:
        return text, None
    # replace the second copy with (offset, length)
    pointer = (second - first, len(phrase))
    encoded = text[:second] + f"<{pointer[0]},{pointer[1]}>" + text[second + len(phrase):]
    return encoded, pointer

def lz_decode(encoded, at, offset, length):
    # "at" is where the pointer sits in the encoded string
    phrase = encoded[at - offset:at - offset + length]
    end = encoded.find(">", at) + 1
    return encoded[:at] + phrase + encoded[end:]

text = "peanut butter and peanut butter toast"
encoded, pointer = lz_encode(text, "peanut butter")
print("original:", text)
print("encoded:", encoded, "pointer:", pointer)
at = encoded.find("<")
back = lz_decode(encoded, at, pointer[0], pointer[1])
print("decoded:", back, "match", back == text)

from collections import Counter
import heapq

sentence = "SHE SELLS SEA SHELLS"
freq = Counter(ch for ch in sentence if ch != " ")
print("frequencies:", dict(sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))))

def huffman_codes(freq):
    heap = [[n, [ch, ""]] for ch, n in freq.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        heap[0][1][1] = "0"
    while len(heap) > 1:
        lo, hi = heapq.heappop(heap), heapq.heappop(heap)
        for item in lo[1:]: item[1] = "0" + item[1]
        for item in hi[1:]: item[1] = "1" + item[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return dict(sorted(heap[0][1:], key=lambda x: (len(x[1]), x[0])))

codes = huffman_codes(freq)
print("codes:", codes)
