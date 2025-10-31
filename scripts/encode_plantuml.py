#!/usr/bin/env python3
# Reads PlantUML text from stdin and prints the PlantUML DEFLATE-based token
import sys, zlib

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def encode64(data: bytes) -> str:
    res = []
    i = 0
    n = len(data)
    while i < n:
        b1 = data[i]
        b2 = data[i+1] if i+1 < n else 0
        b3 = data[i+2] if i+2 < n else 0
        c1 = (b1 >> 2) & 0x3F
        c2 = ((b1 & 0x3) << 4) | ((b2 >> 4) & 0xF)
        c3 = ((b2 & 0xF) << 2) | ((b3 >> 6) & 0x3)
        c4 = b3 & 0x3F
        res.append(ALPHABET[c1])
        res.append(ALPHABET[c2])
        res.append(ALPHABET[c3])
        res.append(ALPHABET[c4])
        i += 3
    return ''.join(res)

def plantuml_token(text: str) -> str:
    # raw deflate (no zlib header) -> plantuml encoding
    compressor = zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)
    compressed = compressor.compress(text.encode('utf-8')) + compressor.flush()
    return encode64(compressed)

if __name__ == "__main__":
    data = sys.stdin.read()
    print(plantuml_token(data))
