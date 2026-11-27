/* ============================================================
 * Mock 数据层（D1 / D4 接口未交付前的替换口）
 * ------------------------------------------------------------
 * 字段口径对齐数据岗《接口契约 v1.0》：
 *  - 企业列表对应 B1 /enterprises，画像对应 B2 /enterprises/{id}/profile
 *  - 政策对应 C2 /policies/match（id / title / policy_type / content / source_url）
 * 本文件把上游响应归一化为看板视图模型（VM）；真实接口走 api-client.js，
 * 页面渲染、状态流转、核验逻辑均不改动。
 * 方案台账 / 生成 / 核验 / 导出为本岗自建，内存维护。
 * 作者：赵帅臣（3240102154 · 软工 2402 班） · 方案生成岗
 * ============================================================ */

const DB = {
  shortboards: [
    { shortboard_id: "SB-半导体设备", link_node: "半导体设备", gap_type: "薄弱环节", priority: "高",
      gap_desc: "本地半导体设备环节企业 3 家，占比约 6%，设备配套能力不足；短板判定以 D1 结论为准。",
      basis_source: "C1 环节覆盖统计（D1 接口未交付，临时派生）", candidate_count: 3, plan_done_count: 1 },
    { shortboard_id: "SB-先进封装", link_node: "先进封装", gap_type: "薄弱环节", priority: "中",
      gap_desc: "先进封装环节企业 4 家，占比约 8%，封测配套存在缺口；短板判定以 D1 结论为准。",
      basis_source: "C1 环节覆盖统计（D1 接口未交付，临时派生）", candidate_count: 4, plan_done_count: 1 }
  ],

  enterprises: [
    { enterprise_id: 1, name: "杭州长川科技股份有限公司", link_node: "半导体设备", shortboard_id: "SB-半导体设备",
      tags: ["半导体设备", "杭州市", "1000 人以上"], fit_score: 86,
      dimension_scores: { industry_fit: 88, factor_match: 84, policy_match: 82, risk_control: 85 },
      hit_reason: "环节=半导体设备；地域=浙江省杭州市；规模=1000 人以上。",
      risk_note: "评分演示占位，D4 接口交付后以真实评分为准。",
      profile: {
        basic: { value: { established: "2008 年", location: "浙江省杭州市" }, source: "工商公开信息" },
        scale: { value: { employees: "1000 人以上", revenue_band: "10 亿元以上" }, source: "公开披露" },
        link: { value: { industry: "半导体设备", node: "半导体设备", tags: ["半导体设备"] }, source: "行业分类 GB/T 4754" },
        region: { value: { current_layout: "浙江省杭州市" }, source: "enterprise.region，来源：qcc" },
        tech: { value: { qualifications: ["高新技术企业"], patents: 300 }, source: "公开专利库" },
        investment: { value: { recent_move: "设备国产替代需求带动扩产" }, source: "企业公告" }
      } },
    { enterprise_id: 2, name: "浙江晶盛机电股份有限公司", link_node: "半导体设备", shortboard_id: "SB-半导体设备",
      tags: ["半导体设备", "绍兴市", "5000 人以上"], fit_score: 82,
      dimension_scores: { industry_fit: 84, factor_match: 80, policy_match: 83, risk_control: 81 },
      hit_reason: "环节=半导体设备；地域=浙江省绍兴市；规模=5000 人以上。",
      risk_note: "评分演示占位，D4 接口交付后以真实评分为准。",
      profile: {
        basic: { value: { location: "浙江省绍兴市" }, source: "工商公开信息" },
        scale: { value: { employees: "5000 人以上", revenue_band: "10 亿元以上" }, source: "公开披露" },
        link: { value: { industry: "半导体设备", node: "半导体设备", tags: ["半导体设备"] }, source: "行业分类 GB/T 4754" },
        region: { value: { current_layout: "浙江省绍兴市" }, source: "enterprise.region，来源：qcc" },
        tech: { value: { qualifications: ["高新技术企业"] }, source: "公开专利库" },
        investment: { value: { recent_move: "—" }, source: "—" }
      } },
    { enterprise_id: 3, name: "杭州众硅电子科技有限公司", link_node: "半导体设备", shortboard_id: "SB-半导体设备",
      tags: ["半导体设备", "杭州市", "100-499 人"], fit_score: null,
      dimension_scores: {}, hit_reason: "环节=半导体设备；地域=浙江省杭州市。",
      risk_note: "评分尚未生成，暂以画像信息参与候选。",
      profile: {
        basic: { value: { location: "浙江省杭州市" }, source: "工商公开信息" },
        scale: { value: { employees: "100-499 人" }, source: "公开披露" },
        link: { value: { industry: "半导体设备", node: "半导体设备", tags: ["半导体设备"] }, source: "行业分类 GB/T 4754" },
        region: { value: { current_layout: "浙江省杭州市" }, source: "enterprise.region，来源：qcc" },
        tech: { value: { qualifications: [] }, source: "公开专利库" },
        investment: { value: { recent_move: "—" }, source: "—" }
      } },
    { enterprise_id: 4, name: "杭州立昂东芯微电子有限公司", link_node: "先进封装", shortboard_id: "SB-先进封装",
      tags: ["先进封装", "杭州市", "100-499 人"], fit_score: 74,
      dimension_scores: { industry_fit: 76, factor_match: 72, policy_match: 70, risk_control: 75 },
      hit_reason: "环节=先进封装；地域=浙江省杭州市；规模=100-499 人。",
      risk_note: "规模偏小，抗风险能力一般；评分演示占位。",
      profile: {
        basic: { value: { location: "浙江省杭州市" }, source: "工商公开信息" },
        scale: { value: { employees: "100-499 人" }, source: "公开披露" },
        link: { value: { industry: "集成电路封装", node: "先进封装", tags: ["先进封装"] }, source: "行业分类 GB/T 4754" },
        region: { value: { current_layout: "浙江省杭州市" }, source: "enterprise.region，来源：qcc" },
        tech: { value: { qualifications: ["高新技术企业"] }, source: "公开专利库" },
        investment: { value: { recent_move: "—" }, source: "—" }
      } },
    { enterprise_id: 5, name: "甬矽电子(宁波)股份有限公司", link_node: "先进封装", shortboard_id: "SB-先进封装",
      tags: ["先进封装", "宁波市", "5000 人以上"], fit_score: 88,
      dimension_scores: { industry_fit: 90, factor_match: 86, policy_match: 80, risk_control: 87 },
      hit_reason: "环节=先进封装；地域=浙江省宁波市；规模=5000 人以上。",
      risk_note: "总部在宁波，外迁意愿需进一步洽谈；评分演示占位。",
      profile: {
        basic: { value: { location: "浙江省宁波市" }, source: "工商公开信息" },
        scale: { value: { employees: "5000 人以上", revenue_band: "10 亿元以上" }, source: "公开披露" },
        link: { value: { industry: "集成电路封装", node: "先进封装", tags: ["先进封装"] }, source: "行业分类 GB/T 4754" },
        region: { value: { current_layout: "浙江省宁波市" }, source: "enterprise.region，来源：qcc" },
        tech: { value: { qualifications: ["高新技术企业"] }, source: "公开专利库" },
        investment: { value: { recent_move: "先进封装产能持续扩张" }, source: "企业公告" }
      } },
    { enterprise_id: 6, name: "杭州集成电路测试公共服务中心(芯云半导体)", link_node: "先进封装", shortboard_id: "SB-先进封装",
      tags: ["先进封装", "杭州市", "500-999 人"], fit_score: 69,
      dimension_scores: { industry_fit: 70, factor_match: 66, policy_match: 72, risk_control: 65 },
      hit_reason: "环节=先进封装；地域=浙江省杭州市；规模=500-999 人。",
      risk_note: "公共服务平台属性，落地投资节奏待确认；评分演示占位。",
      profile: {
        basic: { value: { location: "浙江省杭州市" }, source: "工商公开信息" },
        scale: { value: { employees: "500-999 人", revenue_band: "10 亿元以上" }, source: "公开披露" },
        link: { value: { industry: "集成电路测试", node: "先进封装", tags: ["先进封装"] }, source: "行业分类 GB/T 4754" },
        region: { value: { current_layout: "浙江省杭州市" }, source: "enterprise.region，来源：qcc" },
        tech: { value: { qualifications: [] }, source: "公开专利库" },
        investment: { value: { recent_move: "—" }, source: "—" }
      } }
  ],

  policies: [
    { policy_id: 1, name: "杭州市人民政府办公厅关于促进集成电路产业高质量发展的实施意见", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对重点支持领域的高端芯片产品，首次流片费用 1000 万元以上的，按照不超过其流片费用的 15% 给予补助，最高补助 2000 万元。",
      source: "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html" },
    { policy_id: 2, name: "杭州市集成电路产业关键材料与核心设备研发投入补助", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对集成电路关键材料、核心设备等自主研发投入 5000 万元以上并实现实际销售的，按照不超过其研发投入的 15% 给予补助，最高补助 5000 万元。",
      source: "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html" },
    { policy_id: 3, name: "杭州市集成电路 EDA 工具技术攻关补助", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对开展 EDA 工具技术攻关，自主研发投入 1000 万元以上并实现实际销售的，按照不超过其自主研发投入的 15% 给予补助，最高补助 2000 万元。",
      source: "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html" },
    { policy_id: 4, name: "杭州市集成电路重大项目用地与人才要素保障", policy_type: "用地保障", region: "浙江省杭州市",
      clause: "推荐重点项目纳入省重大项目库，对通过国家行业指导的市重大产业项目，统筹市区两级现有政策，做好项目用地、人才等要素保障。",
      source: "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html" },
    { policy_id: 5, name: "关于进一步鼓励集成电路产业加快发展专项政策", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对集成电路产业研发投入超过 300 万元（含）以上项目，给予其实际研发投入的 20%、最高不超过 1000 万元的补助。",
      source: "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf" },
    { policy_id: 6, name: "杭州市集成电路企业购买 IP 补助", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对购买 IP 开展高端芯片、先进或特色工艺研发的集成电路企业，给予其购买 IP 直接费用的 30%、最高不超过 200 万元的补助。",
      source: "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf" },
    { policy_id: 7, name: "杭州市集成电路企业流片费用补助", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对进行重点支持领域工程产品流片的集成电路企业，给予其该款产品掩膜版制作费用的 50% 或首轮流片费用的 30%、最高不超过 300 万元的补助。",
      source: "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf" },
    { policy_id: 8, name: "杭州高新区（滨江）集成电路企业房租补贴", policy_type: "租金补贴", region: "浙江省杭州市",
      clause: "对新设立或新引进的集成电路企业，经芯火平台审核通过后，按照房租补贴人均面积和单价标准，给予最长三年、最高全额的房租补贴。",
      source: "http://www.hicc.org.cn/news-detail-580691.html" },
    { policy_id: 9, name: "杭州高新区（滨江）集成电路企业购买 EDA 工具补助", policy_type: "研发补贴", region: "浙江省杭州市",
      clause: "对集成电路企业购买 EDA 工具的，按照不超过实际发生费用的 20% 给予补贴，每家企业年度最高补贴 100 万元。",
      source: "https://zjjcmspublic.oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn/jcms_files/jcms1/web2945/site/attach/0/cd1d68feb5a7405098f73adbe3e001c5.pdf" },
    { policy_id: 10, name: "杭州高新区（滨江）芯片模组终端应用补贴", policy_type: "落户奖励", region: "浙江省杭州市",
      clause: "芯片、模组类当年度采购金额累计达 300 万元以上，按照最高不超过当年采购金额的 30% 给予补贴，每家企业最高补贴 150 万元。",
      source: "http://www.hicc.org.cn/news-detail-580691.html" }
  ],

  plans: [
    { plan_id: "PL-2026-0030", enterprise_id: 1, shortboard_id: "SB-半导体设备", status: "draft",
      generator: "llm", model_version: "qwen-plus-2026", template_id: "TPL-ONE-COMPANY-v1",
      created_at: "2026-11-23 16:02", updated_at: "2026-11-24 09:40", current_version_no: 1,
      review: { reviewer: null, reviewed_at: null, comment: null },
      plan: {
        highlights: ["企业主营半导体设备，可直接补齐本地设备环节配套缺口。", "规模 1000 人以上，具备研发与交付基础，扩产意图待进一步核实。"],
        matched_policies: [
          { policy_id: 2, name: "杭州市集成电路产业关键材料与核心设备研发投入补助", clause: "对集成电路关键材料、核心设备等自主研发投入 5000 万元以上并实现实际销售的，按照不超过其研发投入的 15% 给予补助，最高补助 5000 万元。",
            match_dimension: "行业环节 / 要素", match_reason: "行业=集成电路；地域=浙江省杭州市；对应核心设备研发投入补助条款。", source: "https://www.hangzhou.gov.cn/art/2022/7/15/art_1229063382_1822591.html" }
        ],
        negotiation_points: ["以设备环节补链缺口为切入，介绍本地配套与标准厂房载体。", "重点回应研发投入补助、用工与用电成本关切。"],
        action_steps: [
          { stage: "对接准备", actions: ["核验企业扩产计划与投资规模", "准备政策包与载体方案"], owner_suggest: "招商专班", timeline: "第 1–2 周" },
          { stage: "上门对接", actions: ["拜访企业总部", "安排园区考察"], owner_suggest: "招商专班 + 园区", timeline: "第 3–4 周" }
        ]
      },
      versions: [{ version_no: 1, generator: "llm", created_at: "2026-11-23 16:02", status: "draft", note: "LLM 首版生成" }],
      context_ref: { profile_snapshot_id: "PS-1", score_snapshot_id: "SS-1", score_status: "demo" },
      trace: { fallback_reason: null } },
    { plan_id: "PL-2026-0029", enterprise_id: 5, shortboard_id: "SB-先进封装", status: "finalized",
      generator: "llm", model_version: "qwen-plus-2026", template_id: "TPL-ONE-COMPANY-v1",
      created_at: "2026-11-22 11:18", updated_at: "2026-11-23 15:20", current_version_no: 2,
      review: { reviewer: "专班 · 张工", reviewed_at: "2026-11-23 15:20", comment: "数据与公告核对一致，政策条目适用。" },
      plan: {
        highlights: ["企业为规模以上先进封装企业，可补强本地封测配套能力。", "封装产能持续扩张，具备就近扩产基础。"],
        matched_policies: [
          { policy_id: 7, name: "杭州市集成电路企业流片费用补助", clause: "对进行重点支持领域工程产品流片的集成电路企业，给予其该款产品掩膜版制作费用的 50% 或首轮流片费用的 30%、最高不超过 300 万元的补助。",
            match_dimension: "行业环节 / 政策适用", match_reason: "行业=集成电路；地域=浙江省杭州市；对应流片与封装相关补助条款。", source: "https://zfgb.hangzhou.gov.cn/upload/default/bigfile/2025/06/04/20250604_c923fd6357be5772469d63b1714620e4.pdf" }
        ],
        negotiation_points: ["围绕封测配套率提升介绍本地集成电路集群。", "回应新增产线的用工与配套供应链问题。"],
        action_steps: [
          { stage: "对接准备", actions: ["整理本地封测配套需求清单", "准备研发补助政策口径"], owner_suggest: "招商专班", timeline: "第 1 周" },
          { stage: "上门对接", actions: ["拜访企业管理层", "对接园区载体"], owner_suggest: "招商专班 + 园区", timeline: "第 2–3 周" },
          { stage: "落地跟进", actions: ["形成意向条款", "推动选址立项"], owner_suggest: "专班 + 决策层", timeline: "第 4–6 周" }
        ]
      },
      versions: [
        { version_no: 1, generator: "template", created_at: "2026-11-22 11:18", status: "archived", note: "LLM 不可用时模板兜底首版" },
        { version_no: 2, generator: "llm", created_at: "2026-11-22 17:40", status: "finalized", note: "LLM 重新生成，经核验定稿" }
      ],
      context_ref: { profile_snapshot_id: "PS-5", score_snapshot_id: "SS-5", score_status: "demo" },
      trace: { fallback_reason: "首版模板兜底" } }
  ]
};

