"""上游只读仓储 · HTTP 实现。

对接数据岗《接口契约 v1.0》已落地接口（基址默认 http://127.0.0.1:8000/api/v1）：
- B1 GET /enterprises            企业组合筛选
- B2 GET /enterprises/{id}/profile  6 维画像
- C1 GET /data/segments/coverage    环节覆盖统计
- C2 GET /policies/match           政策匹配检索

D1 短板判定、D4 适配评分接口尚未交付：
- 短板列表临时由 C1 统计派生（仅按企业数量多少提示，不等于 D1 短板结论）；
- 评分返回 fit_score=None，方案按画像生成并标注"评分待补"，D4 接口到位后恢复校验。

作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
"""

import json
import urllib.parse
import urllib.request

from schemas import (
    EnterpriseListItem,
    EnterpriseProfile,
    PolicyItem,
    ScoreResult,
    ShortboardItem,
)


class UpstreamError(RuntimeError):
    """上游接口返回非 0 code 或网络 / 解析异常。"""


class HttpUpstreamRepository:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api/v1", timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # ---------- 基础请求 ----------

    def _get(self, path: str, params: dict | None = None):
        if params:
            query = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
            path = f"{path}?{query}" if query else path
        url = self.base_url + path
        try:
            with urllib.request.urlopen(url, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # 网络层异常统一上抛，由方案服务决定降级
            raise UpstreamError(f"上游请求失败：{url}：{exc}") from exc
        if body.get("code") != 0:
            raise UpstreamError(body.get("message", f"上游错误 code={body.get('code')}"))
        return body.get("data")

    # ---------- D1 短板（接口未交付，C1 派生） ----------

    def list_shortboards(self) -> list[ShortboardItem]:
        data = self._get("/data/segments/coverage")
        segments = data.get("segments", [])
        # 临时派生：企业数最少的两个环节标为薄弱环节；不替代 D1 短板判定结论
        ordered = sorted(segments, key=lambda s: s["count"])
        items: list[ShortboardItem] = []
        for idx, seg in enumerate(ordered[:2]):
            ratio = seg["ratio"]
            gap_type = "薄弱环节" if ratio < 0.1 else "配套缺口"
            priority = "高" if idx == 0 else "中"
            items.append(ShortboardItem(
                shortboard_id="SB-" + seg["segment"],
                link_node=seg["segment"],
                gap_type=gap_type,
                priority=priority,
                gap_desc=f"{seg['segment']}环节本地企业 {seg['count']} 家，占比 {ratio:.0%}；"
                         f"短板判定以 D1 短板识别结论为准。",
                basis_source="C1 环节覆盖统计（D1 接口未交付，临时派生）",
                candidate_count=seg["count"],
                plan_done_count=0,
            ))
        return items

    def get_shortboard(self, shortboard_id: str) -> ShortboardItem:
        for item in self.list_shortboards():
            if item.shortboard_id == shortboard_id:
                return item
        raise UpstreamError(f"补链任务不存在：{shortboard_id}")

    # ---------- B1 候选企业 ----------

    def list_candidates(self, shortboard_id: str | None = None,
                        region: str | None = None, keyword: str | None = None) -> list[EnterpriseListItem]:
        params: dict = {"page": 1, "page_size": 100}
        if shortboard_id:
            segment = shortboard_id.replace("SB-", "", 1)
            params["chain_segment"] = segment
        if region:
            params["region"] = region
        if keyword:
            params["keyword"] = keyword
        data = self._get("/enterprises", params)
        return [EnterpriseListItem(**item) for item in data.get("items", [])]

    # ---------- B2 画像 ----------

    def get_profile(self, enterprise_id: int) -> EnterpriseProfile:
        data = self._get(f"/enterprises/{enterprise_id}/profile")
        return EnterpriseProfile(**data)

    # ---------- D4 评分（未交付占位） ----------

    def get_score(self, enterprise_id: int) -> ScoreResult:
        # TODO: D4 评分接口交付后，改为 GET /enterprises/{id}/score 并回填 fit_score/reasons/risk_note
        return ScoreResult(enterprise_id=enterprise_id, fit_score=None)

    # ---------- C2 政策匹配 ----------

    def get_policies(self, enterprise_id: int, limit: int = 5) -> list[PolicyItem]:
        data = self._get("/policies/match", {"enterprise_id": enterprise_id})
        items = data.get("items", [])[:limit]
        return [PolicyItem(**item) for item in items]
