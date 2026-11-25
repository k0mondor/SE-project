"""按接口契约第 3 节的 8 条规则清洗原始数据。

输入 data/企业数据.csv、data/政策数据.csv、data/环节字典_草稿.csv
输出 data/企业_清洗后.csv、data/政策_清洗后.csv、data/清洗报告.json
运行：python data/clean.py
"""

import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent

ENTERPRISE_COLS = [
    "name", "credit_code", "founded_year", "legal_person", "reg_capital",
    "employee_scale", "revenue_scale", "industry_code", "industry_name",
    "chain_segment", "region", "production_bases", "tech_qualifications",
    "investment_events", "source", "source_url",
]
POLICY_COLS = [
    "title", "region", "industry", "policy_type", "issuer", "publish_date",
    "eligibility", "content", "source_url",
]
VALID_SOURCE = {"qcc", "tianyancha", "annual_report", "official_site", "manual"}
VALID_SEGMENT = {"芯片设计", "晶圆制造", "先进封装", "半导体设备", "半导体材料"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, header, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def clean_enterprises(rows, report):
    kept, seen_code, seen_name_region = [], set(), set()
    dup_code, dup_name = [], []

    for r in rows:
        code = r["credit_code"].strip()
        key = (r["name"].strip(), r["region"].strip())

        # 规则1 去重：优先 credit_code，缺失时 name+region
        if code and code in seen_code:
            dup_code.append(code)
            continue
        if key in seen_name_region:
            dup_name.append(key[0])
            continue
        if code:
            seen_code.add(code)
        seen_name_region.add(key)

        # 规则2 行业代码：4 位数字
        r["industry_code"] = r["industry_code"].strip()
        if not (r["industry_code"].isdigit() and len(r["industry_code"]) == 4):
            report["行业代码异常"].append({"name": r["name"], "value": r["industry_code"]})

        # 规则3 环节归一化：必须命中字典
        r["chain_segment"] = r["chain_segment"].strip()
        if r["chain_segment"] not in VALID_SEGMENT:
            report["待确认环节"].append({"name": r["name"], "value": r["chain_segment"]})

        # 规则4 地域归一化：统一到省+市
        r["region"] = r["region"].strip()
        if not r["region"].startswith("浙江省"):
            report["地域异常"].append({"name": r["name"], "value": r["region"]})

        # 规则5 规模字段：去掉模糊表述
        for c in ("employee_scale", "revenue_scale"):
            r[c] = r[c].strip()
            if any(w in r[c] for w in ("约", "左右", "大概", "近")):
                report["规模模糊表述"].append({"name": r["name"], "field": c, "value": r[c]})
                r[c] = ""

        # 规则6 缺失值：空字符串统一为 null 并统计
        for c in ENTERPRISE_COLS:
            if not r[c].strip():
                r[c] = None
                report["缺失字段统计"][c] = report["缺失字段统计"].get(c, 0) + 1

        # 规则7 来源必填：无来源直接拒收
        if r["source"] not in VALID_SOURCE or not r["source_url"]:
            report["来源拒收"].append({"name": r["name"], "source": r["source"]})
            continue

        kept.append(r)

    report["去重"][ "信用代码重复"] = dup_code
    report["去重"]["名称地域重复"] = dup_name
    return [[r[c] for c in ENTERPRISE_COLS] for r in kept]


def clean_policies(rows, report):
    kept = []
    for r in rows:
        # 规则8 政策原文：只做摘录，不改写；必填字段缺失拒收
        required = ("title", "region", "policy_type", "issuer", "content", "source_url")
        missing = [c for c in required if not r[c].strip()]
        if missing:
            report["政策拒收"].append({"title": r["title"], "missing": missing})
            continue
        for c in POLICY_COLS:
            r[c] = r[c].strip()
        kept.append(r)
    return [[r[c] for c in POLICY_COLS] for r in kept]


def main():
    ent = read_csv(BASE / "企业数据.csv")
    pol = read_csv(BASE / "政策数据.csv")

    report = {
        "输入企业数": len(ent),
        "输入政策数": len(pol),
        "去重": {},
        "缺失字段统计": {},
        "待确认环节": [],
        "行业代码异常": [],
        "地域异常": [],
        "规模模糊表述": [],
        "来源拒收": [],
        "政策拒收": [],
    }

    ent_clean = clean_enterprises(ent, report)
    pol_clean = clean_policies(pol, report)

    write_csv(BASE / "企业_清洗后.csv", ENTERPRISE_COLS, ent_clean)
    write_csv(BASE / "政策_清洗后.csv", POLICY_COLS, pol_clean)

    report["输出企业数"] = len(ent_clean)
    report["输出政策数"] = len(pol_clean)
    (BASE / "清洗报告.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("企业:", len(ent), "->", len(ent_clean))
    print("政策:", len(pol), "->", len(pol_clean))
    print("待确认环节:", len(report["待确认环节"]))
    print("缺失字段统计:", report["缺失字段统计"])


if __name__ == "__main__":
    main()
