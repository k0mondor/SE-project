<script setup lang="ts">
import { ref, watch } from 'vue'
import UiButton from '../../../components/UiButton.vue'
import { getSegmentEvidence, type EvidencePage, type LeadershipDiagnosis, type SegmentDiagnosis } from '../../../api/leadership'

const props = defineProps<{ scope: LeadershipDiagnosis; segment: SegmentDiagnosis }>()
const page = ref(1)
const refresh = ref(0)
const loading = ref(false)
const error = ref('')
const result = ref<EvidencePage>()

watch([page, refresh], async ([selectedPage], _, onCleanup) => {
  if (!props.segment.count) return
  const controller = new AbortController()
  onCleanup(() => controller.abort())
  loading.value = true
  error.value = ''
  result.value = undefined
  try {
    const evidence = await getSegmentEvidence(props.scope, props.segment.segment, selectedPage, controller.signal)
    if (!controller.signal.aborted) result.value = evidence
  } catch (failure) {
    if (!controller.signal.aborted) {
      error.value = failure instanceof Error ? failure.message : '无法读取企业样本'
    }
  } finally {
    if (!controller.signal.aborted) loading.value = false
  }
}, { immediate: true })
</script>

<template>
  <div class="evidence">
    <p class="muted">统计来源：{{ segment.evidence.source }}。</p>
    <p v-if="segment.definition" class="muted">{{ segment.definition }}。</p>
    <p v-if="!segment.count" class="muted">当前统计范围内没有该环节的企业样本。</p>
    <p v-else-if="loading" role="status">正在读取企业样本…</p>
    <div v-else-if="error" role="alert">
      <p>{{ error }}</p>
      <UiButton label="重试" @click="refresh++" />
    </div>
    <template v-else-if="result">
      <p v-if="!result.items.length" class="muted">本页暂无样本。</p>
      <ul v-else>
        <li v-for="enterprise in result.items" :key="enterprise.id">
          <strong>{{ enterprise.name }}</strong>
          <span class="muted">{{ enterprise.region }}</span>
          <a
            v-if="/^https?:\/\//i.test(enterprise.source_url)"
            :href="enterprise.source_url"
            target="_blank"
            rel="noopener noreferrer"
          >{{ enterprise.source || '查看来源' }} ↗</a>
          <span v-else class="muted">{{ enterprise.source || '暂无来源链接' }}</span>
        </li>
      </ul>
      <div v-if="result.total > result.page_size || page > 1" class="pagination">
        <UiButton label="上一页" variant="dark" :disabled="page === 1" @click="page--" />
        <span>第 {{ page }} 页 · {{ result.total }} 家</span>
        <UiButton label="下一页" variant="dark" :disabled="page * result.page_size >= result.total" @click="page++" />
      </div>
    </template>
  </div>
</template>

<style scoped>
.evidence { background: var(--color-page); padding: var(--space-4); margin-top: var(--space-2); }
.evidence p + p { margin-top: var(--space-2); }
.muted { color: var(--color-muted); }
ul { list-style: none; padding: 0; margin: var(--space-2) 0 0; }
li { display: grid; gap: var(--space-1); padding: var(--space-2) 0; border-top: 1px solid var(--color-icon); overflow-wrap: anywhere; }
li strong { font-weight: 500; }
a { width: fit-content; max-width: 100%; color: #a9c2ff; text-decoration: underline; text-underline-offset: 3px; }
.pagination { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2); margin-top: var(--space-2); }
</style>
