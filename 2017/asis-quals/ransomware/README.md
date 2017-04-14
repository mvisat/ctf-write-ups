# Ransomware
```
Points: 199
Solves: 27
Category: Reverse
Description: One of my very important files has been locked by a ransomware, please help me to get it again!

$ file ransomware
ransomware: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=d4d80f5a2c919caa0baa9d987c70dcd6716283f3, not stripped
```

## English
TODO

## Bahasa Indonesia
Buka dengan IDA untuk mendapatkan pseudocode.

```c
signed __int64 Dmain() {
...
  if ( D3std4file15__T6existsTAyaZ6existsFNbNiNfAyaZb(15LL, "important_files") ^ 1 ) {
    result = 0xFFFFFFFFLL;
  } else {
    D3std4file10dirEntriesFAyaE3std4file8SpanModebZS3std4file11DirIterator(&v8, 1LL, 0LL, 15LL, "important_files");
    while ( D3std4file11DirIterator5emptyMFNdZb(&v8) ^ 1 ) {
      LODWORD(v1) = D3std4file11DirIterator5frontMFNdZS3std4file8DirEntry(&v8, &v9);
      LODWORD(v2) = D3std4file8DirEntry4nameMxFNaNbNdZAya(v1);
      v6 = v2;
      v7 = v3;
      if ( D3std4file15__T6isFileTAyaZ6isFileFNdNfAyaZb(v2, v3) ) {
        LODWORD(v4) = d_arraycatT(&D12TypeInfo_Aya6__initZ, v6, v7, 7LL, ".locked");
        D8ransom1112encrypt_fileFAyaAyaZv(v4, v5, v6, v7);
      }
...
}
```

