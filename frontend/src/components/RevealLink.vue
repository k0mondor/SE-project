<script setup lang="ts">
import UiIcon from './UiIcon.vue'
import FlipText from './FlipText.vue'
withDefaults(defineProps<{to?:string;text?:string;embedded?:boolean}>(),{text:'进入看板',embedded:false})
</script>
<template>
 <component :is="embedded?'span':'RouterLink'" :to="embedded?undefined:to" class="reveal-link motion-trigger">
  <span class="reveal-link__fill" aria-hidden="true"></span>
  <span class="reveal-link__arrow"><UiIcon name="arrow"/></span>
  <FlipText :text="text"/>
 </component>
</template>
<style scoped>
.reveal-link{position:relative;display:flex;align-items:center;width:100%;min-height:var(--button-height);gap:16px;font-size:var(--text-xs);isolation:isolate;overflow:hidden;color:white}.reveal-link__fill{position:absolute;inset:0;background:var(--color-blue);transform:scaleX(0);transform-origin:0 50%;transition:transform .4s var(--ease-out);z-index:-1}.reveal-link__arrow{height:var(--button-height);width:var(--button-height);background:var(--color-blue);display:grid;place-items:center;flex:none;overflow:hidden}.reveal-link__arrow svg{width:16px;transition:transform .4s var(--ease-out)}.reveal-link:hover .reveal-link__fill,.reveal-link:focus-visible .reveal-link__fill,:global(.role-card:hover .reveal-link__fill),:global(.role-card:focus-visible .reveal-link__fill){transform:scaleX(1)}</style>
