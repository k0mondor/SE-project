/* ============================================================
 * 真实接口客户端（对接数据岗 v1.0 + 本岗方案后端）
 * ------------------------------------------------------------
 * 启用方式：index.html 中把
 *   <script src="mock-api.js"></script>
 * 换成
 *   <script src="api-client.js"></script>
 * 页面统一通过 window.MockAPI 调用，方法签名与 mock-api.js 一致。
 *
 * 上游（数据岗，已落地，基址 UPSTREAM_BASE）：
 *   B1  GET /enterprises?chain_segment=&keyword=
 *   B2  GET /enterprises/{id}/profile
 *   C1  GET /data/segments/coverage
 *   C2  GET /policies/match?enterprise_id=
 * 本岗后端（方案台账 / 生成 / 核验 / 导出，基址 PLAN_BASE）：
 *   /plans /plans/{id} /plans/generate /plans/{id}/status
 *   /plans/{id}/regenerate /plans/{id}/export
 *
 * D1 短板、D4 评分接口尚未交付：短板列表由 C1 临时派生；评分 fit_score 为 null。
 * 作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
 * ============================================================ */

const UPSTREAM_BASE = "http://127.0.0.1:8000/api/v1";
const PLAN_BASE = "/api/v1";

async function request(base, path, options = {}) {
  const resp = await fetch(base + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await resp.json().catch(() => ({ code: -1, message: "响应解析失败", data: null }));
  if (body.code !== 0) throw new Error(body.message || `请求失败：${resp.status}`);
  return body.data;
}

/* ---------- 上游响应 → 看板视图模型（VM） ---------- */

function normalizeDimension(dim) {
  if (!dim) return { value: null, source: null };
  const { provenance, ...value } = dim;
  return { value: Object.keys(value).length ? value : null, source: provenance || null };
}

function normalizeProfile(profileData) {
  if (!profileData) {
    const empty = { value: null, source: null };
    return { basic: { ...empty }, scale: { ...empty }, link: { ...empty },
      region: { ...empty }, tech: { ...empty }, investment: { ...empty } };
  }
  const d = profileData.dimensions || {};
  const techRaw = d["技术/资质"] || {};
  const techQ = techRaw.tech_qualifications;
  const investmentRaw = d["投资动向"] || {};
  const events = investmentRaw.investment_events;
  return {
    basic: normalizeDimension(d["基础信息"]),
    scale: normalizeDimension(d["经营规模"]),
    link: normalizeDimension(d["行业环节"]),
    region: normalizeDimension(d["地域布局"]),
    tech: {
      value: techQ ? { patents: techQ["专利数"], qualifications: techQ["资质"] || [] } : null,
      source: techRaw.provenance || null,
    },
    investment: {
      value: events && events.length ? { recent_move: events.map(e => e["事件"] || "").filter(Boolean).join("；") } : null,
      source: investmentRaw.provenance || null,
    },
  };
}

function normalizeEnterprise(item, profileData) {
  return {
    enterprise_id: item.id,
    name: item.name,
    link_node: item.chain_segment,
    shortboard_id: "SB-" + (item.chain_segment || ""),
    tags: [item.industry_name, item.region, item.employee_scale].filter(Boolean),
    fit_score: null, // D4 接口未交付
    dimension_scores: {},
    hit_reason: (item.match_reasons || []).join("；"),
    risk_note: null,
    profile: normalizeProfile(profileData),
  };
}

/* ---------- 本岗方案后端适配（台账数据缓存于页面内存） ---------- */

const PLAN_CACHE = { plans: [] };

function cachePlan(plan) {
  const idx = PLAN_CACHE.plans.findIndex(p => p.plan_id === plan.plan_id);
  if (idx >= 0) PLAN_CACHE.plans[idx] = plan; else PLAN_CACHE.plans.unshift(plan);
  return plan;
}

const ApiClient = {
  // D1 未交付：由 C1 环节覆盖统计临时派生任务
  async listShortboards() {
    const data = await request(UPSTREAM_BASE, "/data/segments/coverage");
    const segments = (data.segments || []).slice().sort((a, b) => a.count - b.count);
    const tasks = segments.slice(0, 2).map((seg, idx) => ({
      shortboard_id: "SB-" + seg.segment,
      link_node: seg.segment,
      gap_type: seg.ratio < 0.1 ? "薄弱环节" : "配套缺口",
      priority: idx === 0 ? "高" : "中",
      gap_desc: `${seg.segment}环节本地企业 ${seg.count} 家，占比 ${(seg.ratio * 100).toFixed(0)}%；短板判定以 D1 结论为准。`,
      basis_source: "C1 环节覆盖统计（D1 接口未交付，临时派生）",
      candidate_count: seg.count,
      plan_done_count: 0,
    }));
    DB.shortboards = tasks;
    return tasks;
  },

  // B1 候选 + B2 画像；D4 评分待接口
  async listCandidates(shortboardId) {
    const segment = shortboardId ? shortboardId.replace("SB-", "") : null;
    const params = new URLSearchParams({ page: "1", page_size: "100" });
    if (segment) params.set("chain_segment", segment);
    const data = await request(UPSTREAM_BASE, "/enterprises?" + params.toString());
    const items = data.items || [];
    const list = await Promise.all(items.map(async (item) => {
      let profile = null;
      try { profile = await request(UPSTREAM_BASE, `/enterprises/${item.id}/profile`); } catch (e) { profile = null; }
      return normalizeEnterprise(item, profile);
    }));
    DB.enterprises = list;
    return list;
  },

  async listPlans() {
    const data = await request(PLAN_BASE, "/plans");
    PLAN_CACHE.plans = (data.items || []).map(cachePlan);
    return PLAN_CACHE.plans;
  },

  async getPlan(planId) {
    return PLAN_CACHE.plans.find(p => p.plan_id === planId) || null;
  },

  async generatePlan(enterpriseId, shortboardId) {
    const plan = await request(PLAN_BASE, "/plans/generate", {
      method: "POST",
      body: JSON.stringify({ enterprise_id: enterpriseId, shortboard_id: shortboardId, mode: "auto" }),
    });
    return cachePlan(plan);
  },

  async regenerate(planId) {
    const old = PLAN_CACHE.plans.find(p => p.plan_id === planId);
    const plan = await request(PLAN_BASE, `/plans/${encodeURIComponent(planId)}/regenerate`, {
      method: "POST",
      body: JSON.stringify({ enterprise_id: old.enterprise_id, shortboard_id: old.shortboard_id, mode: "auto" }),
    });
    return cachePlan(plan);
  },

  async changeStatus(planId, action, comment) {
    const plan = await request(PLAN_BASE, `/plans/${encodeURIComponent(planId)}/status`, {
      method: "PUT",
      body: JSON.stringify({ action, comment: comment || null }),
    });
    return cachePlan(plan);
  },

  async exportPlan(planId) {
    const data = await request(PLAN_BASE, `/plans/${encodeURIComponent(planId)}/export?format=markdown`);
    return data.markdown;
  },
};

window.DB = PLAN_CACHE;
window.MockAPI = ApiClient;
