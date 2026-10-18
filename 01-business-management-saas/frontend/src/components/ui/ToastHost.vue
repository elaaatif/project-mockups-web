<script setup>
import { CheckCircle2, XCircle } from 'lucide-vue-next'
import { toasts } from '@/core/toast'
</script>

<template>
  <div class="pointer-events-none fixed right-4 bottom-4 z-[60] flex w-80 flex-col gap-2">
    <TransitionGroup
      enter-from-class="translate-y-3 opacity-0" enter-active-class="transition duration-300"
      leave-to-class="translate-x-6 opacity-0" leave-active-class="transition duration-200"
    >
      <div v-for="t in toasts" :key="t.id"
           class="pointer-events-auto flex items-start gap-3 rounded-2xl bg-slate-900 px-4 py-3 text-sm text-white shadow-2xl ring-1 ring-white/10">
        <CheckCircle2 v-if="t.type === 'success'" class="mt-0.5 size-5 shrink-0 text-emerald-400" />
        <XCircle v-else class="mt-0.5 size-5 shrink-0 text-rose-400" />
        <span>{{ t.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>
