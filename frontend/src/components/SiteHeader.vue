<script setup lang="ts">
import {ref,watch} from 'vue'
import {useRoute} from 'vue-router'
import UiIcon from './UiIcon.vue'
import ScrambleText from './ScrambleText.vue'
const opened=ref(false),route=useRoute()
const links=[['/','项目总览'],['/leadership','决策领导'],['/specialist','招商专员'],['/planning','规划专班']]
watch(()=>route.path,()=>opened.value=false)
</script>
<template><header class="site-header"><RouterLink to="/" class="site-logo" aria-label="项目首页"><UiIcon name="logo"/></RouterLink><button class="menu-toggle" :aria-expanded="opened" aria-controls="main-navigation" @click="opened=!opened">{{opened?'关闭':'菜单'}}<UiIcon name="cross"/></button><nav id="main-navigation" aria-label="主导航" :class="{'is-open':opened}"><RouterLink v-for="[path,label] in links" :key="path" :to="path" class="nav-link" :aria-current="route.path===path?'page':undefined"><ScrambleText :text="label"/><span class="nav-cross"><UiIcon name="cross"/></span></RouterLink></nav></header></template>
<style scoped>
.site-header{position:fixed;z-index:50;left:var(--page-gutter);right:var(--page-gutter);top:8px;height:var(--nav-height);padding:0 16px;background:var(--color-surface);display:flex;align-items:center;justify-content:space-between}.site-logo{width:34px;height:29.333px;display:flex;align-items:center}.site-logo svg{height:25px;width:32px}.site-header nav{display:flex;align-items:center;gap:clamp(18px,4.8vw,80px);padding-right:16px;margin-left:clamp(64px,18vw,300px);margin-right:auto}.nav-link{display:flex;align-items:center;gap:8px;font-size:var(--text-sm);padding:7px 0}.nav-cross{background:var(--color-icon);width:23.104px;height:23.104px;display:grid;place-items:center;transition:background .3s}.nav-cross svg{width:9px;height:9px;transition:transform .4s var(--ease-out)}.nav-link:hover .nav-cross,.nav-link:focus-visible .nav-cross{background:var(--color-blue)}.nav-link:hover .nav-cross svg,.nav-link:focus-visible .nav-cross svg{transform:rotate(90deg)}.menu-toggle{display:none;background:none;color:white}.menu-toggle svg{width:12px}
@media(max-width:700px){.site-header{padding:0 14px}.menu-toggle{display:flex;gap:10px;align-items:center}.site-header nav{display:none;position:absolute;top:56px;left:0;right:0;background:var(--color-surface);padding:20px;gap:12px}.site-header nav{margin:0}.site-header nav.is-open{display:flex;flex-direction:column;align-items:stretch}.nav-link{justify-content:space-between;min-height:44px}}
</style>
