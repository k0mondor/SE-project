<script setup lang="ts">
import {ref,onMounted,onBeforeUnmount} from 'vue'
import gsap from 'gsap'
import {ScrollTrigger} from 'gsap/ScrollTrigger'
import {motionEnabled} from '../composables/motionPreference'
const props=withDefaults(defineProps<{text:string;mode?:'hover'|'enter'}>(),{mode:'hover'})
const root=ref<HTMLElement>()
let timeline:gsap.core.Timeline|undefined,trigger:ScrollTrigger|undefined,disposed=false,parent:HTMLElement|null=null
const symbols='abcdefghijklmnopqrstuvwxyz0123456789!$^*()-_=+[]{}'
function restore(){root.value?.querySelectorAll<HTMLElement>('.scramble-char').forEach((e,i)=>{e.textContent=[...props.text][i]??'';gsap.set(e,{clearProps:'color,backgroundColor,opacity,visibility'})})}
function play(){if(!motionEnabled.value||!root.value)return;timeline?.kill();restore();const chars=[...root.value.querySelectorAll<HTMLElement>('.scramble-char')];const tl=timeline=gsap.timeline({onComplete:restore,onInterrupt:restore});chars.forEach((el,i)=>{const original=[...props.text][i]??'';if(original===' ')return;const delay=props.mode==='enter'?i*.0311:i*.04;const color=['#5986fa','#abb2b9','#000'][i%3];if(props.mode==='enter')tl.set(el,{opacity:1,backgroundColor:color,color:i%3===1?'#000':'#fff'},delay);for(let frame=0;frame<4;frame++)tl.call(()=>{el.textContent=symbols[Math.floor(Math.random()*symbols.length)]!;if(props.mode==='hover')el.style.color=frame%2?'#6c7584':'#298dff'},[],delay+frame*.03);tl.call(()=>{el.textContent=original;gsap.set(el,{clearProps:'color,backgroundColor,opacity,visibility'})},[],delay+.14)})}
onMounted(async()=>{await document.fonts.ready;if(disposed||!root.value||!motionEnabled.value)return;root.value.querySelectorAll<HTMLElement>('.scramble-char').forEach(e=>{e.style.width=`${e.getBoundingClientRect().width}px`});if(props.mode==='enter'){gsap.set(root.value.querySelectorAll('.scramble-char'),{opacity:0});trigger=ScrollTrigger.create({trigger:root.value,start:'top 90%',once:true,onEnter:play})}else{parent=root.value.closest('.nav-link')||root.value;parent.addEventListener('mouseenter',play);parent.addEventListener('focus',play)}})
onBeforeUnmount(()=>{disposed=true;timeline?.kill();trigger?.kill();parent?.removeEventListener('mouseenter',play);parent?.removeEventListener('focus',play)})
</script>
<template><span ref="root" class="scramble-text" :aria-label="text"><span v-for="(char,i) in [...text]" :key="i" class="scramble-char" aria-hidden="true">{{char===' '?'\u00a0':char}}</span></span></template>
<style scoped>.scramble-text{display:inline-block;white-space:nowrap}.scramble-char{display:inline-block;text-align:center}</style>
