import json
import sqlite3
from collections import Counter

from src.db import connect

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


def _field_errors(rec, required):
    errors = []
    for field in required:
        value = getattr(rec, field, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            errors.append({"field": field, "reason": "必填字段为空"})
    return errors


def _to_db_value(value):
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def import_enterprises(records, dry_run=False):
    total = len(records)
    created = updated = skipped = 0
    errors = []
    missing = Counter()

    conn = connect()
    try:
        for index, rec in enumerate(records):
            # 校验必填
            errs = _field_errors(rec, ["name", "industry_code", "industry_name",
                                       "chain_segment", "region", "source", "source_url"])
            if errs:
                skipped += 1
                for e in errs:
                    errors.append({"index": index, **e})
                continue

            # 缺失字段统计
            for f in ENTERPRISE_FIELDS:
                v = getattr(rec, f, None)
                if v is None or (isinstance(v, str) and not v.strip()):
                    missing[f] += 1

            # 定位已有记录：优先 credit_code，否则 name+region
            row = None
            if rec.credit_code:
                row = conn.execute(
                    "SELECT id FROM enterprise WHERE credit_code = ?", (rec.credit_code,)
                ).fetchone()
            if row is None:
                row = conn.execute(
                    "SELECT id FROM enterprise WHERE name = ? AND region = ?",
                    (rec.name, rec.region),
                ).fetchone()

            values = [_to_db_value(getattr(rec, f, None)) for f in ENTERPRISE_FIELDS]

            if row:
                updated += 1
                if not dry_run:
                    assigns = ", ".join(f"{f} = ?" for f in ENTERPRISE_FIELDS)
                    conn.execute(
                        f"UPDATE enterprise SET {assigns}, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                        values + [row["id"]],
                    )
            else:
                created += 1
                if not dry_run:
                    cols = ", ".join(ENTERPRISE_FIELDS)
                    marks = ", ".join("?" for _ in ENTERPRISE_FIELDS)
                    conn.execute(
                        f"INSERT INTO enterprise ({cols}) VALUES ({marks})", values
                    )

        if not dry_run:
            conn.commit()
    finally:
        conn.close()

    return {
        "total": total,
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
        "missing_fields": dict(missing),
    }


def import_policies(records, dry_run=False):
    total = len(records)
    created = updated = skipped = 0
    errors = []

    conn = connect()
    try:
        for index, rec in enumerate(records):
            errs = _field_errors(rec, ["title", "region", "policy_type",
                                       "issuer", "content", "source_url"])
            if errs:
                skipped += 1
                for e in errs:
                    errors.append({"index": index, **e})
                continue

            row = conn.execute(
                "SELECT id FROM policy WHERE title = ? AND region = ?",
                (rec.title, rec.region),
            ).fetchone()
            values = [_to_db_value(getattr(rec, f, None)) for f in POLICY_FIELDS]

            if row:
                updated += 1
                if not dry_run:
                    assigns = ", ".join(f"{f} = ?" for f in POLICY_FIELDS)
                    conn.execute(
                        f"UPDATE policy SET {assigns} WHERE id = ?", values + [row["id"]]
                    )
            else:
                created += 1
                if not dry_run:
                    cols = ", ".join(POLICY_FIELDS)
                    marks = ", ".join("?" for _ in POLICY_FIELDS)
                    conn.execute(f"INSERT INTO policy ({cols}) VALUES ({marks})", values)

        if not dry_run:
            conn.commit()
    finally:
        conn.close()

    return {
        "total": total,
        "created": created,
        "updated": updated,
        "skipped": skipped,
        "errors": errors,
    }


def import_status():
    conn = connect()
    try:
        enterprise_count = conn.execute("SELECT COUNT(*) FROM enterprise").fetchone()[0]
        policy_count = conn.execute("SELECT COUNT(*) FROM policy").fetchone()[0]
        segment_count = conn.execute("SELECT COUNT(*) FROM chain_segment").fetchone()[0]
        total = conn.execute("SELECT COUNT(*) FROM enterprise").fetchone()[0]
        with_source = conn.execute(
            "SELECT COUNT(*) FROM enterprise WHERE source IS NOT NULL AND source_url IS NOT NULL"
        ).fetchone()[0]
        missing_dims = {}
        for dim, col in [("经营规模", "employee_scale"), ("技术/资质", "tech_qualifications"),
                         ("投资动向", "investment_events")]:
            n = conn.execute(
                f"SELECT COUNT(*) FROM enterprise WHERE {col} IS NULL OR {col} = ''"
            ).fetchone()[0]
            if n:
                missing_dims[dim] = n
        last = conn.execute("SELECT MAX(updated_at) FROM enterprise").fetchone()[0]
        return {
            "enterprise_count": enterprise_count,
            "policy_count": policy_count,
            "segment_count": segment_count,
            "with_source_ratio": round(with_source / total, 4) if total else 0,
            "missing_dims": missing_dims,
            "pending_segments": [],
            "last_import_at": last,
        }
    finally:
        conn.close()
