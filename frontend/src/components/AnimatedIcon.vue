<script setup lang="ts">
import {onMounted,onBeforeUnmount,ref} from 'vue'
import type {AnimationItem} from 'lottie-web'
import {motionEnabled} from '../composables/motionPreference'
const props=defineProps<{name:string;active?:boolean}>()
const holder=ref<HTMLElement>(),reduced=!motionEnabled.value
let animation:AnimationItem|undefined,observer:IntersectionObserver|undefined,disposed=false
onMounted(async()=>{if(!holder.value||props.name==='pen')return;const {default:lottie}=await import('lottie-web/build/player/lottie_light');if(disposed||!holder.value)return;animation=lottie.loadAnimation({container:holder.value,renderer:'svg',loop:false,autoplay:false,path:`/reference-icons/${props.name}.json`});animation.addEventListener('DOMLoaded',()=>{if(reduced)animation?.goToAndStop(animation.totalFrames-1,true)});observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){animation?.play();observer?.disconnect()}},{threshold:.5});observer.observe(holder.value)})
onBeforeUnmount(()=>{disposed=true;observer?.disconnect();animation?.destroy()})
function replay(){if(!reduced)animation?.goToAndPlay(0,true)}
</script>
<template><span ref="holder" class="animated-icon" @mouseenter="replay"><svg v-if="name==='pen'" viewBox="0 0 38 43" fill="none" aria-hidden="true"><path d="M32.3505 42.6667H0V39.2002H32.3505V42.6667ZM26.7031 6.88165L2.83304 30.4916V34.5359L6.91345 34.5361L30.7872 10.9223L32.7878 12.9011L8.08552 37.3347H.0034225L.00368577 35.9353L.0034225 29.9122L.00368577 29.3328L24.7025 4.90286L26.7031 6.88165ZM37.7436 7.99748L36.5044 9.22293L35.2654 10.4486L27.1799 2.45143L29.6583 0L37.7436 7.99748Z" fill="currentColor"/></svg></span></template>
<style scoped>.animated-icon{width:var(--icon-size);height:var(--icon-size);display:block;background:var(--color-blue);color:white;flex:none;overflow:hidden}.animated-icon>svg{padding:9px 11px;width:100%;height:100%}.animated-icon:deep(svg){width:100%;height:100%}</style>
