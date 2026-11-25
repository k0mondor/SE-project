<script setup lang="ts">
defineProps<{name?:string}>()
</script>
<template>
 <svg v-if="name==='cross'" viewBox="0 0 10 10" fill="none" aria-hidden="true"><path d="M5.49609 10.001H4.49609V5.91895H5.49609V10.001ZM10 4.49512V5.49512H5.91797V4.49512H10ZM4.08203 5.49512H0V4.49512H4.08203V5.49512ZM5.49609 4.08301H4.49609V0.000976562L5.49609 0V4.08301Z" fill="currentColor"/></svg>
 <svg v-else-if="name==='logo'" viewBox="0 0 36 28" fill="none" aria-hidden="true"><path d="m14 4-11 10 8 8 10-10M22 24l11-10-8-8-10 10" stroke="currentColor" stroke-width="2.5" stroke-linejoin="miter"/></svg>
 <svg v-else-if="name==='arrow'" viewBox="0 0 13 11" aria-hidden="true"><path d="M12.7432 4.11621V6.68066L7.20996 10.7549V8.89355L10.9619 6.12891L.000976562 6.12988L0 4.62988L10.917 4.62891L7.20996 1.87012V0L12.7432 4.11621Z" fill="currentColor"/></svg>
 <svg v-else-if="name==='target'" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="1.5"/><path d="m15 15 6 6" stroke="currentColor" stroke-width="1.5"/></svg>
 <svg v-else-if="name==='document'" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5h14v16H4zM7 2h14v16M7 9h8M7 12h8M7 15h6" stroke="currentColor" stroke-width="1.5"/></svg>
 <svg v-else viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z" stroke="currentColor" stroke-width="1.5"/></svg>
</template>
