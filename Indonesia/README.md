# Al-Muhit Indonesia — Millennium Dawn override

Override kecil untuk **Millennium Dawn 2.0.x**. Folder `Millennium-Dawn` asli tidak diubah; mod ini menyalin seluruh `history/states/` MD lalu menimpa 5 file yang diubah.

## State yang disentuh

| State | Nama MD | Perubahan |
|---:|---|---|
| 631 | Western Java | SDA + manpower x2 |
| 1114 | Central Java | SDA + manpower x2 |
| 634 | Eastern Java | SDA + manpower x2 |
| 640 | Kalimantan (Borneo) | SDA |
| 639 | Sulawesi | SDA |

## Tambahan SDA (gabungan 5 state)

| Resource | Tambahan | Total akhir |
|---|---:|---:|
| oil | 150 | 173 |
| steel | 300 | 311 |
| aluminium | 340 | 350 |
| coal | 120 | 120 |
| chromium | 200 | 200 |
| tungsten | 170 | 243 |
| rubber | 100 | 228 |

## Nama resource di UI Millennium Dawn

Key di file state tetap memakai key vanilla, tapi MD menampilkannya dengan nama lain:

| Key di file state | Nama tampilan di MD |
|---|---|
| `oil` | Oil |
| `steel` | Steel |
| `aluminium` | **Light Metals** |
| `chromium` | **Precious Metals** |
| `tungsten` | **Technology Metals** |
| `rubber` | Rubber |
| `coal` | Coal (resource bawaan 1.20; MD 2.0 tidak punya sistem coal khusus) |

Jadi jangan terkecoh kalau di UI tidak tertulis "aluminium", "chromium", atau "tungsten".

## Manpower Jawa

| State | Sebelum | Sesudah |
|---:|---:|---:|
| 631 | 35.729.537 | 71.459.074 |
| 1114 | 31.228.940 | 62.457.880 |
| 634 | 34.783.640 | 69.567.280 |

## Install

1. Salin folder `Indonesia` ke `.../Hearts of Iron IV/mod/Al-Muhit Indonesia`.
2. Salin `Al-Muhit Indonesia.mod` ke `.../Hearts of Iron IV/mod/`.
3. Di launcher, aktifkan **Millennium Dawn** dulu, lalu **Al-Muhit Indonesia** di bawahnya.

Karena MD memakai `replace_path = "history/states"`, override ini juga menyalin **seluruh** folder `history/states/` MD lalu menimpa 5 state yang diubah, dan ikut mendeklarasikan `replace_path = "history/states"` supaya file kita yang dipakai game.

Penting: HOI4 menentukan load order dari **nama file `.mod`** (dan `dependencies`), bukan dari urutan di `dlc_load.json`. Karena `Al-Muhit Indonesia.mod` secara alfabet mendahului `Millennium-Dawn.mod`, mod ini punya:

```text
dependencies={
	"Millennium Dawn: A Modern Day Mod"
}
```

Tanpa `dependencies`, MD dimuat belakangan dan menimpa file override ini — itulah sebabnya resource tetap angka default.

## Regenerate

```powershell
python tools/generate.py --md "C:\Users\myace\Documents\Paradox Interactive\Hearts of Iron IV\mod\Millennium-Dawn"
python tools/validate.py
```
