# TextUserInterface-BMKG
TUI untuk menampilkan prakiraan cuaca memggunakan API BMKG,
ini versi API BMKG versi yang sebelum nya adalah versi web scrapping
yang bisa di lihat disini -> [`Scrapping_BMKG`](https://github.com/Tooya12/Scrapping_BMKG).

TextUserInterface-BMKG ini menggunakan Kode Wilayah Administrasi IV [`Kepmendagri-2022`](kepmendagri-2022.json)
Terimakasih kepada [`cahyadsn`](https://github.com/cahyadsn/wilayah) untuk data wilayah.
Saya juga menyediakan Kode Wilayah Administrasi IV dalam bentuk csv dsn json di sini -> [`Kode Wilayah`](https://github.com/Tooya12/Kode-Wilayah-Indonesia)

## Installasi
Pastikan menggunakan Python 3.9+

```bash
   pip install -r requirements.txt
```

## Penggunaan
Jalankan Program :

```bash
   python bmkg.py
```

Di tampilan awal anda harus memilih Provinsi, Kabupaten/Kota, Kecamatan, Keluran/desa.

Data BMKG akan di perbaharui setiap 10 menit saat anda menjalankan program nya.

Contoh Tampilan Data Cuaca :

```bash
                        Prakiraan Cuaca BMKG
           Jawa Barat - Kota Bogor - Bogor Barat - Loji

                      Selsa 24 Desember 2024
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                          03:00                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Cuaca            : Cerah Berawan                          │
│ Suhu             : 29 °C                                  │
│ Tutupan Awan     : 76%                                    │
│ Jarak Pandang    : < 10 km                                │
│ Kelembapan Udara : 74%                                    │
│ Kecepatan Angin  : 7.5 km/jam                             │
│ Arah Angin       : Barat Laut                             │
└───────────────────────────────────────────────────────────┘
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                          06:00                            ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Cuaca            : Hujan Sedang                           │
│ Suhu             : 25 °C                                  │
│ Tutupan Awan     : 100%                                   │
│ Jarak Pandang    : < 6 km                                 │
│ Kelembapan Udara : 86%                                    │
│ Kecepatan Angin  : 6.5 km/jam                             │
│ Arah Angin       : Selatan                                │
└───────────────────────────────────────────────────────────┘
```
Ketik help untuk menampilkan command yang tersedia.

```bash
>>> help

List Command yang tersedia :

help                   Untuk menampilkan pesan ini.

exit atau quit         Untuk keluar dari program.

version                Untuk menampilkan versi dan author script
                       ini.

ganti-provinsi         Untuk mengganti provinsi.

ganti-kabupaten/kota   Untuk mengganti kabupaten/kota.

ganti-kecamatan        Untuk mengganti kecamatan.

ganti-kelurahan/desa   Untuk mengganti kelurahan/desa.

daftar-provinsi        Untuk menampilkan daftar provinsi.

daftar-kabupaten/kota  Untuk menampilkan daftar kabupaten/kota
                       yang ada di provinsi saat ini.

daftar-kecamatan       Untuk menampilkan daftar kecamatan yang ada
                       di provinsi saat ini.

daftar-kelurahan/desa  Untuk menampilkan daftar kelurahan/desa
                       yang ada di provinsi saat ini.

>>>
```
Ketika dijalankan program ini akan membuat sebuah file tambahan yaitu :

```bash
   .cache cache.json configCuaca.json
```
file itu bertujuan sebagai sebuah cache dan config.
