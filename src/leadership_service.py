from contextlib import closing

from src.db import connect
from src.query_service import segment_coverage

WEAK_THRESHOLD_PERCENT = 10

RECOMMENDATIONS = {
    "芯片设计": "摸排与本地制造、封装工艺匹配的芯片设计企业。",
    "晶圆制造": "摸排与本地设计企业工艺需求匹配的晶圆代工及特色工艺项目。",
    "先进封装": "摸排先进封装、可靠性验证和测试服务项目。",
    "半导体设备": "摸排与本地晶圆产线和封测产线匹配的设备及服务商。",
    "半导体材料": "摸排与本地制造工艺匹配的关键材料供应商。",
}

# 以基础环节覆盖度筛查潜在配套缺口，具体工艺和供需关系需要核验。
SUPPORT_CHECKS = (
    ("芯片设计", "晶圆制造", "核验设计企业的流片需求与本地可用工艺。"),
    ("芯片设计", "先进封装", "核验设计企业所需的封装形式与本地测试能力。"),
    ("晶圆制造", "半导体设备", "核验本地制造工艺所需设备与维保能力。"),
    ("晶圆制造", "半导体材料", "核验本地制造工艺所需的关键材料及供应能力。"),
)


def diagnose_shortages(region=None, include_subregions=False):
    with closing(connect()) as conn, conn:
        conn.execute("BEGIN")
        definitions = conn.execute(
            "SELECT id, name, definition FROM chain_segment ORDER BY id"
        ).fetchall()
        coverage = segment_coverage(region, include_subregions, connection=conn)

    total = coverage["total"]
    counts = {row["segment"]: row["count"] for row in coverage["segments"]}
    segments = []
    for definition in definitions:
        name = definition["name"]
        count = counts.get(name, 0)
        ratio = count / total if total else None
        status = "covered"
        if not total:
            status = "no_data"
        elif count == 0:
            status = "missing"
        elif count * 100 < total * WEAK_THRESHOLD_PERCENT:
            status = "weak"

        segments.append({
            "id": definition["id"],
            "segment": name,
            "definition": definition["definition"],
            "count": count,
            "ratio": ratio,
            "status": status,
            "evidence": {
                "enterprise_count": count,
                "sample_count": total,
                "rule": status,
                "threshold_percent": WEAK_THRESHOLD_PERCENT,
                "source": "企业名录、产业链环节字典",
            },
            "recommendation": (
                RECOMMENDATIONS.get(name, f"核验{name}环节的本地需求并摸排候选企业。")
                if status in ("missing", "weak") else None
            ),
        })

    shortages = sorted(
        (item for item in segments if item["status"] in ("missing", "weak")),
        key=lambda item: (item["count"], item["id"]),
    )
    by_name = {item["segment"]: item for item in segments}
    support_gaps = []
    for demand_name, supply_name, recommendation in SUPPORT_CHECKS:
        demand = by_name.get(demand_name)
        supply = by_name.get(supply_name)
        if demand and demand["count"] and supply and supply["status"] in ("missing", "weak"):
            support_gaps.append({
                "demand_segment": demand_name,
                "demand_count": demand["count"],
                "supply_segment": supply_name,
                "supply_count": supply["count"],
                "supply_status": supply["status"],
                "status": "pending_verification",
                "recommendation": recommendation,
            })

    return {
        "region": region,
        "include_subregions": bool(region and include_subregions),
        "total": total,
        "covered_count": sum(item["count"] > 0 for item in segments),
        "unclassified_count": total - sum(item["count"] for item in segments),
        "threshold_percent": WEAK_THRESHOLD_PERCENT,
        "segments": segments,
        "shortages": shortages,
        "support_gaps": support_gaps,
    }
