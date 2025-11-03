import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime


DB_PATH = os.getenv("MAIKA_DB", "metrics.db")


def _ensure_parent_dir(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


@contextmanager
def get_connection(readonly: bool = False):
    uri = DB_PATH
    _ensure_parent_dir(uri)
    conn = sqlite3.connect(uri)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        if not readonly:
            conn.commit()
    finally:
        conn.close()


def migrate() -> None:
    with get_connection() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                display_name TEXT
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS xp_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                amount INTEGER NOT NULL,
                meta_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS srs_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                item_id TEXT NOT NULL,
                due_at TEXT NOT NULL,
                ease REAL NOT NULL DEFAULT 2.5,
                interval_days INTEGER NOT NULL DEFAULT 0,
                last_result TEXT,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                state_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
        )


def ensure_user(user_id: str, display_name: str | None = None) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO users(user_id, created_at, display_name) VALUES(?,?,?)",
                (user_id, datetime.utcnow().isoformat(), display_name),
            )


def add_xp(user_id: str, kind: str, amount: int, meta_json: str | None = None) -> None:
    ensure_user(user_id)
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO xp_events(user_id, kind, amount, meta_json, created_at) VALUES (?,?,?,?,?)",
            (user_id, kind, amount, meta_json, datetime.utcnow().isoformat()),
        )


def get_user_xp(user_id: str) -> int:
    with get_connection(True) as conn:
        cur = conn.execute(
            "SELECT COALESCE(SUM(amount),0) AS total FROM xp_events WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        return int(row[0] if row else 0)


def upsert_srs_review(
    user_id: str,
    item_id: str,
    due_at_iso: str,
    ease: float,
    interval_days: int,
    last_result: str | None,
) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT id FROM srs_reviews WHERE user_id = ? AND item_id = ?",
            (user_id, item_id),
        )
        now = datetime.utcnow().isoformat()
        if (row := cur.fetchone()) is None:
            cur.execute(
                """
                INSERT INTO srs_reviews(user_id, item_id, due_at, ease, interval_days, last_result, updated_at)
                VALUES (?,?,?,?,?,?,?)
                """,
                (user_id, item_id, due_at_iso, ease, interval_days, last_result, now),
            )
        else:
            cur.execute(
                """
                UPDATE srs_reviews
                SET due_at = ?, ease = ?, interval_days = ?, last_result = ?, updated_at = ?
                WHERE id = ?
                """,
                (due_at_iso, ease, interval_days, last_result, now, row[0]),
            )


def get_due_srs_items(user_id: str, now_iso: str) -> list[sqlite3.Row]:
    with get_connection(True) as conn:
        cur = conn.execute(
            "SELECT * FROM srs_reviews WHERE user_id = ? AND due_at <= ? ORDER BY due_at ASC",
            (user_id, now_iso),
        )
        return cur.fetchall()


