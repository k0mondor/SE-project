"""方案台账仓储 · 内存占位实现。

本岗自建的方案台账（生成 / 版本 / 核验 / 导出）持久化归本模块；
接共享数据库后替换为表实现，路由与服务逻辑不变。

作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
"""

from datetime import datetime

from schemas import PlanDetail, PlanStatus, ReviewAction


class InMemoryPlanRepository:
    def __init__(self):
        self._plans: dict[str, PlanDetail] = {}
        self._seq = 0

    # ---------- 编号 / 存取 ----------

    def next_plan_id(self) -> str:
        self._seq += 1
        return f"PL-2026-{self._seq:04d}"

    def save_plan(self, plan: PlanDetail) -> None:
        self._plans[plan.plan_id] = plan

    def get_plan(self, plan_id: str) -> PlanDetail | None:
        return self._plans.get(plan_id)

    def list_plans(self, shortboard_id: str | None = None, status: str | None = None,
                   keyword: str | None = None) -> list[PlanDetail]:
        items = list(self._plans.values())
        if shortboard_id:
            items = [p for p in items if p.shortboard_id == shortboard_id]
        if status:
            items = [p for p in items if p.status == status]
        if keyword:
            items = [p for p in items if keyword in p.plan_id]
        return sorted(items, key=lambda p: p.updated_at, reverse=True)

    # ---------- 核验流转 ----------

    def apply_review(self, plan_id: str, action: ReviewAction, comment: str | None) -> PlanDetail:
        plan = self._plans[plan_id]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        allowed = {
            ReviewAction.SUBMIT: {PlanStatus.DRAFT},
            ReviewAction.FINALIZE: {PlanStatus.IN_REVIEW},
            ReviewAction.REJECT: {PlanStatus.IN_REVIEW},
        }
        if plan.status not in allowed[action]:
            raise ValueError("40902:状态非法跳转")
        if action == ReviewAction.REJECT and not comment:
            raise ValueError("40011:驳回意见必填")

        if action == ReviewAction.SUBMIT:
            plan.status = PlanStatus.IN_REVIEW
        elif action == ReviewAction.FINALIZE:
            plan.status = PlanStatus.FINALIZED
            plan.review.reviewer = "专班规划人员"
            plan.review.reviewed_at = now
            plan.review.comment = comment or "数据与政策来源核对一致，同意定稿。"
        else:  # REJECT
            plan.status = PlanStatus.DRAFT
            plan.review.reviewer = "专班规划人员"
            plan.review.reviewed_at = now
            plan.review.comment = comment
        plan.updated_at = now
        return plan

    def archive_old_version(self, plan_id: str) -> None:
        old = self._plans[plan_id]
        for v in old.versions:
            v.status = PlanStatus.ARCHIVED

    # ---------- 导出 ----------

    def export_markdown(self, plan: PlanDetail) -> str:
        p = plan.plan
        lines = [
            f"# 招商方案 · {plan.enterprise_id}",
            "",
            f"方案编号：{plan.plan_id}　|　补链任务：{plan.shortboard_id}　|　状态：{plan.status.value}",
            f"|　生成方式：{plan.generator.value}",
            "", "## 一、推介要点",
            *[f"- {h}" for h in p.highlights],
            "", "## 二、匹配政策包",
            *[f"### {po.name}\n- 条款：{po.clause}\n- 匹配维度：{po.match_dimension}\n"
              f"- 匹配理由：{po.match_reason}\n- 来源：{po.source or '—'}"
              for po in p.matched_policies],
            "", "## 三、谈判策略",
            *[f"- {n}" for n in p.negotiation_points],
            "", "## 四、分步行动计划",
            *[f"### {s.stage}\n- {'；'.join(s.actions)}\n"
              f"- 建议责任：{s.owner_suggest or '—'}　时间建议：{s.timeline or '—'}"
              for s in p.action_steps],
            "", "## 五、核验信息",
            f"- 核验人：{plan.review.reviewer or '待核验'}　核验时间：{plan.review.reviewed_at or '—'}",
            f"- 意见：{plan.review.comment or '—'}",
            "", "> 本文档数据取自业务数据库；AI 生成内容已经/待人工核验。",
        ]
        return "\n".join(lines)
