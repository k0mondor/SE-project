import json

from src.db import connect

B1_FIELDS = [
    "id", "name", "credit_code", "founded_year", "legal_person", "reg_capital",
    "employee_scale", "revenue_scale", "industry_code", "industry_name",
    "chain_segment", "region", "production_bases", "tech_qualifications",
    "investment_events", "source", "source_url",
]


def list_enterprises(industry_codes=None, segments=None, employee_scale=None,
                     region=None, keyword=None, page=1, page_size=20):
    """D2 组合筛选。条件之间 AND，同类多值 OR，返回命中原因，不打分。"""
    industry_codes = [x for x in (industry_codes or "").split(",") if x.strip()]
    segments = [x for x in (segments or "").split(",") if x.strip()]

    where, params = [], []

    if industry_codes:
        where.append("industry_code IN (%s)" % ",".join("?" for _ in industry_codes))
        params.extend(industry_codes)
    if segments:
        where.append("chain_segment IN (%s)" % ",".join("?" for _ in segments))
        params.extend(segments)
    if employee_scale:
        where.append("employee_scale = ?")
        params.append(employee_scale)
    if region:
        where.append("region = ?")
        params.append(region)
    if keyword:
        where.append("(name LIKE ? OR industry_name LIKE ?)")
        params.extend([f"%{keyword}%", f"%{keyword}%"])

    clause = " WHERE " + " AND ".join(where) if where else ""

    conn = connect()
    try:
        total = conn.execute(
            "SELECT COUNT(*) FROM enterprise" + clause, params
        ).fetchone()[0]

        rows = conn.execute(
            "SELECT * FROM enterprise" + clause +
            " ORDER BY id LIMIT ? OFFSET ?",
            params + [page_size, (page - 1) * page_size],
        ).fetchall()
    finally:
        conn.close()

    items = []
    for r in rows:
        reasons = []
        if industry_codes:
            reasons.append("行业=" + r["industry_name"])
        if segments:
            reasons.append("环节=" + r["chain_segment"])
        if employee_scale:
            reasons.append("规模=" + r["employee_scale"])
        if region:
            reasons.append("地域=" + r["region"])
        if keyword:
            reasons.append("关键词=" + keyword)

        item = {f: r[f] for f in B1_FIELDS}
        item["match_reasons"] = reasons or ["未设筛选条件，返回全部企业"]
        items.append(item)

    return {"total": total, "page": page, "page_size": page_size, "items": items}


def enterprise_profile(enterprise_id):
    """D3 企业画像。6 维度固定，每维度带 provenance；缺失维度为 null 并列入 missing_dims。不下结论、不评分。"""
    conn = connect()
    try:
        r = conn.execute(
            "SELECT * FROM enterprise WHERE id = ?", (enterprise_id,)
        ).fetchone()
    finally:
        conn.close()

    if r is None:
        return None

    source = r["source"] or "未知来源"

    def parse(value):
        if not value:
            return None
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return value

    def dim(values, fields, extra=""):
        """有任一值时返回该维度内容+来源，否则返回 None。"""
        if not any(v is not None and v != "" and v != [] for v in values.values()):
            return None
        provenance = "enterprise." + " / enterprise.".join(fields) + f"，来源：{source}"
        if extra:
            provenance += "；" + extra
        return {**values, "provenance": provenance}

    dimensions = {
        "基础信息": dim(
            {
                "founded_year": r["founded_year"],
                "legal_person": r["legal_person"],
                "reg_capital": r["reg_capital"],
                "credit_code": r["credit_code"],
            },
            ["founded_year", "legal_person", "reg_capital", "credit_code"],
        ),
        "经营规模": dim(
            {"employee_scale": r["employee_scale"], "revenue_scale": r["revenue_scale"]},
            ["employee_scale", "revenue_scale"],
        ),
        "行业环节": dim(
            {
                "industry_code": r["industry_code"],
                "industry_name": r["industry_name"],
                "chain_segment": r["chain_segment"],
            },
            ["industry_code", "industry_name", "chain_segment"],
            "环节按环节字典归一化",
        ),
        "地域布局": dim(
            {"region": r["region"], "production_bases": parse(r["production_bases"])},
            ["region", "production_bases"],
        ),
        "技术/资质": dim(
            {"tech_qualifications": parse(r["tech_qualifications"])},
            ["tech_qualifications"],
        ),
        "投资动向": dim(
            {"investment_events": parse(r["investment_events"])},
            ["investment_events"],
        ),
    }

    missing_dims = [k for k, v in dimensions.items() if v is None]

    return {
        "enterprise_id": r["id"],
        "name": r["name"],
        "dimensions": dimensions,
        "missing_dims": missing_dims,
    }


def segment_coverage(region=None):
    """C1 环节覆盖统计。只给数量与占比，不判定短板。"""
    conn = connect()
    try:
        if region:
            rows = conn.execute(
                "SELECT chain_segment AS segment, COUNT(*) AS count FROM enterprise "
                "WHERE region = ? GROUP BY chain_segment ORDER BY chain_segment",
                (region,),
            ).fetchall()
            total = conn.execute(
                "SELECT COUNT(*) FROM enterprise WHERE region = ?", (region,)
            ).fetchone()[0]
        else:
            rows = conn.execute(
                "SELECT chain_segment AS segment, COUNT(*) AS count FROM enterprise "
                "GROUP BY chain_segment"
            ).fetchall()
            total = conn.execute("SELECT COUNT(*) FROM enterprise").fetchone()[0]
    finally:
        conn.close()

    segments = []
    for r in rows:
        segments.append({
            "segment": r["segment"],
            "count": r["count"],
            "ratio": round(r["count"] / total, 4) if total else 0,
        })
    return {"segments": segments, "total": total}


def match_policies(enterprise_id=None, industry=None, region=None):
    """C2 政策匹配检索。按企业或行业+地域检索，返回匹配理由，不生成方案。"""
    conn = connect()
    try:
        if enterprise_id is not None:
            ent = conn.execute(
                "SELECT industry_name, region FROM enterprise WHERE id = ?", (enterprise_id,)
            ).fetchone()
            if ent is None:
                return None
            industry = industry or ent["industry_name"]
            region = region or ent["region"]

        where, params = [], []
        if industry:
            # 政策行业可能是泛类（集成电路），企业行业是细分（集成电路设计）
            where.append("(? LIKE '%' || industry || '%' OR industry LIKE '%' || ? || '%' "
                         "OR industry IS NULL OR industry = '')")
            params.extend([industry, industry])
        if region:
            # 富阳、萧山属杭州，用前缀匹配兼容市辖区
            where.append("(region = ? OR ? LIKE region || '%' OR region IS NULL OR region = '')")
            params.extend([region, region])

        clause = " WHERE " + " AND ".join(where) if where else ""
        rows = conn.execute("SELECT * FROM policy" + clause, params).fetchall()
    finally:
        conn.close()

    items = []
    for r in rows:
        reasons = []
        if industry and r["industry"]:
            reasons.append("行业=" + r["industry"])
        elif industry:
            reasons.append("行业=通用")
        if region and r["region"]:
            reasons.append("地域=" + r["region"])
        elif region:
            reasons.append("地域=通用")
        items.append({
            "id": r["id"],
            "title": r["title"],
            "policy_type": r["policy_type"],
            "content": r["content"],
            "source_url": r["source_url"],
            "match_reasons": reasons or ["未设条件，返回全部政策"],
        })
    return {"items": items}
