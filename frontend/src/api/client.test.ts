import {afterEach,describe,it,expect,vi} from 'vitest'
import {request,ApiError,getEnterprises} from './client'
afterEach(()=>vi.unstubAllGlobals())
describe('shared API boundary',()=>{
 it('unwraps successful backend response',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:true,json:async()=>({code:0,data:{total:50}})}));await expect(request('/enterprises')).resolves.toEqual({total:50})})
 it('rejects business errors even under HTTP 200',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:true,json:async()=>({code:404,message:'企业不存在',data:null})}));await expect(request('/enterprises/999/profile')).rejects.toEqual(new ApiError('企业不存在',404))})
 it('encodes Chinese filters and excludes empty filters',async()=>{const fetcher=vi.fn().mockResolvedValue({ok:true,json:async()=>({code:0,data:{items:[]}})});vi.stubGlobal('fetch',fetcher);await getEnterprises({chain_segment:'先进封装',keyword:'',page:1});const url=fetcher.mock.calls[0][0] as string;expect(decodeURIComponent(url)).toContain('chain_segment=先进封装');expect(url).not.toContain('keyword=')})
 it('does not treat an HTTP failure as data',async()=>{vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:false,status:503}));await expect(request('/health')).rejects.toMatchObject({code:503})})
})
