import time
import subprocess
import shutil
import sqlite3
import os
import json
import sys

# --- BAGIAN GRAPH (DATABASE) ---
class FactGraph:
    def __init__(self, db_path="runs/graph.db"):
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS facts 
            (id INTEGER PRIMARY KEY, title TEXT, summary TEXT, evidence TEXT, status TEXT)""")
        self.conn.commit()

    def list_titles(self, status="open"):
        cur = self.conn.execute("SELECT id, title, summary, evidence FROM facts WHERE status=?", (status,))
        return [{"id": r[0], "title": r[1], "summary": r[2], "evidence": r[3]} for r in cur]

    def add(self, title, summary, evidence):
        self.conn.execute("INSERT INTO facts (title, summary, evidence, status) VALUES (?, ?, ?, 'open')",
                          (title, summary, json.dumps(evidence)))
        self.conn.commit()

    def update_status(self, fact_id, status):
        self.conn.execute("UPDATE facts SET status=? WHERE id=?", (status, fact_id))
        self.conn.commit()

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
    db = FactGraph()
    
    # Contoh task awal
    db.add("Fix bug", "Ada error di file main.py", {"file": "main.py", "line": 10})
    db.add("Tulis test", "Test untuk modul auth", {"file": "tests/test_auth.py"})
    
    tasks = db.list_titles()
    if not tasks:
        print("Tidak ada task. Keluar.")
        return

    print(f"Ditemukan {len(tasks)} task. Membangunkan tmux...")
    spawn_tmux("bg-soldier", "bash")
    
    for t in tasks:
        print(f"[DISPATCH] Mengirim task ke Soldier: {t['title']}")
        tell_tmux("bg-soldier", f"Kerjakan task ini: {t['title']}")
        db.update_status(t['id'], "in_progress")

    print("Selesai men-dispatch task. Silakan cek layar tmux (bg-soldier).")

if __name__ == "__main__":
    main()