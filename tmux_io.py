"""
Create: spawn agent baru via tmux.
Language: ketik teks ke pane agent lain, tekan Enter.
"""
from __future__ import annotations
import subprocess
import shutil

class TmuxError(RuntimeError):
    pass

def _require_tmux() -> None:
    if not shutil.which("tmux"):
        raise TmuxError("tmux tidak ditemukan.")

def session_exists(name: str) -> bool:
    r = subprocess.run(["tmux", "has-session", "-t", name], capture_output=True, text=True)
    return r.returncode == 0

def spawn(name: str, cmd: str = "bash") -> None:
    _require_tmux()
    if session_exists(name):
        return
    subprocess.run(["tmux", "new-session", "-d", "-s", name, cmd], check=True)

def tell(name: str, text: str) -> None:
    if not session_exists(name):
        raise TmuxError(f"sesi '{name}' tidak ada")
    subprocess.run(["tmux", "send-keys", "-t", name, text, "Enter"], check=True)

def capture(name: str, lines: int = 40) -> str:
    r = subprocess.run(
        ["tmux", "capture-pane", "-p", "-t", name, "-S", f"-{lines}"],
        capture_output=True, text=True, check=True,
    )
    return r.stdout