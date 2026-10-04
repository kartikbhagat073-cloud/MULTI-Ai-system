"""Tiny SQLite store for the outputs people chose."""
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "history.db"


def _conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    c.execute("""CREATE TABLE IF NOT EXISTS selections(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        prompt TEXT NOT NULL, model TEXT NOT NULL, output TEXT NOT NULL, all_outputs TEXT NOT NULL)""")
    return c


def save(prompt: str, model: str, output: str, all_outputs: dict) -> int:
    with _conn() as c:
        cur = c.execute("INSERT INTO selections(prompt, model, output, all_outputs) VALUES (?,?,?,?)",
                        (prompt, model, output, json.dumps(all_outputs)))
        return cur.lastrowid


def recent(limit: int = 20) -> list[dict]:
    with _conn() as c:
        rows = c.execute("SELECT id, created_at, prompt, model, output FROM selections ORDER BY id DESC LIMIT ?",
                         (limit,)).fetchall()
    return [dict(r) for r in rows]
