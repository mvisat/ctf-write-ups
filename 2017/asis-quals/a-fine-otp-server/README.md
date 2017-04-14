# A Fine OTP Server
```
Points: 79
Solves: 74
Category: Crypto
Description: Connect to OTP generator server, and try to find one OTP.

$ nc 66.172.27.77 35156
|-------------------------------------|
| Welcome to the S3cure OTP Generator |
|-------------------------------------|
| Guess the OTP and get the nice flag!|
| Options:
	[F]irst encrypted OTP
	[S]econd encrypted OTP
	[G]uess the OTP
	[P]ublic key
	[E]ncryption function
	[Q]uit
F
13424849164527521403756445050870196571038349263738328860728317613249912394547060932323343839684520029298203039106900245311207700034998334716959150347732399830523999713642280162830272139002574817592090449659747011744703476809634972932424650521403852280849375862898949701206176647643528687979687920144374964064784133996196090800036156410968651004203824246943296894828553683000484465761352121637534235125088628796273443211696022861160713124901769694940627663466248809007143330654429895400868446639764335437622070240622232138022096764419001816584077426696752932340875
S
13424849164527521403756445050870196571038349263738328860728317613249912394547060932323343839684520029298203039106900245311207700034998334716959149454550557367264230052801518249153148576223898059366636342780811732574735190112604137979705287967095665948621318436322902754115719508431451778710511528511691658414603904398970686628940939503906710237649395483385082258030982314713064151686703819098208241404962938693167811749402813532948002084723706574749907947111793811458272999022599048315033569702955244664197018184891481021879557971902494057679784811053218015784448
P
the public key is:
-----BEGIN PUBLIC KEY-----
MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEAqiRs5K+mdZirr0Bl/M5c
2vREBH8I+A6LwzHiArNB0hG6joECEA5oM7xPb78kIIsOLH6ABSEgbo9AVY819qSn
SUXsLlZzZ0Sw7E47q0moN8uYiI1YPHqvem/2GKzRjogGtECxpNaff0VTLQNtPaVo
57Ed/JzOI7tgLWKAWZPueiDUfcoVMgpGV9vIMg13efJg+W+2G7t5zsWKVi3xgH2j
zdFftDdSco0FXT3aU7r5jUF5oTQDEI7/Zktva8vV5cYW+oHJ7VChlRI84owSngx0
+Y7+GSSlv4qcWDdQA8C2BcUSBp1BOWGAb0i1yk4smB7r4M0B89Ny0ixd3ImAy8bY
9wIBAw==
-----END PUBLIC KEY-----
E
def gen_otps():
  template_phrase = 'Welcome, dear customer, the secret passphrase for today is: '

  OTP_1 = template_phrase + gen_passphrase(18)
  OTP_2 = template_phrase + gen_passphrase(18)

  otp_1 = bytes_to_long(OTP_1)
  otp_2 = bytes_to_long(OTP_2)

  nbit, e = 2048, 3
  privkey = RSA.generate(nbit, e = e)
  pubkey  = privkey.publickey().exportKey()
  n = getattr(privkey.key, 'n')

  r = otp_2 - otp_1
  if r < 0:
      r = -r
  IMP = n - r**(e**2)
  if IMP > 0:
  	c_1 = pow(otp_1, e, n)
  	c_2 = pow(otp_2, e, n)
  return pubkey, OTP_1[-18:], OTP_2[-18:], c_1, c_2

G
Send me the otp :)
1
Sorry, try again later :|
```

## English
TODO

## Bahasa Indonesia
Jika kita lakukan perhitungan, `otp_1 ^ 3 < n`. Dengan begitu, kita hanya perlu mencari akar 3 dari `c_1` saja dan tidak memerlukan modulusnya.

```python
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
```
Flag: `ASIS{0f4ae19fefbb44b37f9012b561698d19}`
