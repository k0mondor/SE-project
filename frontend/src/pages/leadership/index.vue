<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import UiButton from '../../components/UiButton.vue'
import {
  getLeadershipDiagnosis,
  type LeadershipDiagnosis,
  type SegmentDiagnosis,
  type SegmentStatus,
} from '../../api/leadership'
import SegmentEvidence from './components/SegmentEvidence.vue'

const region = ref('')
const refresh = ref(0)
const diagnosis = ref<LeadershipDiagnosis>()
const activeId = ref<number>()
const error = ref('')
const loading = ref(true)
const leading = computed(() => diagnosis.value?.segments.reduce<SegmentDiagnosis | undefined>(
  (best, item) => !best || item.count > best.count ? item : best, undefined,
))

const labels: Record<SegmentStatus, string> = {
  covered: '达到阈值',
  missing: '样本未覆盖',
  weak: '覆盖偏薄',
  no_data: '暂无样本',
}
const percent = new Intl.NumberFormat('zh-CN', { style: 'percent', maximumFractionDigits: 2 })

function evidenceText(item: SegmentDiagnosis) {
  const counts = `${item.evidence.enterprise_count} / ${item.evidence.sample_count} 家`
  return item.status === 'missing'
    ? `${counts}，环节字典中有此环节，当前范围的样本未覆盖。`
    : `${counts}，占 ${percent.format(item.ratio ?? 0)}，低于 ${item.evidence.threshold_percent}% 阈值。`
}

function toggleEvidence(id: number) {
  activeId.value = activeId.value === id ? undefined : id
}

watch([region, refresh], async ([selectedRegion], _, onCleanup) => {
  const controller = new AbortController()
  onCleanup(() => controller.abort())
  loading.value = true
  diagnosis.value = undefined
  activeId.value = undefined
  error.value = ''
  try {
    const result = await getLeadershipDiagnosis(selectedRegion, controller.signal)
    if (!controller.signal.aborted) diagnosis.value = result
  } catch (failure) {
    if (!controller.signal.aborted) {
      error.value = failure instanceof Error ? failure.message : '无法读取短板诊断'
    }
  } finally {
    if (!controller.signal.aborted) loading.value = false
  }
}, { immediate: true })
</script>

<template>
  <section class="leadership">
    <header class="heading">
      <div>
        <h1>决策领导看板</h1>
        <p>集成电路产业链短板与补链方向</p>
      </div>
      <label class="scope">
        统计范围
        <select v-model="region" class="ui-field">
          <option value="">全部样本</option>
          <option value="浙江省杭州市">杭州市（含下辖区）</option>
        </select>
      </label>
    </header>

    <p v-if="loading" class="state-panel" role="status">正在读取产业链诊断…</p>
    <div v-else-if="error" class="state-panel" role="alert">
      <p>无法读取产业链诊断。{{ error }}</p>
      <UiButton label="重新加载" @click="refresh++" />
    </div>
    <template v-else-if="diagnosis">
      <div v-if="!diagnosis.total" class="state-panel">
        <p role="status">当前统计范围暂无企业样本。请选择其他统计范围，或导入样本后重新加载。</p>
        <UiButton label="重新加载" @click="refresh++" />
      </div>
      <template v-else>
        <dl class="metrics" aria-label="样本概况">
          <div><dt>样本企业</dt><dd>{{ diagnosis.total }} <small>家</small></dd></div>
          <div><dt>已覆盖环节</dt><dd>{{ diagnosis.covered_count }} <small>/ {{ diagnosis.segments.length }}</small></dd></div>
          <div><dt>短板环节</dt><dd>{{ diagnosis.shortages.length }} <small>个</small></dd></div>
          <div>
            <dt>最高环节占比</dt>
            <dd v-if="leading?.count">{{ percent.format(leading.ratio ?? 0) }} <small>{{ leading.segment }}</small></dd>
            <dd v-else>—</dd>
          </div>
        </dl>

        <div class="diagnosis-grid">
          <section class="panel coverage" aria-labelledby="coverage-heading">
            <h2 id="coverage-heading">产业链覆盖</h2>
            <p class="muted">以企业名录为样本，环节占比低于 {{ diagnosis.threshold_percent }}% 标为覆盖偏薄。</p>
            <p v-if="diagnosis.unclassified_count" class="muted">
              {{ diagnosis.unclassified_count }} 家样本尚未匹配环节字典，计入样本总数。
            </p>
            <ul class="coverage-list">
              <li v-for="item in diagnosis.segments" :key="item.id" class="coverage-row">
                <div class="bar-label">
                  <span>{{ item.segment }}</span>
                  <span class="muted">{{ item.count }} 家 · {{ percent.format(item.ratio ?? 0) }}</span>
                </div>
                <div class="bar-track" aria-hidden="true">
                  <div class="bar-fill" :class="item.status" :style="{ width: `${(item.ratio ?? 0) * 100}%` }"></div>
                </div>
                <span v-if="item.status !== 'covered'" class="warning bar-status">{{ labels[item.status] }}</span>
              </li>
            </ul>
          </section>

          <section class="panel" aria-labelledby="shortages-heading">
            <h2 id="shortages-heading">短板清单</h2>
            <p v-if="!diagnosis.shortages.length" class="muted">当前样本未命中短板规则。</p>
            <article v-for="item in diagnosis.shortages" :key="item.id" class="shortage">
              <div class="shortage-title">
                <h3>{{ item.segment }}</h3>
                <span class="ui-tag warning">{{ labels[item.status] }}</span>
              </div>
              <p class="muted">{{ evidenceText(item) }}</p>
              <p>{{ item.recommendation }}</p>
              <button
                type="button"
                class="evidence-toggle"
                :aria-expanded="activeId === item.id"
                :aria-controls="activeId === item.id ? `segment-evidence-${item.id}` : undefined"
                @click="toggleEvidence(item.id)"
              >{{ activeId === item.id ? '收起数据依据' : '查看数据依据' }}</button>
              <SegmentEvidence
                v-if="activeId === item.id"
                :id="`segment-evidence-${item.id}`"
                :scope="diagnosis"
                :segment="item"
                :key="item.id"
              />
            </article>
          </section>
        </div>

        <section class="panel support" aria-labelledby="support-heading">
          <h2 id="support-heading">潜在配套缺口</h2>
          <p class="muted">结合相关环节的样本覆盖情况筛查。工艺、产能和实际供需关系需进一步核验。</p>
          <p v-if="!diagnosis.support_gaps.length" class="muted">当前样本未触发配套缺口筛查规则。</p>
          <ul v-else class="support-list">
            <li v-for="gap in diagnosis.support_gaps" :key="`${gap.demand_segment}-${gap.supply_segment}`">
              <div class="shortage-title">
                <h3>{{ gap.demand_segment }} → {{ gap.supply_segment }}</h3>
                <span class="ui-tag warning">待核验</span>
              </div>
              <p class="muted">需求侧样本 {{ gap.demand_count }} 家，配套侧样本 {{ gap.supply_count }} 家（{{ labels[gap.supply_status] }}）。</p>
              <p>{{ gap.recommendation }}</p>
            </li>
          </ul>
        </section>
      </template>
    </template>
  </section>
