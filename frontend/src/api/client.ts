export class ApiError extends Error{constructor(message:string,public code:number){super(message);this.name='ApiError'}}
export interface Envelope<T>{code:number;message?:string;data:T}
/** Handles the existing backend's HTTP-200/business-error response convention. */
export async function request<T>(path:string,options:RequestInit={}):Promise<T>{
 const timeout=new AbortController(),timer=setTimeout(()=>timeout.abort(),10000)
 const signal=options.signal?AbortSignal.any([options.signal,timeout.signal]):timeout.signal
 try{
  const response=await fetch(`/api/v1${path}`,{...options,signal,headers:{Accept:'application/json',...options.headers}})
  if(!response.ok)throw new ApiError(`请求失败（${response.status}）`,response.status)
  const envelope=await response.json() as Envelope<T>
  if(typeof envelope.code!=='number')throw new ApiError('接口返回格式不正确',502)
  if(envelope.code!==0)throw new ApiError(envelope.message||'请求未成功',envelope.code)
  return envelope.data
 }finally{clearTimeout(timer)}
}
export interface ImportStatus{enterprise_count:number;policy_count:number;segment_count:number;with_source_ratio:number;missing_dims:Record<string,number>}
export interface Enterprise{id:number;name:string;industry_name:string;chain_segment:string;region:string;match_reasons:string[]}
export interface EnterprisePage{total:number;page:number;page_size:number;items:Enterprise[]}
export function getImportStatus(signal?:AbortSignal){return request<ImportStatus>('/data/import/status',{signal})}
export function getEnterprises(params:Record<string,string|number>={},signal?:AbortSignal){const query=new URLSearchParams(Object.entries(params).filter(([,v])=>v!=='').map(([k,v])=>[k,String(v)]));return request<EnterprisePage>(`/enterprises?${query}`,{signal})}
