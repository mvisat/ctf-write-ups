# Wandere bits
```
Points: 109
Solves: 49
Category: Reverse
Description: I lost my flag's bit under a cherry tree... Can you find it?

$ file wandere_bits
wandere_bits: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=141e08c0806d8e6ac51c80eb5a54b5534d3afbca, not stripped
```

## English
TODO

## Bahasa Indonesia
Program tersebut meminta flag pada parameter pertamanya. Coba kita buka dengan IDA untuk mendapatkan pseudocode.

```c
int __cdecl main(int argc, const char **argv, const char **envp) {
...
    v4 = argv[1];
    v5 = -1LL;
    v12 = &v13;
    if ( v4 )
      v5 = (unsigned __int64)&v4[strlen(v4)];
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::_M_construct<char *>(&v12, v4, v5);
    BigNumber::BigNumber(&v9, &v12, 0LL);
    if ( v12 != &v13 )
      operator delete(v12);
    v12 = &v13;
    std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::_M_construct<char *>(
      &v12,
      v9,
      v10 + v9);
    v14 = v11;
    wapint(&v7, &v12);
    v6 = std::__cxx11::basic_string<char,std::char_traits<char>,std::allocator<char>>::compare(
           &v7,
           "82a386a3b7983198313b363293399232349892369a98323692989a313493913036929a303abf");
    if ( v7 != &v8 )
      operator delete(v7);
    BigNumber::~BigNumber((BigNumber *)&v12);
    if ( v6 )
      std::__ostream_insert<char,std::char_traits<char>>(&std::cout, "0ops, try harder plz :(", 23LL);
    else
      std::__ostream_insert<char,std::char_traits<char>>(&std::cout, "gj, you got the flag :)", 23LL);
  ...
```

Program tersebut melakukan transformasi string parameter yang diberikan. Pertama dijadikan `BigInteger`, lalu fungsi `wapint` menjadikan ke sebuah string dalam heksadesimal. Kemudian string tersebut dibandingkan dengan `82a386a3b7983198313b363293399232349892369a98323692989a313493913036929a303abf`. Jika sama, maka parameter tersebut adalah flagnya.

Akan tetapi, fungsi `wapint` terlihat sedikit rumit. Coba kita jalankan dengan GDB (+gdb-peda) untuk melihat bagaimana hasil transformasinya. Pertama, cari dahulu address yang tepat untuk melihat hasil fungsi `wapint`, bisa dengan GDB maupun IDA.

```
.text:000000000040108F  mov     [rsp+88h+var_18], eax
.text:0000000000401093  call    _Z6wapintB5cxx119BigNumber ; => Fungsi wapint
.text:0000000000401098  mov     esi, offset a82a386a3b79831 ; "82a386a3b7983198313b3632933992323498923"...
```

Address `0x0401098` kelihatannya cukup baik untuk dipasang *breakpoint*. Kita coba jalankan dengan parameter sederhana, seperti `a`.

```shell
$ gdb wandere_bits
gdb-peda$ b *0x0401098
gdb-peda$ r a
...
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd890 --> 0x7fffffffd8a0 --> 0x3339 ('93')
0008| 0x7fffffffd898 --> 0x2
0016| 0x7fffffffd8a0 --> 0x3339 ('93')
0024| 0x7fffffffd8a8 --> 0x400eb0 (<_ZNSt8ios_base4InitD1Ev@plt>:	jmp    QWORD PTR [rip+0x2071aa]        # 0x608060)
0032| 0x7fffffffd8b0 --> 0x61b430 ('0' <repeats 200 times>...)
...
Breakpoint 1, 0x0000000000401098 in main ()
gdb-peda$
```

Hasil transformasi fungsi `wapint` pada run program di atas terletak pada address stack `0x7fffffffd8a0`, yaitu string `93`. Sekarang kita coba dengan parameter-parameter lainnya.

```shell
gdb-peda$ r a
0016| 0x7fffffffd8a0 --> 0x3239 ('93')

gdb-peda$ r b
0016| 0x7fffffffd8a0 --> 0x3239 ('92')

gdb-peda$ r ab
0016| 0x7fffffffd8a0 --> 0x32393239 ('9292')

gdb-peda$ r ba
0016| 0x7fffffffd8a0 --> 0x33393139 ('9193')

gdb-peda$ r abc
0016| 0x7fffffffd8a0 --> 0x343931393239 ('929194')

gdb-peda$ r ca
0016| 0x7fffffffd8a0 --> 0x33393339 ('9393')
```

Jika kita perhatikan, hasil transformasi pada karakter terakhir parameter nilainya ditambah dengan 1. Sehingga transformasi tersebut adalah `a => 92`, `b => 91`, `c => 93`, dst dengan pengecualian jika karakter tersebut adalah karakter terakhir.

Dengan begitu, kita dapat membuat *mapping* untuk untuk melakukan transformasi balik heksadesimal ke karakter aslinya. Kita masukkan karakter yang mungkin ada dalam flag sebagai parameter (dan ditambah karakter *dummy*, karena karakter terakhir nilainya akan ditambah 1).

```shell
gdb-peda$ r {}_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789a
0000| 0x7fffffffd850 --> 0x61c5d0 ("b7beaf929193989a999b949695979c9e9d9fb0b2b1b3b8bab9bbb4b6b5828183888a898b848685878c8e8d8fa0a2a1a3a8aaa9aba4a6a530323133383a393b343693")
```

Kita buat script python sederhana untuk mendapatkan flagnya. Jangan lupa untuk mengurangi nilai karakter terakhir pada string dengan 1 (lihat kode).

```python
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
```

Flag: `ASIS{d2d2791c6a18da9ed19ade28cb09ae05}`
