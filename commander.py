import logging
import shutil
import subprocess

from builderguild.config import Config
from builderguild.errors import TmuxError, TmuxNotAvailableError
from builderguild.graph import FactGraph

logger = logging.getLogger(__name__)


# --- BAGIAN TMUX (CREATE & LANGUAGE) ---
def session_exists(name):
    r = subprocess.run(["tmux", "has-session", "-t", name], capture_output=True)
    return r.returncode == 0


def _run_tmux(args):
    try:
        subprocess.run(["tmux", *args], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        detail = e.stderr.decode(errors="replace").strip() if e.stderr else ""
        raise TmuxError(f"tmux {args[0]} gagal: {detail}") from e


def spawn_tmux(name, cmd="bash"):
    if not shutil.which("tmux"):
        raise TmuxNotAvailableError("tmux belum diinstall! (pkg install tmux)")
    if not session_exists(name):
        _run_tmux(["new-session", "-d", "-s", name, cmd])
    return True


def tell_tmux(name, text):
    if session_exists(name):
        _run_tmux(["send-keys", "-t", name, text, "Enter"])


# --- BAGIAN COMMANDER ---
def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger.info("=== BUILDERGUILD LEGION DIMULAI ===")

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
        logger.info("Tidak ada task. Keluar.")
        return

    logger.info("Ditemukan %d task. Membangunkan tmux...", len(tasks))
    try:
        spawn_tmux("bg-soldier", "bash")
    except TmuxError as e:
        logger.error("%s", e)
        return

    for t in tasks:
        logger.info("[DISPATCH] Mengirim task ke Soldier: %s", t["title"])
        tell_tmux("bg-soldier", f"Kerjakan task ini: {t['title']}")
        db.update_status(t["id"], "in_progress")

    logger.info(
        "Selesai men-dispatch task. Silakan cek layar tmux (bg-soldier)."
    )


if __name__ == "__main__":
    main()