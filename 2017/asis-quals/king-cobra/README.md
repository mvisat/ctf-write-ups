# King Cobra
```
Points: 128
Solves: 55
Category: Reverse
Description: King Cobra can swallows her victim like Python, do you want to test it?

$ file king_cobra
king_cobra: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=373ec5dee826653796e927ac3d65c9a8ec7db9da, stripped

$ ./king_cobra
Oops, do you know the usage?!
```

## English
TODO

## Bahasa Indonesia
Kita coba lakukan command `strings`, untuk melihat apakah ada string yang menarik.

```shell
$ strings king_cobra
...snip...
breadline.so
bresource.so
xflag.enc
xgpl-2.0.txt
zout00-PYZ.pyz
libpython2.7.so.1.0
...snip...
.comment
pydata
```

Terdapat string menarik `flag.enc`, dan `pyz`. Dengan googling, ternyata `pyz` adalah Python zipped executable file yang salah satunya dibuat oleh [PyInstaller](https://github.com/pyinstaller/pyinstaller "PyInstaller"). PyInstaller juga menyediakan program `archive_viewer` untuk melihat dan mengekstrak file yang terdapat pada *executable*-nya.

```
$ pyinstaller/archive_viewer.py king_cobra
 pos, length, uncompressed, iscompressed, type, name
[(0, 158, 185, 1, 'm', u'pyimod00_crypto_key'),
 (158, 171, 237, 1, 'm', u'struct'),
 (329, 1139, 2543, 1, 'm', u'pyimod01_os_path'),
 (1468, 4201, 11252, 1, 'm', u'pyimod02_archive'),
 (5669, 6009, 18151, 1, 'm', u'pyimod03_importers'),
 (11678, 1572, 4254, 1, 's', u'pyiboot01_bootstrap'),
 (13250, 468, 726, 1, 's', u'reverse_1.1'),
...snip...
 (3149187, 7003, 7265, 1, 'x', u'flag.enc'),
 (3156190, 6812, 18092, 1, 'x', u'gpl-2.0.txt'),
 (3163002, 647390, 647390, 0, 'z', u'out00-PYZ.pyz')]
? help
U: go Up one level
O <name>: open embedded archive name
X <name>: extract name
Q: quit
? X flag.enc
to filename? flag.enc
? X reverse_1.1
to filename? reverse_1.1
? Q
```

File apakah reverse_1.1 tersebut?

```
$ file reverse_1.1
reverse_1.1: data

$ strings reverse_1.1
...
reverse_1.1.pyt
encode
Oops, do you know the usage?!i
flag.enct
your encoded file is ready :Ps$
huh?!, what do you mean by this arg?N(
sysR
lent
opent
readR
writet
close(
reverse_1.1.pyt
<module>
```

Sepertinya file tersebut adalah python yang telah dicompile, `pyc` yang telah dihilangkan *magic number* dan *timestamp*-nya (total 8 byte). Kita perbaiki file tersebut dan *decompile* dengan  [uncompyle6](https://pypi.python.org/pypi/uncompyle6).

```shell
$ printf "\x03\xf3\x0d\x0a\x00\x00\x00\x00" | cat - reverse_1.1 > reverse_1.1.pyc

$ uncompyle6 reverse_1.1.pyc > reverse_1.1.py
```

Hasilnya kode berikut.

```python
# uncompyle6 version 2.9.10
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.12 (default, Nov 19 2016, 06:48:10)
# [GCC 5.4.0 20160609]
# Embedded file name: reverse_1.1.py
from sys import argv

def encode(data):
    res = ''
    for b in data:
        res += chr((ord(b) & 15) << 4 | (ord(b) & 240) >> 4)

    return res


if len(argv) < 2:
    print 'Oops, do you know the usage?!'
else:
    try:
        data = open(argv[1], 'r').read()
        f = open('flag.enc', 'w')
        f.write(encode(data))
        f.close()
        print 'your encoded file is ready :P'
    except:
        print 'huh?!, what do you mean by this arg?'
# okay decompiling reverse_1.1.pyc
```

Jika kita perhatikan kode python tersebut, untuk melakukan `decode` dapat dengan cara melakukan `encode` kembali. Hal itu disebabkan `encode` hanya menggeser 4 bit terkecil ke paling besar dan sebaliknya.

```shell
$ python reverse_1.1.py flag.enc
your encoded file is ready :P
```

File `flag.enc` sekarang merupakan PNG yang berisi flag: `ASIS{20a87eb1e30361e19ef48940f9573fe3}`
