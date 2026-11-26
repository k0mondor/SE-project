"""政策匹配：优先采用数据岗 C2 检索结果，本模块做维度归纳与本地兜底。

- C2（GET /api/v1/policies/match）已按行业、地域召回并给出 match_reasons，
  正常路径直接沿用其命中理由，不再重复检索；
- C2 不可用时，按行业、地域、资质关键词做本地规则兜底；
- 语义检索（Embedding / 向量库）为可选增强，未接入时仅返回规则结果并标注。

作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
"""

from dataclasses import dataclass

from schemas import EnterpriseProfile, MatchedPolicy, PolicyItem


def _dimension_from_reasons(reasons: list[str]) -> str:
    dims: list[str] = []
    joined = "、".join(reasons)
    if "行业" in joined:
        dims.append("行业环节")
    if "地域" in joined:
        dims.append("地域布局")
    if any(k in joined for k in ("资质", "规模", "要素")):
        dims.append("要素资质")
    return "、".join(dims) if dims else "政策适用"


def _fallback_hit(profile: EnterpriseProfile, policy: PolicyItem) -> list[str]:
    """C2 不可用时的本地粗匹配：行业 / 地域 / 资质关键词。"""
    reasons: list[str] = []
    link = (profile.dimensions.get("行业环节") or {})
    region = (profile.dimensions.get("地域布局") or {})
    tech = (profile.dimensions.get("技术/资质") or {})

    industry_name = str(link.get("industry_name") or "")
    if industry_name and (not policy.title or industry_name in policy.title or "集成电路" in policy.title):
        reasons.append("行业=" + industry_name)
    if region.get("region"):
        reasons.append("地域=" + str(region["region"]))
    qualifications = (tech.get("tech_qualifications") or {})
    if isinstance(qualifications, dict) and qualifications.get("资质"):
        reasons.append("资质=" + "、".join(map(str, qualifications["资质"])))
    return reasons


@dataclass
class MatchScore:
    policy: PolicyItem
    dimension: str
    reason: str
    score: float


def match_policies(
    profile: EnterpriseProfile,
    policies: list[PolicyItem],
    limit: int = 5,
    use_upstream_reasons: bool = True,
) -> list[MatchedPolicy]:
    """归纳政策匹配结果，按命中维度数排序，截断到 limit。"""
    scored: dict[int, MatchScore] = {}

    for policy in policies:
        reasons = policy.match_reasons if use_upstream_reasons else _fallback_hit(profile, policy)
        if not reasons:
            continue
        dimension = _dimension_from_reasons(reasons)
        reason = "；".join(reasons)
        scored[policy.id] = MatchScore(
            policy, dimension, reason, score=0.6 + 0.1 * len(reasons)
        )

    ordered = sorted(scored.values(), key=lambda m: m.score, reverse=True)[:limit]
    return [
        MatchedPolicy(
            policy_id=m.policy.id,
            name=m.policy.title,
            clause=m.policy.content or "",
            match_dimension=m.dimension,
            match_reason=m.reason,
            source=m.policy.source_url,
        )
        for m in ordered
    ]
