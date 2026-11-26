"""D5 方案生成服务：上下文装配 → 校验 → LLM 生成 / 模板兜底 → 留痕。

LLM 客户端通过 ``LlmClient`` 抽象预留；接入真实 API 时替换实现即可，
校验、兜底与留痕逻辑不变。

上游对接数据岗 v1.0（B1/B2/C2 已落地）；D4 评分接口未交付前，
fit_score 为空不阻断生成，方案按画像组织并标注"评分待补"，接口到位后恢复校验。

作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
"""

from datetime import datetime
from typing import Optional, Protocol

from policy_matcher import match_policies
from schemas import (
    ActionStep,
    EnterpriseProfile,
    EnterpriseListItem,
    Generator,
    PlanBody,
    PlanDetail,
    PlanStatus,
    PolicyItem,
    ReviewInfo,
    ScoreResult,
    ShortboardItem,
)


class LlmUnavailableError(Exception):
    """LLM 调用失败 / 超时 / 结构非法且不可恢复。"""


class LlmClient(Protocol):
    def generate(self, prompt: str, template_id: str) -> dict:
        """返回符合 PlanBody 结构的 dict；失败抛 LlmUnavailableError。"""
        ...


class UpstreamRepository(Protocol):
    """上游数据读取协议：D1 短板 / D2 筛选 / D3 画像 / D4 评分 / 政策库。"""

    def list_shortboards(self) -> list[ShortboardItem]: ...
    def get_shortboard(self, shortboard_id: str) -> ShortboardItem: ...
    def list_candidates(self, shortboard_id: str | None) -> list[EnterpriseListItem]: ...
    def get_profile(self, enterprise_id: int) -> EnterpriseProfile: ...
    def get_score(self, enterprise_id: int) -> ScoreResult: ...
    def get_policies(self, enterprise_id: int, limit: int) -> list[PolicyItem]: ...


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _dim(profile: EnterpriseProfile, key: str) -> dict:
    return profile.dimensions.get(key) or {}


def _industry_name(profile: EnterpriseProfile) -> str:
    link = _dim(profile, "行业环节")
    return link.get("industry_name") or "相关业务"


def _validate_body(body: dict) -> PlanBody:
    """校验 LLM 输出结构；缺字段抛 LlmUnavailableError。"""
    if not isinstance(body, dict):
        raise LlmUnavailableError("返回不是 JSON 对象")
    if "highlights" not in body or "matched_policies" not in body:
        raise LlmUnavailableError("缺少必备字段")
    return PlanBody(**body)


def _fallback_body(
    profile: EnterpriseProfile,
    score: ScoreResult,
    shortboard: ShortboardItem,
    policies: list[PolicyItem],
) -> PlanBody:
    """规则模板兜底：素材全部来自数据库字段，不引入库外事实。"""
    highlights = [
        f"{profile.name}主营{_industry_name(profile)}，"
        f"可补本地{shortboard.link_node}环节缺口。",
    ]
    if score.fit_score is not None:
        highlights.append(f"适配总分 {score.fit_score}；评分理由：{'；'.join(score.reasons[:2])}。")
    else:
        highlights.append("适配评分待 D4 补充，方案要点以画像公开信息为准。")

    negotiation = ["以补链缺口为切入，介绍本地载体与配套条件。"]
    if score.risk_note:
        negotiation.append(f"如实回应风险关切：{score.risk_note}")

    steps = [
        ActionStep(stage="对接准备", actions=["核验企业扩产计划与投资规模", "准备政策包与载体方案"],
                   owner_suggest="招商专班", timeline="第 1–2 周"),
        ActionStep(stage="上门对接", actions=["拜访企业总部", "安排园区考察"],
                   owner_suggest="招商专班 + 园区", timeline="第 3–4 周"),
        ActionStep(stage="落地跟进", actions=["形成意向条款", "推动立项选址"],
                   owner_suggest="专班 + 决策层", timeline="第 5–8 周"),
    ]
    matched = match_policies(profile, policies)
    return PlanBody(highlights=highlights, matched_policies=matched,
                    negotiation_points=negotiation, action_steps=steps)


def _build_prompt(
    profile: EnterpriseProfile,
    score: ScoreResult,
    shortboard: ShortboardItem,
    policies: list[PolicyItem],
    template_id: str,
) -> str:
    policy_lines = "\n".join(
        f"- [{p.id}] {p.title}：{p.content or ''}" for p in policies
    )
    score_line = (
        f"适配总分 {score.fit_score}，理由：{'；'.join(score.reasons)}"
        if score.fit_score is not None else "评分尚未生成，仅依据画像事实组织方案"
    )
    return (
        f"# 角色\n你是产业链招商专班方案撰写助手，只能依据给定资料组织语言，"
        f"不得引入资料以外的企业事实、数据或政策条款。\n\n"
        f"# 给定资料\n短板结论：{shortboard.gap_desc}\n"
        f"企业画像：{profile.model_dump()}\n"
        f"评分与理由：{score_line}\n"
        f"政策候选集：\n{policy_lines}\n\n"
        f"# 任务\n输出 JSON：highlights / matched_policies / negotiation_points / action_steps；"
        f"政策只能引用候选集内 policy_id。模板版本：{template_id}"
    )


def generate_plan(
    plan_id: str,
    enterprise_id: int,
    shortboard_id: str,
    repo: UpstreamRepository,
    llm: Optional[LlmClient],
    template_id: str,
    mode: str,
    policy_limit: int,
) -> PlanDetail:
    """生成方案草稿。mode: auto / llm / template。"""
    shortboard = repo.get_shortboard(shortboard_id)
    profile = repo.get_profile(enterprise_id)
    score = repo.get_score(enterprise_id)

    score_status = "scored" if score.fit_score is not None else "missing"
    policies = repo.get_policies(enterprise_id, policy_limit)
    matched = match_policies(profile, policies, limit=policy_limit)

    generator = Generator.TEMPLATE
    model_version = None
    fallback_reason: Optional[str] = None
    body: Optional[PlanBody] = None

    if mode != "template" and llm is not None:
        try:
            prompt = _build_prompt(profile, score, shortboard, policies, template_id)
            raw = llm.generate(prompt, template_id)
            body = _validate_body(raw)
            # 政策引用二次校验：只保留候选集内条目
            valid_ids = {p.id for p in policies}
            body.matched_policies = [p for p in body.matched_policies if p.policy_id in valid_ids]
            generator = Generator.LLM
            model_version = getattr(llm, "model_version", "unknown")
        except LlmUnavailableError as exc:
            if mode == "llm":
                raise LlmUnavailableError(str(exc)) from exc
            fallback_reason = str(exc)

    if body is None:
        body = _fallback_body(profile, score, shortboard, policies)
        generator = Generator.TEMPLATE
        if fallback_reason is None:
            fallback_reason = "按模板模式生成"

    now = _now()
    return PlanDetail(
        plan_id=plan_id,
        enterprise_id=enterprise_id,
        shortboard_id=shortboard_id,
        status=PlanStatus.DRAFT,
        current_version_no=1,
        generator=generator,
        model_version=model_version,
        template_id=template_id,
        created_at=now,
        updated_at=now,
        plan=body,
        review=ReviewInfo(),
        context_ref={
            "profile_snapshot_id": f"PS-{enterprise_id}",
            "score_snapshot_id": f"SS-{enterprise_id}",
            "score_status": score_status,
            "shortboard_id": shortboard_id,
        },
        trace={"fallback_reason": fallback_reason, "template_id": template_id},
    )
