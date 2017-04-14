#!/usr/bin/env python3
import os

mapping = {}
for i in range(256):
    with open('key', 'wb') as f:
        f.write(bytes([i]))
    assert os.system("./unbreakable") == 0
    with open('flag.enc', 'rb') as f:
        mapping[f.read()] = i

s = open('flag_encoded.enc', 'rb').read()
with open('flag', 'wb') as f:
    for i in range(0, len(s), 2):
        flip = True if (i // 2) % 2 == 0 else False
        cur = s[i:i+2]
        if flip:
            cur = cur[::-1]
        f.write(bytes([mapping[cur]]))
