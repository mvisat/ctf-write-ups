#!/usr/bin/env python
from pwn import *
from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import RSA
import gmpy2

r = remote('66.172.27.77', 35156)
for _ in xrange(11):
  r.recvline()

r.sendline("F")
c1 = int(r.recvline())

r.sendline("S")
c2 = int(r.recvline())

r.sendline("P")
r.recvline()
s = r.recvuntil("-----END PUBLIC KEY-----\n")
pubkey = RSA.importKey(s)
n = pubkey.n
e = pubkey.e

def solve(n, e, c):
  ret = gmpy2.iroot(c, e)
  assert ret[1]
  return long_to_bytes(long(ret[0]))

otp1 = solve(n, e, c1)
otp2 = solve(n, e, c2)
# print otp1
# print otp2
r.sendline("G")
r.recvline()
r.sendline(otp1[-18:])
print r.recvline()
r.close()