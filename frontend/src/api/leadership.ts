import { request, type Enterprise, type EnterprisePage } from './client'

export type SegmentStatus = 'covered' | 'missing' | 'weak' | 'no_data'

export interface SegmentDiagnosis {
  id: number
  segment: string
  definition: string | null
  count: number
  ratio: number | null
  status: SegmentStatus
  evidence: {
    enterprise_count: number
    sample_count: number
    threshold_percent: number
    source: string
  }
  recommendation: string | null
}

export interface SupportGap {
  demand_segment: string
  demand_count: number
  supply_segment: string
  supply_count: number
  supply_status: SegmentStatus
  recommendation: string
}

export interface LeadershipDiagnosis {
  region: string | null
  include_subregions: boolean
  total: number
  covered_count: number
  unclassified_count: number
  threshold_percent: number
  segments: SegmentDiagnosis[]
  shortages: SegmentDiagnosis[]
  support_gaps: SupportGap[]
}

export interface EvidenceEnterprise extends Enterprise {
  source: string
  source_url: string
}

export type EvidencePage = Omit<EnterprisePage, 'items'> & { items: EvidenceEnterprise[] }

interface Scope {
  region: string | null
  include_subregions: boolean
}

function scopeParams(scope: Scope) {
  const query = new URLSearchParams()
  if (scope.region) {
    query.set('region', scope.region)
    query.set('include_subregions', String(scope.include_subregions))
  }
  return query
}

export function getLeadershipDiagnosis(region: string, signal?: AbortSignal) {
  const query = scopeParams({ region, include_subregions: true })
  return request<LeadershipDiagnosis>(`/leadership/shortages?${query}`, { signal })
}

export function getSegmentEvidence(scope: Scope, segment: string, page: number, signal?: AbortSignal) {
  const query = scopeParams(scope)
  query.set('chain_segment', segment)
  query.set('page', String(page))
  query.set('page_size', '10')
  return request<EvidencePage>(`/enterprises?${query}`, { signal })
}