Karena nama fungsi banyak yang diawali dengan karakter D, kita dapat berasumsi kalau program tersebut ditulis dalam [bahasa pemrograman D](https://dlang.org/). Program tersebut mencari semua file yang ada dalam folder `important_files`, lalu melakukan enkripsi file tersebut ke file dengan namanya ditambah `.locked`. Bagaimana dengan alur enkripsinya?

```c
int __fastcall D8ransom1112encrypt_fileFAyaAyaZv(__int64 a1, __int64 a2, __int64 a3, __int64 a4) {
  v26 = a1;
  v27 = a2;
  v28 = a3;
  v29 = a4;
  LODWORD(v4) = D3std4file13__T4readTAyaZ4readFNfAyamZAv(8LL, a3, a4);
  v19 = v4;
  v20 = v5;
  if ( v4 != 8 || (result = 0, memcmp(v20, "_LOCKED_", 8uLL)) )
  {
    LODWORD(v7) = D3std4file13__T4readTAyaZ4readFNfAyamZAv(-1LL, v28, v29);
    v17 = v7;
    v18 = v8;
    v9 = v7;
    if ( v7 & 3 )
      d_arraysetlengthT(&D11TypeInfo_Ah6__initZ, v17 + 4 - (v17 & 3), &v17);
    v21 = 0LL;
    v22 = 0LL;
    v23 = 0LL;
    D3std5stdio4File6__ctorMFNcNfAyaxAaZS3std5stdio4File(&v21, 2LL, "wb", v26, v27);
    D3std5stdio4File15__T8rawWriteTaZ8rawWriteMFNfxAaZv(&v21, 8LL, "_LOCKED_");
    LODWORD(v10) = d_arrayliteralTX(&D12TypeInfo_xAk6__initZ, 1LL);
    *v10 = v9;
    LODWORD(v11) = D3std5stdio4File15__T8rawWriteTkZ8rawWriteMFNfxAkZv(&v21, 1LL, v10);
    *(&D8ransom117key_idxi + v11) = 0x5E31BC3;
    v12 = 0LL;
    v13 = v17 >> 2;
    if ( v17 >> 2 )
    {
      do
      {
        LODWORD(v14) = d_arrayliteralTX(&D12TypeInfo_xAk6__initZ, 1LL);
        v15 = v14;
        LODWORD(v16) = D3std8bitmanip36__T4readTkVE3std6system6Endiani1TAhZ4readFNaNbNiNfKAhZk(&v17);
        *v15 = D8ransom1117encrypt_16_roundsFkZk(v16);
        D3std5stdio4File15__T8rawWriteTkZ8rawWriteMFNfxAkZv(&v21, 1LL, v15);
        ++v12;
      }
      while ( v12 < v13 );
    }
    D3std5stdio4File5closeMFNeZv(&v21);
    D3std4file15__T6removeTAyaZ6removeFNfAyaZv(v28, v29);
    v25 = 4;
    result = D3std5stdio4File6__dtorMFNfZv(&v21);
    if ( !v25 )
      _Unwind_Resume(v24);
  }
  return result;
}
```

Alur fungsi `encrypt_file` secara kasar seperti ini:
1. Baca 8 byte pertama file `input`. Jika ukuran file kurang dari 8 byte atau byte yang terbaca adalah string `_LOCKED_`, keluar dari fungsi.
2. Baca semua isi file `input` ke array `v7`.
3. Jika panjang `v7` bukan kelipatan 4, perpanjang array hingga kelipatan 4 dengan *null bytes*.
4. Tulis string `_LOCKED_` ke file `output`.
5. Tulis ukuran file `input` ke file `output`.
5. Isi variable `ransom_key` dengan `0x5E31BC3`.
6. Looping hingga `v7` habis:
  1. Baca array `v7` sebanyak 4 byte.
  2. Panggil fungsi `encrypt_16_rounds`.
  3. Tulis ke file `output`.

Yang terlihat rumit di sini adalah fungsi `encrypt_16_rounds` dan `encrypt_one_round`.

```c
int64 D8ransom1117encrypt_16_roundsFkZk@<rax>(__int64 a1@<rax>, int a2@<edi> {
  v2 = *(&D8ransom117key_idxi + a1) ^ a2;
  v3 = 0;
  do {
    LODWORD(result) = D8ransom1117encrypt_one_roundFkZk(v2);
    v2 = result;
    ++v3;
  }
  while ( v3 < 0x10 );
  *(&D8ransom117key_idxi + result) = result;
  return result;
}

int64 D8ransom1117encrypt_one_roundFkZk@<rax>(__int64 a1@<rax>, unsigned int a2@<edi>) {
  v2 = *(&D8ransom117key_idxi + a1) - 3;
  if ( v2 >= D8ransom113keyyAa )
    D8ransom117__arrayZ(36LL);
  v8 = *(*(&D8ransom113keyyAa + 1) + v2) << 24;
  v3 = *(&D8ransom117key_idxi + v2) - 2;
  if ( v3 >= D8ransom113keyyAa )
    D8ransom117__arrayZ(36LL);
  v9 = (*(*(&D8ransom113keyyAa + 1) + v3) << 16) | v8;
  v4 = *(&D8ransom117key_idxi + v3) - 1;
  if ( v4 >= D8ransom113keyyAa )
    D8ransom117__arrayZ(36LL);
  v5 = *(&D8ransom117key_idxi + v4);
  if ( v5 >= D8ransom113keyyAa )
    D8ransom117__arrayZ(36LL);
  v10 = *(*(&D8ransom113keyyAa + 1) + v5) | (*(*(&D8ransom113keyyAa + 1) + v4) << 8) | v9;
  ++*(&D8ransom113keyyAa + 0x1C482C);
  v6 = *(&D8ransom117key_idxi + (&D8ransom113keyyAa + 0x7120B0));
  if ( v6 == D8ransom113keyyAa )
    *(&D8ransom117key_idxi + v6) = 3;
  return v10 ^ D8ransom1112rotate_rightFNakZk(D8ransom115suboxyG256h[a2] | (D8ransom115suboxyG256h[a2 >> 8] << 8) | (D8ransom115suboxyG256h[(a2 >> 16) & 0xFF] << 16) | (D8ransom115suboxyG256h[a2 >> 24] << 24));
}

int64 D8ransom1112rotate_rightFNakZk(unsigned int a1) {
  return (a1 << 31) | (a1 >> 1);
}
```
Fungsi `encrypt_16_rounds` sederhana: melakukan xor input dengan `ransom_key`, memanggil fungsi `encrypt_one_round` sebanyak 16 kali, lalu menyimpannya kembali hasilnya ke `ransom_key`.

Pada fungsi `encrypt_one_round`, IDA tidak terlalu sempurna melakukan dekompilasi dan membuat bingung, sehingga saya terpaksa melakukan **dekompilasi manual** dengan GDB untuk memperjelas alur fungsi. Lalu saya terjemahkan ke bahasa python agar lebih mudah dibaca. Kira-kira seperti ini kodenya.

```python
#!/usr/bin/env python3
ransom_key = 0x5E31BC3
internal = [0x59, 0x5e, 0x78, 0x2e, 0x47, 0x20, 0x85, 0xe1, 0x6c, 0x60, 0xa6, 0xdf, 0xb2, 0x77, 0xc, 0x78, 0x6a, 0xdf, 0x92]
sbox = [0x21, 0x10, 0x1a, 0xe6, 0x15, 0xc8, 0xc5, 0x44, 0x96, 0xa0, 0x5d, 0xc7, 0xb8, 0xae, 0x55, 0x30, 0x1f, 0x4, 0xfc, 0x1b, 0xfe, 0xc4, 0x35, 0xef, 0xd1, 0x77, 0x43, 0x61, 0xc9, 0x9b, 0xe5, 0xa3, 0xc, 0x40, 0x2f, 0xc0, 0xcf, 0x4d, 0xe7, 0xb0, 0x70, 0xd4, 0xfb, 0x6c, 0x88, 0xc1, 0x16, 0x65, 0xe9, 0x36, 0x80, 0x51, 0x53, 0xa, 0xa2, 0xea, 0xdb, 0x5, 0x1, 0xb, 0x8d, 0x4a, 0x68, 0x47, 0x25, 0x99, 0x2, 0xc6, 0xe0, 0x2b, 0x2d, 0x73, 0xf3, 0xfa, 0x27, 0x7e, 0xbb, 0xca, 0x6, 0xa4, 0xf9, 0x98, 0x97, 0xb5, 0x9, 0x12, 0xe, 0x4f, 0x14, 0xfd, 0x41, 0xf7, 0x83, 0x6d, 0x52, 0x7, 0x75, 0x93, 0x74, 0x6f, 0x5a, 0xb1, 0xad, 0x28, 0x31, 0x18, 0x69, 0xa7, 0x3f, 0x48, 0xf1, 0x81, 0x85, 0x92, 0xdd, 0x3e, 0x3a, 0xe8, 0xc3, 0x34, 0xf4, 0x7f, 0x57, 0x62, 0x3b, 0xa8, 0xbe, 0xbc, 0xd7, 0xaa, 0xcc, 0xa5, 0xba, 0xab, 0xde, 0xaf, 0x8b, 0xe3, 0x58, 0x1e, 0x3d, 0x4b, 0xd3, 0xa1, 0x19, 0x84, 0x23, 0x95, 0xdc, 0xeb, 0x32, 0x9e, 0x72, 0x5c, 0x46, 0xa9, 0x5f, 0xee, 0x89, 0x1c, 0x49, 0x9d, 0x6b, 0x5e, 0x9f, 0x3c, 0x7d, 0x4e, 0xcd, 0x13, 0x2c, 0x2e, 0x56, 0x7a, 0xf2, 0xe1, 0xd6, 0x79, 0x8a, 0x63, 0x9c, 0x54, 0xda, 0x20, 0xd, 0x76, 0xdf, 0xc2, 0xec, 0x50, 0xd0, 0x38, 0x67, 0xe4, 0xb2, 0x0, 0xb7, 0x8c, 0xf0, 0x5b, 0x82, 0x59, 0xe2, 0xac, 0xd9, 0xd2, 0x8, 0x6a, 0x45, 0xbf, 0xd8, 0x94, 0x4c, 0x17, 0x8e, 0x7b, 0xf8, 0xce, 0x42, 0x39, 0x29, 0x2a, 0xbd, 0xf, 0x66, 0x22, 0x3, 0x6e, 0x1d, 0x60, 0x8f, 0x26, 0xf6, 0x37, 0x11, 0xb4, 0x9a, 0x91, 0xed, 0x64, 0x7c, 0x90, 0xb9, 0xb3, 0xb6, 0xf5, 0xcb, 0x86, 0x87, 0x33, 0x78, 0x24, 0xa6, 0xd5, 0x71, 0xff]

def encrypt_16_rounds(x):
  global ransom_key
  ret = x ^ ransom_key
  for i in range(16):
    ret = encrypt_one_round(ret, i)
  ransom_key = ret
  return ret

def encrypt_one_round(x, idx):
  ret = internal[idx] << 24
  ret |= internal[idx+1] << 16
  ret |= internal[idx+2] << 8
  ret |= internal[idx+3]

  tmp = sbox[x & 0xff]
  tmp |= sbox[(x >> 8) & 0xff] << 8
  tmp |= sbox[(x >> 16) & 0xff] << 16
  tmp |= sbox[(x >> 24) & 0xff] << 24
  return ret ^ rotate_right(tmp)

def rotate_right(x):
  return ((x << 31) | (x >> 1)) & 0xffffffff
```

Lalu bagaimana dengan fungsi dekripsinya? Balikkan saja semua *logic* fungsi enkripsi, mulai dari alurnya, `sbox` untuk dekripsi, hingga manipulasi bit `rotate_right` menjadi `rotate_left`. Berikut kode lengkapnya.

```python
#!/usr/bin/env python3
import struct

ransom_key = 0x5E31BC3
internal = [0x59, 0x5e, 0x78, 0x2e, 0x47, 0x20, 0x85, 0xe1, 0x6c, 0x60, 0xa6, 0xdf, 0xb2, 0x77, 0xc, 0x78, 0x6a, 0xdf, 0x92]
sbox = [0x21, 0x10, 0x1a, 0xe6, 0x15, 0xc8, 0xc5, 0x44, 0x96, 0xa0, 0x5d, 0xc7, 0xb8, 0xae, 0x55, 0x30, 0x1f, 0x4, 0xfc, 0x1b, 0xfe, 0xc4, 0x35, 0xef, 0xd1, 0x77, 0x43, 0x61, 0xc9, 0x9b, 0xe5, 0xa3, 0xc, 0x40, 0x2f, 0xc0, 0xcf, 0x4d, 0xe7, 0xb0, 0x70, 0xd4, 0xfb, 0x6c, 0x88, 0xc1, 0x16, 0x65, 0xe9, 0x36, 0x80, 0x51, 0x53, 0xa, 0xa2, 0xea, 0xdb, 0x5, 0x1, 0xb, 0x8d, 0x4a, 0x68, 0x47, 0x25, 0x99, 0x2, 0xc6, 0xe0, 0x2b, 0x2d, 0x73, 0xf3, 0xfa, 0x27, 0x7e, 0xbb, 0xca, 0x6, 0xa4, 0xf9, 0x98, 0x97, 0xb5, 0x9, 0x12, 0xe, 0x4f, 0x14, 0xfd, 0x41, 0xf7, 0x83, 0x6d, 0x52, 0x7, 0x75, 0x93, 0x74, 0x6f, 0x5a, 0xb1, 0xad, 0x28, 0x31, 0x18, 0x69, 0xa7, 0x3f, 0x48, 0xf1, 0x81, 0x85, 0x92, 0xdd, 0x3e, 0x3a, 0xe8, 0xc3, 0x34, 0xf4, 0x7f, 0x57, 0x62, 0x3b, 0xa8, 0xbe, 0xbc, 0xd7, 0xaa, 0xcc, 0xa5, 0xba, 0xab, 0xde, 0xaf, 0x8b, 0xe3, 0x58, 0x1e, 0x3d, 0x4b, 0xd3, 0xa1, 0x19, 0x84, 0x23, 0x95, 0xdc, 0xeb, 0x32, 0x9e, 0x72, 0x5c, 0x46, 0xa9, 0x5f, 0xee, 0x89, 0x1c, 0x49, 0x9d, 0x6b, 0x5e, 0x9f, 0x3c, 0x7d, 0x4e, 0xcd, 0x13, 0x2c, 0x2e, 0x56, 0x7a, 0xf2, 0xe1, 0xd6, 0x79, 0x8a, 0x63, 0x9c, 0x54, 0xda, 0x20, 0xd, 0x76, 0xdf, 0xc2, 0xec, 0x50, 0xd0, 0x38, 0x67, 0xe4, 0xb2, 0x0, 0xb7, 0x8c, 0xf0, 0x5b, 0x82, 0x59, 0xe2, 0xac, 0xd9, 0xd2, 0x8, 0x6a, 0x45, 0xbf, 0xd8, 0x94, 0x4c, 0x17, 0x8e, 0x7b, 0xf8, 0xce, 0x42, 0x39, 0x29, 0x2a, 0xbd, 0xf, 0x66, 0x22, 0x3, 0x6e, 0x1d, 0x60, 0x8f, 0x26, 0xf6, 0x37, 0x11, 0xb4, 0x9a, 0x91, 0xed, 0x64, 0x7c, 0x90, 0xb9, 0xb3, 0xb6, 0xf5, 0xcb, 0x86, 0x87, 0x33, 0x78, 0x24, 0xa6, 0xd5, 0x71, 0xff]

# build sbox for decryption
sbox_decrypt = [0] * len(sbox)
for i in range(len(sbox)):
  sbox_decrypt[sbox[i]] = i

def decrypt_file(name):
  assert name.endswith('.locked')

  with open(name, 'rb') as f:
    s = f.read()

  assert len(s) % 4 == 0
  assert s[:8] == b'_LOCKED_'
  s = s[8:]

  file_len = s[:4]
  file_len = struct.unpack('<I', file_len)[0]
  s = s[4:]

  with open(name.rstrip('.locked'), 'wb') as f:
    for i in range(0, file_len, 4):
      cur = s[i:i+4]
      cur = struct.unpack('<I', cur)[0]

      dec = decrypt_16_rounds(cur)
      f.write(struct.pack('<I', dec))

def decrypt_16_rounds(x):
  global ransom_key
  key = ransom_key
  ret = x
  for i in range(15, -1, -1):
    ret = decrypt_one_round(ret, i)
  ransom_key = x
  return ret ^ key

def decrypt_one_round(x, idx):
  tmp = internal[idx] << 24
  tmp |= internal[idx+1] << 16
  tmp |= internal[idx+2] << 8
  tmp |= internal[idx+3]

  x = rotate_left(x ^ tmp)
  ret = sbox_decrypt[x & 0xff]
  ret |= sbox_decrypt[(x >> 8) & 0xff] << 8
  ret |= sbox_decrypt[(x >> 16) & 0xff] << 16
  ret |= sbox_decrypt[(x >> 24) & 0xff] << 24
  return ret

def rotate_left(x):
  return ((x >> 31) | (x << 1)) & 0xffffffff

if __name__ == '__main__':
  decrypt_file('flag.locked')
```

File `flag` merupakan PNG yang berisi flag: `ASIS{There_aRe_real_Rans0mw4re_f0r_Linux_to0}`
