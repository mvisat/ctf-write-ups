#!/usr/bin/env python3

import string

# note: last hex digit (93) is removed
hexadecimal = "b7beaf929193989a999b949695979c9e9d9fb0b2b1b3b8bab9bbb4b6b5828183888a898b848685878c8e8d8fa0a2a1a3a8aaa9aba4a6a530323133383a393b3436"
charset = "{}_" + string.ascii_letters + string.digits
mapping = {}
for i in range(0, len(hexadecimal), 2):
    cur = hexadecimal[i:i+2]
    mapping[cur] = charset[i//2]

# note: last hex digit (bf) is substracted by 1 (be)
encoded = "82a386a3b7983198313b363293399232349892369a98323692989a313493913036929a303abe"
flag = []
for i in range(0, len(encoded), 2):
    cur = encoded[i:i+2]
    flag.append(mapping[cur])
print("".join(flag))