from __future__ import annotations
import sqlite3
import os
import time
import json

SCHEMA = """
CREATE TABLE IF NOT EXISTS facts (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT NOT NULL,
    summary   TEXT NOT NULL,
    evidence  TEXT NOT NULL,
    kind      TEXT DEFAULT 'fact',
    status    TEXT DEFAULT 'open',
    owner     TEXT DEFAULT '',
    created   REAL NOT NULL,
    updated   REAL NOT NULL
);
"""


class FactGraph:
    def __init__(self, db_path: str):
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def list_titles(self, status: str | None = None) -> list[dict]:
        q = "SELECT id, title, status, owner FROM facts"
        args: tuple = ()
        if status:
            q += " WHERE status = ?"
            args = (status,)
        q += " ORDER BY id"
        return [dict(r) for r in self.conn.execute(q, args)]

    def add(self, title: str, summary: str, evidence: dict, kind: str = "fact", owner: str = "") -> int:
        now = time.time()
        cur = self.conn.execute(
            "INSERT INTO facts(title,summary,evidence,kind,status,owner,created,updated) VALUES (?,?,?,?,?,?,?,?)",
            (title, summary, json.dumps(evidence), kind, "open", owner, now, now),
        )
        self.conn.commit()
        if cur.lastrowid is None:
            raise RuntimeError("INSERT tidak menghasilkan id baris")
        return cur.lastrowid

    def update_status(self, fact_id: int, status: str) -> None:
        self.conn.execute(
            "UPDATE facts SET status = ?, updated = ? WHERE id = ?",
            (status, time.time(), fact_id),
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()