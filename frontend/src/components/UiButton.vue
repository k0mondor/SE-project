<script setup lang="ts">
import FlipText from './FlipText.vue'
withDefaults(defineProps<{label:string;variant?:'primary'|'dark'|'light';loading?:boolean;disabled?:boolean;type?:'button'|'submit'|'reset'}>(),{variant:'primary',type:'button'})
</script>
<template><button class="ui-button motion-trigger" :class="`ui-button--${variant}`" :type="type" :disabled="disabled||loading" :aria-busy="loading||undefined"><span v-if="loading" class="ui-button__spinner" aria-hidden="true"></span><FlipText :text="loading?'处理中':label"/></button></template>
<style scoped>.ui-button{min-height:var(--button-height);display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:0 23px;font-size:var(--text-xs);background:var(--color-blue);color:#fff;transition:background .4s var(--ease-out)}.ui-button--dark{background:#000}.ui-button--light{background:#fff;color:#000}.ui-button:hover:not(:disabled){background:var(--color-blue-hover);color:#fff}.ui-button__spinner{width:12px;height:12px;border:1px solid #fff5;border-top-color:white;animation:spin .8s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}:global(html[data-motion='reduced'] .ui-button__spinner){animation:none}</style>
