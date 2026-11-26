import {onMounted,onBeforeUnmount,nextTick,type Ref} from 'vue'
import gsap from 'gsap'
import {ScrollTrigger} from 'gsap/ScrollTrigger'
import Lenis from 'lenis'
import {motionEnabled} from './motionPreference'
gsap.registerPlugin(ScrollTrigger)
export function useOverviewMotion(root:Ref<HTMLElement|undefined>,active:Ref<number>){
 let lenis:Lenis|undefined,context:gsap.Context|undefined
 let disposed=false,tick:((time:number)=>void)|undefined
 function goTo(id:string){const target=document.getElementById(id);if(!target)return;if(lenis)lenis.scrollTo(target,{offset:-72,duration:1.1});else target.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'})}
 onMounted(async()=>{await nextTick();await document.fonts.ready;if(disposed||!root.value)return
  if(!motionEnabled.value)return
  lenis=new Lenis({lerp:.12,syncTouch:false,autoRaf:false,anchors:false})
  lenis.on('scroll',ScrollTrigger.update)
  tick=time=>lenis?.raf(time*1000);gsap.ticker.add(tick)
  context=gsap.context(()=>{
   gsap.from('.hero-title .hero-word',{y:24,opacity:0,filter:'blur(12px)',duration:1.3,stagger:.09,ease:'expo.out',clearProps:'all'})
   gsap.from('.hero-subtitle,.hero-bottom',{y:14,opacity:0,duration:.9,stagger:.12,delay:.35,ease:'expo.out',clearProps:'all'})
   gsap.to('.hero-atmosphere',{yPercent:14,scale:1.08,ease:'none',scrollTrigger:{trigger:'.hero',start:'top top',end:'bottom top',scrub:1}})
   gsap.utils.toArray<HTMLElement>('.workflow-row').forEach((row,i)=>{
    ScrollTrigger.create({trigger:row,start:'top 65%',end:'bottom 65%',onEnter:()=>active.value=i,onEnterBack:()=>active.value=i})
   })
   const cards=gsap.utils.toArray<HTMLElement>('.role-card')
   gsap.from(cards,{yPercent:15,opacity:0,stagger:.12,duration:.8,ease:'expo.out',clearProps:'all',scrollTrigger:{trigger:'.roles-grid',start:'top 88%',once:true}})
   gsap.utils.toArray<HTMLElement>('.role-card').forEach(card=>{gsap.from(card.querySelectorAll('li svg'),{clipPath:'inset(0 100% 0 0)',duration:.4,stagger:.1,ease:'power2.out',clearProps:'all',scrollTrigger:{trigger:card,start:'top 70%',once:true}})})
  },root.value)
  ScrollTrigger.refresh()
 })
 onBeforeUnmount(()=>{disposed=true;context?.revert();if(tick)gsap.ticker.remove(tick);lenis?.destroy()})
 return{goTo}
}
