"""D5 方案生成服务 · 数据模型。

上游只读字段对齐《数据岗接口契约 v1.0》（B1/B2/C1/C2 已落地）；
D1 短板、D4 评分接口尚未交付，对应模型按预留口径保留，字段可空。
方案内部结构与规划人员看板对应。

作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PlanStatus(str, Enum):
    PENDING = "pending"          # 待生成
    DRAFT = "draft"             # 草稿（AI / 模板产出，待核验）
    IN_REVIEW = "in_review"     # 待审核
    FINALIZED = "finalized"     # 已定稿
    FAILED = "failed"           # 生成失败
    ARCHIVED = "archived"       # 旧版本归档


class Generator(str, Enum):
    LLM = "llm"
    TEMPLATE = "template"


class ReviewAction(str, Enum):
    SUBMIT = "submit"
    FINALIZE = "finalize"
    REJECT = "reject"


# ---------- 上游只读数据（数据岗 v1.0，已落地） ----------

class EnterpriseListItem(BaseModel):
    """B1 GET /api/v1/enterprises 列表项。"""
    id: int
    name: str
    industry_code: Optional[str] = None
    industry_name: Optional[str] = None
    chain_segment: Optional[str] = None
    region: Optional[str] = None
    employee_scale: Optional[str] = None
    revenue_scale: Optional[str] = None
    production_bases: Optional[list] = None
    tech_qualifications: Optional[dict] = None
    investment_events: Optional[list] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    match_reasons: list[str] = Field(default_factory=list)


class EnterpriseProfile(BaseModel):
    """B2 GET /api/v1/enterprises/{id}/profile，6 维中文键，每维带 provenance。"""
    enterprise_id: int
    name: str
    dimensions: dict[str, Optional[dict]]
    missing_dims: list[str] = Field(default_factory=list)


class PolicyItem(BaseModel):
    """C2 GET /api/v1/policies/match 列表项。"""
    id: int
    title: str
    policy_type: Optional[str] = None
    content: Optional[str] = None
    source_url: Optional[str] = None
    match_reasons: list[str] = Field(default_factory=list)


class SegmentCoverage(BaseModel):
    """C1 GET /api/v1/data/segments/coverage 统计项。"""
    segment: str
    count: int
    ratio: float


# ---------- 上游预留（D1 / D4 接口未交付，字段可空） ----------

class ScoreResult(BaseModel):
    """D4 适配评分。接口未交付前 fit_score 为 None，方案按画像生成并标注评分待补。"""
    enterprise_id: int
    fit_score: Optional[float] = None
    reasons: list[str] = Field(default_factory=list)
    risk_note: Optional[str] = None
    score_version: Optional[str] = None
    scored_at: Optional[str] = None


class ShortboardItem(BaseModel):
    """D1 补链任务。接口未交付前可由 C1 环节覆盖统计临时派生，待 D1 确认短板判定口径。"""
    shortboard_id: str
    link_node: str
    gap_type: Optional[str] = None
    priority: Optional[str] = None
    gap_desc: Optional[str] = None
    basis_source: Optional[str] = None
    candidate_count: int = 0
    plan_done_count: int = 0


# ---------- 方案内部结构 ----------

class MatchedPolicy(BaseModel):
    policy_id: int
    name: str
    clause: str
    match_dimension: str
    match_reason: str
    source: Optional[str] = None


class ActionStep(BaseModel):
    stage: str
    actions: list[str] = Field(default_factory=list)
    owner_suggest: Optional[str] = None
    timeline: Optional[str] = None


class PlanBody(BaseModel):
    highlights: list[str] = Field(default_factory=list)
    matched_policies: list[MatchedPolicy] = Field(default_factory=list)
    negotiation_points: list[str] = Field(default_factory=list)
    action_steps: list[ActionStep] = Field(default_factory=list)


class ReviewInfo(BaseModel):
    reviewer: Optional[str] = None
    reviewed_at: Optional[str] = None
    comment: Optional[str] = None


class PlanVersion(BaseModel):
    version_no: int
    generator: Generator
    created_at: str
    status: PlanStatus
    note: Optional[str] = None


class PlanDetail(BaseModel):
    plan_id: str
    enterprise_id: int
    shortboard_id: str
    status: PlanStatus
    current_version_no: int
    generator: Generator
    model_version: Optional[str] = None
    template_id: Optional[str] = None
    created_at: str
    updated_at: str
    plan: PlanBody
    review: ReviewInfo = Field(default_factory=ReviewInfo)
    versions: list[PlanVersion] = Field(default_factory=list)
    context_ref: dict = Field(default_factory=dict)
    trace: dict = Field(default_factory=dict)


# ---------- 请求 ----------

class GenerateRequest(BaseModel):
    enterprise_id: int
    shortboard_id: str
    template_id: str = "TPL-ONE-COMPANY-v1"
    mode: str = "auto"          # auto / llm / template
    policy_limit: int = 5


class StatusRequest(BaseModel):
    action: ReviewAction
    comment: Optional[str] = None
