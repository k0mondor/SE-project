import {readonly,ref} from 'vue'

// Overview animations are always enabled; no stored preference or UI toggle.
export const motionEnabled=readonly(ref(true))
document.documentElement.dataset.motion='full'