</template>

<style scoped>
.leadership {
  max-width: 1440px;
  min-height: calc(100svh - 64px);
  margin: 0 auto;
  padding: clamp(104px, 10vw, 144px) max(var(--page-gutter), 4vw) var(--space-16);
}
.heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: var(--space-6);
  margin-bottom: var(--space-8);
}
h1 { font-size: clamp(32px, 4.5vw, 56px); line-height: 1.12; margin-bottom: var(--space-3); }
h2 { font-size: var(--text-card); margin-bottom: var(--space-2); }
h3 { font-size: var(--text-base); }
.heading p, .scope, .muted { color: var(--color-muted); }
.scope { display: grid; gap: var(--space-2); min-width: 192px; }
.state-panel p { margin-bottom: var(--space-4); }
.metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  margin: 0 0 var(--space-4);
  gap: 1px;
  background: var(--color-icon);
  border: 1px solid var(--color-icon);
}
.metrics > div { background: var(--color-surface); padding: var(--space-6); }
.metrics dt { color: var(--color-muted); }
.metrics dd { margin: var(--space-2) 0 0; font-size: clamp(26px, 4vw, 44px); font-variant-numeric: tabular-nums; }
.metrics small { font-size: var(--text-xs); color: var(--color-muted); }
.diagnosis-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.17fr); gap: var(--space-4); }
.panel { background: var(--color-surface); border: 1px solid var(--color-icon); padding: var(--space-6); }
.coverage-list, .support-list { list-style: none; padding: 0; margin: var(--space-6) 0 0; }
.coverage-row + .coverage-row { margin-top: var(--space-4); }
.bar-label { display: flex; justify-content: space-between; gap: var(--space-2); }
.bar-track { height: 8px; background: var(--color-icon); margin-top: var(--space-2); }
.bar-fill { height: 100%; background: var(--color-blue); }
.bar-fill.weak { background: #e8ad68; }
.warning { color: #ffd198; }
.bar-status { display: block; margin-top: var(--space-1); font-size: var(--text-xs); }
.shortage { padding-top: var(--space-4); margin-top: var(--space-4); border-top: 1px solid var(--color-icon); }
.shortage-title { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2); }
.shortage p, .support-list p { margin-top: var(--space-2); line-height: 1.6; }
.evidence-toggle {
  padding: var(--space-2) 0;
  margin-top: var(--space-1);
  background: transparent;
  color: #a9c2ff;
  text-decoration: underline;
  text-underline-offset: 4px;
}
.support { margin-top: var(--space-4); }
.support-list { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-4); }
.support-list li { border-top: 1px solid var(--color-icon); padding-top: var(--space-3); }
@media (max-width: 900px) {
  .diagnosis-grid { grid-template-columns: 1fr; }
  .support-list { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 560px) {
  .heading { align-items: stretch; flex-direction: column; }
  .metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .metrics > div, .panel { padding: var(--space-4); }
  .support-list { grid-template-columns: 1fr; }
}
</style>
