from dataclasses import dataclass
from . import tmux_io

@dataclass
class Role:
    name: str
    system: str
    tmux_name: str

ROLES = {
    "commander": Role("commander", "Baca board, pecah goal, dispatch. Jangan menulis kode.", "bg-commander"),
    "scout": Role("scout", "Recon repo 4 menit: struktur, dependency, test gagal.", "bg-scout"),
    "general": Role("general", "Tangani task kompleks. Boleh hire soldier.", "bg-general"),
    "soldier": Role("soldier", "Kerjakan task massal (lint, test, dep).", "bg-soldier"),
    "signalman": Role("signalman", "Kumpulkan PR belum review, jalankan CI.", "bg-signalman"),
}

def spawn(role_name: str, ai_cmd: str = "bash") -> Role:
    role = ROLES[role_name]
    tmux_io.spawn(role.tmux_name, ai_cmd)
    return role

def dispatch(role_name: str, mission: str) -> None:
    role = ROLES[role_name]
    tmux_io.tell(role.tmux_name, f"[{role_name}] {mission}")