function nowStr() { return new Date().toLocaleString("zh-CN", { hour12: false }).replace(/\//g, "-"); }

/* ---------- 政策匹配（规则版，对应 policy_matcher.py） ---------- */
function matchPoliciesMock(ent) {
  const out = [];
  DB.policies.forEach(p => {
    const reason = ["行业=集成电路", ent.region ? `地域=${ent.profile.region.value.current_layout}` : null].filter(Boolean);
    out.push({ policy_id: p.policy_id, name: p.name, clause: p.clause,
      match_dimension: "行业环节 / 要素", match_reason: reason.join("；"), source: p.source,
      policy_type: p.policy_type });
  });
  return out.slice(0, 5);
}

function buildFallbackBody(ent, policies) {
  const highlights = [
    `${ent.name}主营${ent.profile.link.value.industry}，可补本地${ent.link_node}环节缺口。`,
    ent.fit_score ? `适配总分 ${ent.fit_score}；命中原因：${ent.hit_reason}` : "适配评分待 D4 补充，方案要点以画像公开信息为准。"
  ];
  const negotiation = ["以补链缺口为切入，介绍本地载体与配套条件。"];
  if (ent.risk_note) negotiation.push(`如实回应风险关切：${ent.risk_note}`);
  return {
    highlights, matched_policies: policies, negotiation_points: negotiation,
    action_steps: [
      { stage: "对接准备", actions: ["核验企业扩产计划与投资规模", "准备政策包与载体方案"], owner_suggest: "招商专班", timeline: "第 1–2 周" },
      { stage: "上门对接", actions: ["拜访企业总部", "安排园区考察"], owner_suggest: "招商专班 + 园区", timeline: "第 3–4 周" },
      { stage: "落地跟进", actions: ["形成意向条款", "推动立项选址"], owner_suggest: "专班 + 决策层", timeline: "第 5–8 周" }
    ]
  };
}

/* ---------- Mock API：方法签名与接口契约一致，模拟异步延迟 ---------- */
const MockAPI = {
  delay: (ms) => new Promise(r => setTimeout(r, ms)),
  async listShortboards() { await this.delay(200); return DB.shortboards; },
  async listCandidates(shortboardId) {
    await this.delay(200);
    let list = DB.enterprises;
    if (shortboardId) list = list.filter(e => e.shortboard_id === shortboardId);
    return list;
  },
  async listPlans() { await this.delay(200); return DB.plans; },
  async getPlan(planId) { return DB.plans.find(p => p.plan_id === planId); },
  async generatePlan(enterpriseId, shortboardId) {
    await this.delay(1200);
    const ent = DB.enterprises.find(e => String(e.enterprise_id) === String(enterpriseId));
    const policies = matchPoliciesMock(ent);
    const body = buildFallbackBody(ent, policies);
    const plan = {
      plan_id: "PL-2026-" + String(31 + DB.plans.length).padStart(4, "0"),
      enterprise_id: enterpriseId, shortboard_id: shortboardId, status: "draft",
      generator: "llm", model_version: "qwen-plus-2026", template_id: "TPL-ONE-COMPANY-v1",
      created_at: nowStr(), updated_at: nowStr(), current_version_no: 1,
      review: { reviewer: null, reviewed_at: null, comment: null },
      plan: body, versions: [{ version_no: 1, generator: "llm", created_at: nowStr(), status: "draft", note: "LLM 生成" }],
      context_ref: { profile_snapshot_id: "PS-" + enterpriseId, score_snapshot_id: "SS-" + enterpriseId, score_status: "missing" },
      trace: { fallback_reason: null }
    };
    DB.plans.unshift(plan);
    return plan;
  },
  async regenerate(planId) {
    const old = DB.plans.find(p => p.plan_id === planId);
    await this.delay(1000);
    const ent = DB.enterprises.find(e => String(e.enterprise_id) === String(old.enterprise_id));
    const policies = matchPoliciesMock(ent);
    const body = buildFallbackBody(ent, policies);
    old.versions.forEach(v => v.status = "archived");
    old.current_version_no += 1;
    old.plan = body; old.generator = "llm"; old.updated_at = nowStr(); old.status = "draft";
    old.review = { reviewer: null, reviewed_at: null, comment: null };
    old.versions.push({ version_no: old.current_version_no, generator: "llm", created_at: nowStr(), status: "draft", note: "重新生成新版本" });
    return old;
  }
};

window.DB = DB;
window.MockAPI = MockAPI;
