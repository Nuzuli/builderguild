# builderguild — The Autonomous Software Legion

> Autonomous software engineering legion — AI commander + worker swarm + layered fact-intent graph for coding tasks.

**Status**: Prototipe / Eksperimen. **Lisensi**: MIT.

## Kenapa builderguild?
Proyek ini terinspirasi dari pola *legion AI* (seperti sapper-v2), namun dipindahkan ke domain **Software Engineering** yang legal dan mudah di-benchmark. 

## Fondasi
| Kapabilitas | Implementasi |
|---|---|
| **Create** | spawn agent baru via `tmux` |
| **Language** | kirim teks ke pane agent lain |
| **History** | fact graph SQLite: `title / summary / evidence` |

## Institusi
- **Law** — `SKILL.md` (easy-first scheduling, stop-loss)
- **Economy** — model tiering: commander pakai model besar, soldier pakai model murah
- **Division of labor** — commander / general / scout / soldier / signalman

## Quick Start
```bash
git clone https://github.com/Nuzuli/builderguild.git
cd builderguild
pip install -e .
builderguild --help