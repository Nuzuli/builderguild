import shutil
import subprocess

from builderguild.config import Config
from builderguild.graph import FactGraph


# --- BAGIAN TMUX (CREATE & LANGUAGE) ---
def session_exists(name):
    r = subprocess.run(["tmux", "has-session", "-t", name], capture_output=True)
    return r.returncode == 0


def spawn_tmux(name, cmd="bash"):
    if not shutil.which("tmux"):
        print("[ERROR] tmux belum diinstall! (pkg install tmux)")
        return False
    if not session_exists(name):
        subprocess.run(["tmux", "new-session", "-d", "-s", name, cmd])
    return True


def tell_tmux(name, text):
    if session_exists(name):
        subprocess.run(["tmux", "send-keys", "-t", name, text, "Enter"])


# --- BAGIAN COMMANDER ---
def main():
    print("=== BUILDERGUILD LEGION DIMULAI ===")

    db = FactGraph(Config.load().db_path)

    # Contoh task awal
    db.add(
        "Fix bug",
        "Ada error di file main.py",
        {"file": "main.py", "line": 10},
    )
    db.add(
        "Tulis test",
        "Test untuk modul auth",
        {"file": "tests/test_auth.py"},
    )

    tasks = db.list_titles()
    if not tasks:
        print("Tidak ada task. Keluar.")
        return

    print(f"Ditemukan {len(tasks)} task. Membangunkan tmux...")
    spawn_tmux("bg-soldier", "bash")

    for t in tasks:
        print(f"[DISPATCH] Mengirim task ke Soldier: {t['title']}")
        tell_tmux("bg-soldier", f"Kerjakan task ini: {t['title']}")
        db.update_status(t["id"], "in_progress")

    print("Selesai men-dispatch task. Silakan cek layar tmux (bg-soldier).")

if __name__ == "__main__": 
  main()
