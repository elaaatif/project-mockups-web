<script setup>
import { ref } from 'vue'
import { Flame, Mail, Phone } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, humanize } from '@/core/format'
import { agentService } from '../agent.service'

const { data, error, reload } = useResource(agentService.pipeline)
const dragging = ref(null)
const over = ref(null)
const TONE = { new: 'bg-sky-500', contacted: 'bg-violet-500', viewing: 'bg-amber-500', negotiation: 'bg-orange-500', won: 'bg-emerald-500', lost: 'bg-slate-400' }
const compact = (n) => (n >= 1e6 ? `£${(n / 1e6).toFixed(2)}m` : n >= 10000 ? `£${Math.round(n / 1000)}k` : `£${n.toLocaleString()} pcm`)
const inStage = (s) => data.value.leads.filter((l) => l.stage === s)

async function drop(stage) {
  const lead = dragging.value
  over.value = null
  dragging.value = null
  if (!lead || lead.stage === stage) return
  const prev = lead.stage
  lead.stage = stage // optimistic
  if (!(await act(() => agentService.move(lead.id, stage), `${lead.name} → ${humanize(stage)}`))) lead.stage = prev
}
</script>

<template>
  <div>
    <PageHeader title="Lead pipeline" subtitle="Drag cards between stages. Enquiries, viewings and valuations land here automatically." />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="-mx-4 flex gap-4 overflow-x-auto px-4 pb-4">
      <div v-for="s in data.stages" :key="s" class="w-72 shrink-0 rounded-2xl bg-slate-100/80 p-3 transition" :class="{ 'ring-2 ring-brand-400': over === s }"
           @dragover.prevent="over = s" @dragleave="over = null" @drop="drop(s)">
        <div class="mb-3 flex items-center gap-2 px-1">
          <span class="size-2.5 rounded-full" :class="TONE[s]" /><p class="text-sm font-bold capitalize">{{ s }}</p>
          <span class="ml-auto rounded-full bg-white px-2 text-xs font-bold text-slate-500">{{ inStage(s).length }}</span>
        </div>
        <div class="min-h-24 space-y-3">
          <div v-for="l in inStage(s)" :key="l.id" draggable="true" class="card cursor-grab p-4 active:cursor-grabbing" :class="{ 'opacity-40': dragging?.id === l.id }" @dragstart="dragging = l">
            <div class="flex items-start justify-between gap-2">
              <p class="font-semibold">{{ l.name }}</p>
              <span class="inline-flex items-center gap-0.5 rounded-full px-1.5 py-0.5 text-[11px] font-bold" :class="l.score >= 80 ? 'bg-rose-50 text-rose-600' : 'bg-slate-100 text-slate-500'"><Flame v-if="l.score >= 80" class="size-3" />{{ l.score }}</span>
            </div>
            <p class="mt-1 truncate text-xs text-slate-500">{{ l.property_title }}</p>
            <p class="mt-2 text-sm font-bold">{{ compact(l.budget) }}</p>
            <div class="mt-3 flex items-center justify-between text-xs text-slate-400">
              <span class="rounded bg-slate-100 px-1.5 py-0.5 text-slate-600">{{ l.source }}</span><span>{{ date(l.created) }}</span>
            </div>
            <div class="mt-3 flex gap-2 border-t border-slate-100 pt-3">
              <a :href="`mailto:${l.email}`" class="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"><Mail class="size-4" /></a>
              <a :href="`tel:${l.phone}`" class="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700"><Phone class="size-4" /></a>
              <span class="ml-auto self-center text-xs text-slate-400">{{ l.agent }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
