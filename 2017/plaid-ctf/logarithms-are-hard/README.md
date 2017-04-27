# logarithms are hard

| Category  | Points | Solves
| --------- | ------ | ------
| Misc      | 10     | 362

> What is e^(1.000000001)?

> Please enter in decimal with 7 places.
> (For example, if the answer was 2.71828183... the flag would be 2.7182818 )

> Hint: 2.7182818 is not the correct flag. Stop asking about it :P

> Try Google. Look for previous "X is hard" challenges from us to get more ideas.

## Bahasa Indonesia

Melihat petunjuknya, saya mencari writeup PlaidCTF tahun-tahun sebelumnya dan menemukan [artikel ini](https://github.com/ctfs/write-ups-2014/tree/master/plaid-ctf-2014/multiplication-is-hard). Intinya, Excel pernah memiliki bug dalam perhitungan perkaliannya.

Dari situ, googling dengan kata kunci "logarithm bug" dan menemukan [artikel paling atas](http://www.datamath.org/Story/LogarithmBug.htm). Terdapat tabel perhitungan logaritma yang salah. Pilih n = `1,000,000,000` dan kalkulator terbaru (TI-36X SOLAR), dan masukkan angka tersebut sebagai flagnya.

Flag: `2.7191928`
