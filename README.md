# builderguild — The Autonomous Software Legion



![CI](https://github.com/Nuzuli/builderguild/actions/workflows/ci.yml/badge.svg)




![Python](https://img.shields.io/badge/python-3.10%2B-blue)



> Legion AI untuk software engineering: commander, scout, soldier, dan signalman yang bekerja bersama menyimpan memori di fact-intent graph.

## ✨ Fitur

- **Commander**: memimpin dan membagi tugas ke para pekerja.
- **Scout, Soldier, Signalman**: pekerja dengan peran berbeda yang menjalankan tugas coding.
- **Fact-intent graph**: memori bersama yang menyimpan fakta dan tujuan selama pekerjaan berlangsung.

## 📦 Kebutuhan

- Python 3.10 atau lebih baru
- git
- tmux

## 🚀 Cara Menjalankan (Di HP / Laptop)

```bash
# 1. Clone repo ini
git clone https://github.com/Nuzuli/builderguild.git
cd builderguild

# 2. Install
pip install -r requirements.txt
pip install -e .

# 3. Jalankan Commander Legion
python commander.py
```

## 🧪 Menjalankan Tes

```bash
pip install pytest
pytest
```

Tes juga berjalan otomatis lewat GitHub Actions setiap ada push atau pull request ke `main`.

## 🗂️ Struktur Proyek

```
builderguild/
├── builderguild/       # paket utama
├── tests/              # tes otomatis
├── commander.py        # titik masuk untuk menjalankan legion
├── pyproject.toml      # konfigurasi paket
├── requirements.txt    # dependensi
└── .github/workflows/  # CI (GitHub Actions)
```

## 🤝 Kontribusi

Pull request dan issue sangat disambut. Jalankan `pytest` sebelum mengirim perubahan.

## 📄 Lisensi

Lihat file [LICENSE](LICENSE).