# Al-Muhit Indonesia — Millennium Dawn override

Override kecil untuk **Millennium Dawn 2.0.x**. Folder `Millennium-Dawn` asli tidak diubah; mod ini menyalin seluruh `history/states/` MD lalu menimpa 5 file SDA dan menambah slot bangunan di 17 state Indonesia.

## State yang disentuh

| State | Nama MD | Perubahan |
|---:|---|---|
| 631 | Western Java | SDA + slot bangunan x2 |
| 1114 | Central Java | SDA + slot bangunan x2 |
| 634 | Eastern Java | SDA + slot bangunan x2 |
| 640 | Kalimantan (Borneo) | SDA + slot bangunan x2 |
| 639 | Sulawesi | SDA + slot bangunan x2 |

Slot bangunan x2 juga diterapkan ke seluruh state IND lainnya: 623, 627, 629, 635, 636, 637, 638, 734, 936, 1113, 1185, dan 1226.

## Tambahan SDA (gabungan 5 state)

Bonus bawaan sudah dikali 3 (`BONUS_MULTIPLIER = 3` di `tools/generate.py`); nilai asli MD tidak diubah.

| Resource | Tambahan | Total akhir |
|---|---:|---:|
| oil | 450 | 473 |
| steel | 900 | 911 |
| aluminium | 1020 | 1030 |
| coal | 360 | 360 |
| chromium | 600 | 600 |
| tungsten | 510 | 583 |
| rubber | 300 | 428 |

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

Manpower dikembalikan ke nilai awal MD; tidak ada perkalian lagi.

| State | Nilai MD |
|---:|---:|
| 631 | 35.729.537 |
| 1114 | 31.228.940 |
| 634 | 34.783.640 |

## Kapasitas bangunan

Semua state Indonesia mendapat efek `add_extra_state_shared_building_slots` sebesar `local_building_slots` kategori MD-nya. Jadi total slot bangunan jadi dua kali kategori aslinya, misalnya `state_15` 55 → 110 dan `state_14` 51 → 102.

Efek ditaruh di dalam blok `history` tiap state, jadi tidak menyentuh `common/state_category` MD dan tidak perlu override `map/`.

## Install

1. Salin folder `Indonesia` ke `.../Hearts of Iron IV/mod/Al-Muhit Indonesia`.
2. Salin `Al-Muhit Indonesia.mod` ke `.../Hearts of Iron IV/mod/`.
3. Di launcher, aktifkan **Millennium Dawn** dulu, lalu **Al-Muhit Indonesia** di bawahnya.

Karena MD memakai `replace_path = "history/states"`, override ini juga menyalin **seluruh** folder `history/states/` MD lalu menimpa 5 state SDA dan 17 state IND untuk slot bangunan, dan ikut mendeklarasikan `replace_path = "history/states"` supaya file kita yang dipakai game.

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
