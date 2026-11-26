# Al-Muhit

Repo gabungan untuk mod Hearts of Iron IV Al-Muhit. Sebelumnya mod-mod ini tersebar di beberapa repo terpisah; sekarang semuanya dirapikan di satu tempat.

## Isi

| Folder | Mod | Catatan |
|---|---|---|
| `Mamluk/` | Al-Muhit (Mamluk / Mesir-Levant-Sudan) | Termasuk perubahan lokal yang belum di-commit di repo lama. |
| `Germany/` | Al-Muhit Germany | Manpower x5, dockyard 10, +40 civilian factory. |
| `Italy/` | Al-Muhit Italy | 29 state ITA, manpower x2, 3 megalopolis, 200 tech. |
| `Indonesia/` | Al-Muhit Indonesia | Override untuk Millennium Dawn: SDA melimpah + manpower Jawa x2. |

Setup lama tetap bisa dipakai; repo ini adalah **sumber gabungan yang rapi**. Repo lama tidak dihapus otomatis.

## Load order untuk Millennium Dawn

1. `Millennium Dawn: A Modern Day Mod`
2. `Al-Muhit Indonesia (MD Override)`

Folder `Millennium-Dawn` asli tidak diubah oleh override Indonesia.

## Validasi

```powershell
python Indonesia/tools/validate.py
```

Generator Indonesia:

```powershell
python Indonesia/tools/generate.py
```

## Repo lama

- `https://github.com/hayyanjpg/hoi4-al-muhit` → `Mamluk/`
- `https://github.com/hayyanjpg/Al-Muhit-Germany` → `Germany/`
- `https://github.com/hayyanjpg/Al-Muhit-Italy` → `Italy/`
