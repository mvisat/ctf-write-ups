# Unbreakable
```
Points: 193
Solves: 22
Category: Reverse
Description: We think this challenge is unbreakable, even for you? Try it now!.
The unbreakable is updated, please re-download!

$ file unbreakable
unbreakable: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=62bb339ccb8cea4653f01df97ad0f942b2c7d579, not stripped
```

## English
TODO

## Bahasa Indonesia
Buka dengan IDA untuk mendapatkan pseudocode.

```c
int __cdecl main(int argc, const char **argv, const char **envp) {
  ...
  std::basic_ifstream<char,std::char_traits<char>>::basic_ifstream(&v22, "key", 8LL);
  v3 = *(&v23 + *(v22 - 24));
  src = &v14;
  std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::_M_construct<std::istreambuf_iterator<char,std::char_traits<char>>>(
    &src, v3, 0xFFFFFFFFLL, 0LL, 0xFFFFFFFFLL);
  if ( v24 & 5 ) {
    std::__ostream_insert<char,std::char_traits<char>>(&edata, "error, input not found", 22LL);
    std::endl<char,std::char_traits<char>>(&edata);
    v4 = 1;
    goto LABEL_3;
  }
  ...
  *(v18 + v11) = 0;
  hencode(&v15, &v18);
  std::basic_ofstream<char,std::char_traits<char>>::basic_ofstream(&v21, "flag.enc", 48LL);
  ...
LABEL_3:
}
```

Pada dasarnya, program ini membaca file `key`, melakukan transformasi dengan fungsi `hencode`, lalu menulis ke dalam file `flag.enc`. Namun, fungsi `hencode` terlihat panjang dan rumit. Kita coba lakukan analisis dengan membuat file `key` palsu dan melihat apa hasilnya di file `flag.enc`.

```shell
$ printf "a" > key && ./unbreakable && hd flag.enc
00000000  63 16                                             |c.|

$ printf "b" > key && ./unbreakable && hd flag.enc
00000000  63 2e                                             |c.|

$ printf "aa" > key && ./unbreakable && hd flag.enc
00000000  63 16 16 63                                       |c..c|

$ printf "ab" > key && ./unbreakable && hd flag.enc
00000000  63 16 2e 63                                       |c..c|

$ printf "bb" > key && ./unbreakable && hd flag.enc
00000000  63 2e 2e 63                                       |c..c|

$ printf "aba" > key && ./unbreakable && hd flag.enc
00000000  63 16 2e 63 63 16                                 |c..cc.|

$ printf "abb" > key && ./unbreakable && hd flag.enc
00000000  63 16 2e 63 63 2e                                 |c..cc.|
```

Bisa melihat polanya? Setiap karakter akan ditransformasi menjadi 2 byte (yang kita tidak tahu bagaimana algoritmanya). Karakter pada posisi ganjil akan ditransformasi seperti biasa, tetapi karakter pada posisi genap akan dibalik posisi byte-nya. Sebagai  contoh, `aa` akan ditransformasi menjadi `63 16 16 63`, terlihat bahwa `63 16` dibalik menjadi `16 63`.

Karena transformasi bersifat satu ke satu, kita hanya perlu mencari *mapping* semua byte sebanyak 256, yaitu dari 0 sampai 255. Kita dapat membuat script python untuk membuat file `key` yang berisi byte tersebut, menjalankan file `unbreakable`, dan membaca isi file `flag.enc`. Terakhir, lakukan transformasi ulang dari file `flag.enc` yang asli untuk mendapatkan flag.

```python
#!/usr/bin/env python3
import os

mapping = {}
for i in range(256):
  with open('key', 'wb') as f:
    f.write(bytes([i]))
  assert os.system("./unbreakable") == 0
  with open('flag.enc', 'rb') as f:
    mapping[f.read()] = i

s = open('flag_original.enc', 'rb').read()
with open('flag', 'wb') as f:
  for i in range(0, len(s), 2):
    cur = s[i:i+2]
    flip = True if (i // 2) % 2 == 0 else False
    if flip:
      cur = cur[::-1]
    f.write(bytes([mapping[cur]]))
```

File `flag` merupakan PNG yang berisi flag: `ASIS{Ju5t_C0py_And_paSte_on_Sc0rebo4rd!!}`
