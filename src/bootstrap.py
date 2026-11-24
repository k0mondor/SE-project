"""数据库准备：建表、环节字典，必要时从清洗后 CSV 填充企业政策。

服务启动调用 ensure_database()，数据为空时自动填充。
data/import_data.py 调用 rebuild_database() 做强制重建。
"""

import csv
from pathlib import Path

from src.db import connect, init_db, init_segments

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

ENTERPRISE_FIELDS = [
    "name", "credit_code", "founded_year", "legal_person", "reg_capital",
    "employee_scale", "revenue_scale", "industry_code", "industry_name",
    "chain_segment", "region", "production_bases", "tech_qualifications",
    "investment_events", "source", "source_url",
]
POLICY_FIELDS = [
    "title", "region", "industry", "policy_type", "issuer", "publish_date",
    "eligibility", "content", "source_url",
]


def read_records(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        item = {}
        for k, v in r.items():
            if v == "" or v is None:
                item[k] = None
            elif k == "founded_year":
                item[k] = int(v)
            elif k == "reg_capital":
                item[k] = float(v)
            else:
                item[k] = v
        out.append(item)
    return out


def _insert_all():
    enterprises = read_records(DATA_DIR / "企业_清洗后.csv")
    policies = read_records(DATA_DIR / "政策_清洗后.csv")
    conn = connect()
    try:
        for r in enterprises:
            cols = ", ".join(ENTERPRISE_FIELDS)
            marks = ", ".join("?" for _ in ENTERPRISE_FIELDS)
            conn.execute(
                f"INSERT INTO enterprise ({cols}) VALUES ({marks})",
                [r.get(f) for f in ENTERPRISE_FIELDS],
            )
        for r in policies:
            cols = ", ".join(POLICY_FIELDS)
            marks = ", ".join("?" for _ in POLICY_FIELDS)
            conn.execute(
                f"INSERT INTO policy ({cols}) VALUES ({marks})",
                [r.get(f) for f in POLICY_FIELDS],
            )
        conn.commit()
    finally:
        conn.close()
    return len(enterprises), len(policies)


def ensure_database():
    """服务启动用。已有数据不动，缺数据时补齐。"""
    init_db()
    conn = connect()
    try:
        seg = conn.execute("SELECT COUNT(*) FROM chain_segment").fetchone()[0]
        ent = conn.execute("SELECT COUNT(*) FROM enterprise").fetchone()[0]
        pol = conn.execute("SELECT COUNT(*) FROM policy").fetchone()[0]
    finally:
        conn.close()

    if seg == 0:
        init_segments()
    if ent == 0 and pol == 0:
        _insert_all()


def rebuild_database():
    """强制重建。先清空三张表，再从源数据填充。"""
    init_db()
    init_segments()
    conn = connect()
    try:
        conn.execute("DELETE FROM enterprise")
        conn.execute("DELETE FROM policy")
        conn.commit()
    finally:
        conn.close()
    return _insert_all()
