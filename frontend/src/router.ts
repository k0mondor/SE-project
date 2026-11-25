import { createRouter, createWebHistory } from 'vue-router'
const OverviewPage=()=>import('./pages/OverviewPage.vue')
const WorkspacePage=()=>import('./pages/WorkspacePage.vue')
export const router=createRouter({history:createWebHistory(),routes:[
 {path:'/',name:'overview',component:OverviewPage,meta:{title:'项目总览'}},
 {path:'/leadership',name:'leadership',component:()=>import('./pages/leadership/index.vue'),meta:{title:'决策领导'}},
 {path:'/specialist',name:'specialist',component:()=>import('./pages/specialist/index.vue'),meta:{title:'招商专员'}},
 {path:'/planning',name:'planning',component:()=>import('./pages/planning/index.vue'),meta:{title:'规划专班'}},
 {path:'/:pathMatch(.*)*',component:WorkspacePage,props:{role:'not-found'},meta:{title:'页面未找到'}}
],scrollBehavior:()=>({top:0})})
router.afterEach(to=>{document.title=`${String(to.meta.title)} · 产业链招商`})
