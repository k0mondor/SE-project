"""FastAPI 路由 · 规划人员看板 / D5 方案生成。

上游只读数据走数据岗 v1.0 接口（B1/B2/C1/C2）；方案台账、生成、核验、
导出为本岗自建。仓储与 LLM 客户端通过依赖注入替换，本期用内存仓储 + 模板兜底。

作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
"""

from fastapi import APIRouter, Depends, HTTPException

from plan_repo import InMemoryPlanRepository
from plan_service import generate_plan
from schemas import GenerateRequest, PlanDetail, StatusRequest
from upstream_http import HttpUpstreamRepository, UpstreamError

router = APIRouter(prefix="/api/v1", tags=["planning"])

_upstream = HttpUpstreamRepository()
_plan_repo = InMemoryPlanRepository()


def get_upstream() -> HttpUpstreamRepository:
    return _upstream


def get_plan_repo() -> InMemoryPlanRepository:
    return _plan_repo


def get_llm():
    """返回 LlmClient 实现；未配置 Key 时返回 None，服务走模板兜底。"""
    return None


def _upstream_error(exc: UpstreamError) -> HTTPException:
    return HTTPException(status_code=502, detail={"code": 50200, "message": str(exc)})


# ---------- 上游只读（透传 / 聚合数据岗接口） ----------

@router.get("/planning/shortboards")
def list_shortboards(repo=Depends(get_upstream)):
    try:
        return {"code": 0, "message": "ok", "data": [s.model_dump() for s in repo.list_shortboards()]}
    except UpstreamError as exc:
        raise _upstream_error(exc)


@router.get("/planning/candidates")
def list_candidates(shortboard_id: str | None = None, repo=Depends(get_upstream)):
    try:
        items = repo.list_candidates(shortboard_id)
        return {"code": 0, "message": "ok", "data": {"total": len(items),
                "items": [e.model_dump() for e in items]}}
    except UpstreamError as exc:
        raise _upstream_error(exc)


@router.get("/enterprises/{enterprise_id}/profile")
def get_profile(enterprise_id: int, repo=Depends(get_upstream)):
    try:
        return {"code": 0, "message": "ok", "data": repo.get_profile(enterprise_id).model_dump()}
    except UpstreamError as exc:
        raise _upstream_error(exc)


@router.get("/enterprises/{enterprise_id}/score")
def get_score(enterprise_id: int, repo=Depends(get_upstream)):
    # D4 接口未交付：返回占位评分，fit_score 为 null；到位后此路由接 D4 结果
    try:
        return {"code": 0, "message": "ok", "data": repo.get_score(enterprise_id).model_dump()}
    except UpstreamError as exc:
        raise _upstream_error(exc)


@router.get("/policies/match")
def list_policies(enterprise_id: int, limit: int = 5, repo=Depends(get_upstream)):
    try:
        items = repo.get_policies(enterprise_id, limit)
        return {"code": 0, "message": "ok", "data": {"items": [p.model_dump() for p in items]}}
    except UpstreamError as exc:
        raise _upstream_error(exc)


# ---------- 方案台账（本岗自建） ----------

@router.post("/plans/generate", response_model=PlanDetail)
def create_plan(req: GenerateRequest,
                upstream=Depends(get_upstream),
                repo=Depends(get_plan_repo),
                llm=Depends(get_llm)):
    try:
        detail = generate_plan(
            plan_id=repo.next_plan_id(),
            enterprise_id=req.enterprise_id,
            shortboard_id=req.shortboard_id,
            repo=upstream,
            llm=llm,
            template_id=req.template_id,
            mode=req.mode,
            policy_limit=req.policy_limit,
        )
    except UpstreamError as exc:
        raise _upstream_error(exc)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail={"code": 40010, "message": str(exc)})
    repo.save_plan(detail)
    return detail


@router.get("/plans")
def list_plans(shortboard_id: str | None = None, status: str | None = None,
               repo=Depends(get_plan_repo)):
    items = repo.list_plans(shortboard_id, status)
    return {"code": 0, "message": "ok", "data": {"total": len(items),
            "items": [p.model_dump() for p in items]}}


@router.get("/plans/{plan_id}", response_model=PlanDetail)
def get_plan(plan_id: str, repo=Depends(get_plan_repo)):
    plan = repo.get_plan(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail={"code": 40404, "message": "方案不存在"})
    return plan


@router.put("/plans/{plan_id}/status", response_model=PlanDetail)
def change_status(plan_id: str, req: StatusRequest, repo=Depends(get_plan_repo)):
    plan = repo.get_plan(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail={"code": 40404, "message": "方案不存在"})
    try:
        return repo.apply_review(plan_id, req.action, req.comment)
    except ValueError as exc:
        code, _, msg = str(exc).partition(":")
        status = 409 if code == "40902" else 400
        raise HTTPException(status_code=status, detail={"code": code, "message": msg})


@router.post("/plans/{plan_id}/regenerate", response_model=PlanDetail)
def regenerate(plan_id: str, req: GenerateRequest,
               upstream=Depends(get_upstream),
               repo=Depends(get_plan_repo),
               llm=Depends(get_llm)):
    old = repo.get_plan(plan_id)
    if old is None:
        raise HTTPException(status_code=404, detail={"code": 40404, "message": "方案不存在"})
    try:
        new = generate_plan(
            plan_id=repo.next_plan_id(),
            enterprise_id=old.enterprise_id,
            shortboard_id=old.shortboard_id,
            repo=upstream,
            llm=llm,
            template_id=req.template_id,
            mode=req.mode,
            policy_limit=req.policy_limit,
        )
    except UpstreamError as exc:
        raise _upstream_error(exc)
    repo.archive_old_version(plan_id)
    repo.save_plan(new)
    return new


@router.get("/plans/{plan_id}/export")
def export_plan(plan_id: str, repo=Depends(get_plan_repo)):
    plan = repo.get_plan(plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail={"code": 40404, "message": "方案不存在"})
    return {"code": 0, "message": "ok", "data": {"markdown": repo.export_markdown(plan)}}
