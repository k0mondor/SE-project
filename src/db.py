import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "data.db"
SCHEMA_PATH = BASE_DIR / "data" / "schema.sql"
SEGMENT_PATH = BASE_DIR / "data" / "环节字典_草稿.csv"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = connect()
    try:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()


def init_segments():
    with SEGMENT_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    conn = connect()
    try:
        for r in rows:
            conn.execute(
                "INSERT OR IGNORE INTO chain_segment (id, name, level, parent_id, definition) "
                "VALUES (?, ?, ?, ?, ?)",
                (r["id"], r["name"], r["level"], r["parent_id"] or None, r["definition"]),
            )
        conn.commit()
    finally:
        conn.close()
    return len(rows)


if __name__ == "__main__":
    init_db()
    n = init_segments()
    print("数据库已初始化:", DB_PATH)
    print("环节字典已导入:", n, "条")
