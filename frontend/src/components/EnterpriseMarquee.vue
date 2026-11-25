<script setup lang="ts">
import {enterprises} from '../data/overview'
const marks=[...enterprises,...enterprises]
</script>
<template><section class="enterprise-marquee" aria-label="企业资料库中的部分企业"><div class="marquee-track"><div v-for="copy in 2" :key="copy" class="marquee-group" :aria-hidden="copy===2?true:undefined"><span v-for="(enterprise,i) in marks" :key="`${enterprise.name}-${i}`" class="enterprise-wordmark" :style="{width:`${enterprise.logoWidth}px`}"><img :src="enterprise.logo" :alt="enterprise.name" :aria-hidden="i>=enterprises.length?true:undefined"></span></div></div></section></template>
<style scoped>
.enterprise-marquee{position:relative;overflow:hidden;padding:58px 0;background:#fff;color:#6c7584;border:0;isolation:isolate}.marquee-track{width:max-content;display:flex;animation:marquee 32s linear infinite}.marquee-group{display:flex;align-items:center;justify-content:space-around;min-width:100vw;gap:64px;padding:0 32px;flex:none}.enterprise-wordmark{position:relative;display:block;height:42px;overflow:hidden;flex:none}.enterprise-wordmark img{position:absolute;width:100%;height:auto;left:0;top:50%;transform:translateY(-50%);filter:grayscale(1) contrast(3);opacity:.55;mix-blend-mode:multiply}@keyframes marquee{to{transform:translateX(-50%)}}@media(max-width:700px){.enterprise-marquee{padding:40px 0}.marquee-group{gap:40px}}:global(html[data-motion='reduced'] .marquee-track){animation:none}
</style>
