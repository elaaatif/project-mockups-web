<script setup>
// Engineering-drawing style product tile (no photo dependency): blueprint grid + category icon.
import { Cpu, Droplets, SlidersHorizontal, Wind, Zap } from 'lucide-vue-next'

defineProps({ category: String, sku: String })
const ICONS = { pumps: Droplets, valves: SlidersHorizontal, motors: Zap, automation: Cpu, air: Wind }
</script>

<template>
  <div class="relative grid place-items-center overflow-hidden bg-slate-900 bg-[linear-gradient(rgba(255,255,255,.06)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,.06)_1px,transparent_1px)] bg-[size:20px_20px]">
    <div class="absolute size-2/3 rounded-full bg-brand-500/20 blur-2xl" />
    <component :is="ICONS[category]" class="relative size-1/3 text-brand-400" :stroke-width="1.2" />
    <span v-if="sku" class="absolute bottom-3 left-3 font-mono text-xs tracking-widest text-slate-400">{{ sku }}</span>
    <span class="absolute top-3 right-3 font-mono text-[10px] text-slate-600">REV C</span>
  </div>
</template>
