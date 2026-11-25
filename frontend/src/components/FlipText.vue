<script setup lang="ts">
defineProps<{text:string}>()
</script>
<template><span class="flip-text" :aria-label="text"><span v-for="(char,i) in [...text]" :key="i" class="flip-window" aria-hidden="true"><span class="flip-char" :style="{'--char-index':i}"><span>{{char===' '?'\u00a0':char}}</span><span class="flip-copy">{{char===' '?'\u00a0':char}}</span></span></span></span></template>
<style scoped>
.flip-text{display:inline-flex;white-space:nowrap;line-height:1.25;perspective:500px}.flip-window{display:inline-block;overflow:hidden}.flip-char{display:block;position:relative;transition:transform var(--motion-hover) var(--ease-out);transition-delay:calc(var(--char-index)*var(--motion-stagger));transform-style:preserve-3d}.flip-copy{position:absolute;top:100%;left:0}.motion-trigger:is(:hover,:focus-visible,:focus-within) .flip-char{transform:translateY(-100%)}
</style>
