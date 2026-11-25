export const workflow=[
 {english:'IDENTIFY',title:'识别产业短板',icon:'pen',to:'/leadership'},
 {english:'DISCOVER',title:'筛选目标企业',icon:'check',to:'/specialist'},
 {english:'PROFILE',title:'查看企业画像',icon:'research',to:'/specialist'},
 {english:'EVALUATE',title:'评估产业适配',icon:'shield',to:'/specialist'},
 {english:'CREATE',title:'生成招商方案',icon:'performance',to:'/planning'}
] as const
export const roles=[
 {title:'决策领导',english:'For leaders',icon:'star',to:'/leadership',description:'掌握产业现状，明确补链重点。',details:['查看环节分布','识别薄弱环节','确定招商方向']},
 {title:'招商专员',english:'For specialists',icon:'target',to:'/specialist',description:'筛选目标企业，判断招商价值。',details:['组合条件筛选','查看企业画像','比较适配评分']},
 {title:'规划专班',english:'For planners',icon:'document',to:'/planning',description:'结合企业与政策，形成招商方案。',details:['匹配适用政策','生成对接方案','审核方案内容']}
] as const
// These are indexed enterprise names, not endorsements. Replace with approved official
// SVG assets through the optional `logo` field; never imitate a company's logo.
export const enterprises:{name:string;logo:string;logoWidth:number}[]=[
 {name:'士兰微',logo:'/enterprise-logos/silan.png',logoWidth:146},
 {name:'杰华特',logo:'/enterprise-logos/joulwatt.png',logoWidth:174},
 {name:'联芸科技',logo:'/enterprise-logos/maxio.png',logoWidth:136}
]
