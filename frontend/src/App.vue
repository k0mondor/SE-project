<script setup lang="ts">
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'
import {useRoute} from 'vue-router'
import {motionEnabled} from './composables/motionPreference'
const route=useRoute()
</script>
<template><a class="skip-link" href="#main">跳到主要内容</a><SiteHeader/><main id="main"><RouterView v-slot="{Component}"><component :is="Component" :key="`${route.fullPath}-${motionEnabled}`"/></RouterView></main><SiteFooter/></template>
