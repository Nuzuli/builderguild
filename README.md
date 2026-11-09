# builderguild — The Autonomous Software Legion

> Legion AI untuk software engineering: commander, scout, soldier, dan signalman yang bekerja bersama menyimpan memori di fact-intent graph.

Status: tahap awal (prototipe). API bisa berubah.

## Kebutuhan

- Python 3.10 atau lebih baru
- git
- tmux (hanya untuk `commander.py`)

## Instalasi

```bash
git clone https://github.com/Nuzuli/builderguild.git
cd builderguild
pip install -r requirements-lock.txt
pip install -e .
```

`requirements-lock.txt` berisi versi pasti semua dependensi supaya instalasi bisa diulang dengan hasil yang sama.

## Cara Menjalankan

```bash
# Inisialisasi graph
builderguild setup

# Tampilkan daftar fakta/task
builderguild status

# Jalankan commander (membagi task ke sesi tmux "bg-soldier")
python commander.py
```

## Konfigurasi

Semua konfigurasi dibaca dari environment variable. Salin `.env.example` sebagai acuan.

| Variabel | Default | Keterangan |
| --- | --- | --- |
| `BG_COMMANDER_MODEL` | `claude-sonnet-4-5` | Model untuk commander |
| `BG_SOLDIER_MODEL` | `claude-haiku-4-5` | Model untuk soldier |
| `BG_MAX_TOKENS` | `200000` | Batas token (harus angka bulat) |
| `BG_MAX_AGENTS` | `6` | Jumlah agent maksimum (harus angka bulat) |
| `BG_DB_PATH` | `runs/graph.db` | Lokasi database SQLite |
| `BG_REPO_PATH` | `.` | Lokasi repo yang dikerjakan |

Nilai angka yang tidak valid menghasilkan `ConfigError` dengan nama variabelnya.

## Arsitektur

- `builderguild/builderguild/config.py`: membaca konfigurasi dari environment dan memvalidasinya (`Config`, `ConfigError`).
- `builderguild/builderguild/graph.py`: `FactGraph`, penyimpanan fakta dan status task di SQLite.
- `builderguild/builderguild/cli.py`: perintah `builderguild setup` dan `builderguild status`.
- `commander.py`: membuat sesi tmux dan mengirim task dari graph ke soldier, lalu menandai statusnya `in_progress`.

Alur: `commander.py` membaca task dari `FactGraph`, mengirimnya ke sesi tmux, lalu memperbarui statusnya di graph.

## Struktur Proyek

```
.
├── builderguild/builderguild/   # paket utama (config, graph, cli)
├── tests/                       # tes otomatis (pytest)
├── commander.py                 # titik masuk commander
├── pyproject.toml               # konfigurasi paket, ruff, pytest
├── requirements.txt             # dependensi langsung
├── requirements-lock.txt        # dependensi terkunci
└── .github/workflows/           # CI dan pembuat lockfile
```

## Menjalankan Tes

```bash
pip install pytest pytest-cov
pytest --cov=builderguild --cov-fail-under=70
```

CI (GitHub Actions) menjalankan lint (`ruff`), tes dengan batas coverage 70%, dan `pip-audit` di Python 3.10 dan 3.12 pada setiap push dan pull request.

## Memperbarui Lockfile

Jalankan workflow **Generate lockfile** dari tab Actions (Run workflow). Hasilnya di-commit otomatis ke `requirements-lock.txt`.

## Lisensi

Lihat file [LICENSE](LICENSE).