<script setup>
import { Mail } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, money } from '@/core/format'
import { portfolioService } from '../portfolio.service'

const { data, error, reload } = useResource(portfolioService.messages)
const STATUS_TONE = { new: 'new', contacted: 'contacted', won: 'won', closed: 'closed' }
async function setStatus(m, s) { const r = await act(() => portfolioService.setStatus(m.id, s), `Marked ${s}`); if (r) Object.assign(m, r) }
</script>

<template>
  <div>
    <PageHeader title="Project enquiries" subtitle="Messages and estimates sent from the portfolio contact form">
      <RouterLink to="/" class="btn btn-secondary">View site</RouterLink>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="space-y-4">
      <div v-for="m in data" :key="m.id" class="card p-6">
        <div class="flex flex-wrap items-start gap-3">
          <div class="flex-1"><p class="font-bold">{{ m.name }} <span class="font-normal text-slate-500">· {{ m.company || 'Individual' }}</span></p><p class="text-xs text-slate-500">{{ m.email }} · {{ date(m.created) }}{{ m.budget ? ` · budget ${m.budget}` : '' }}</p></div>
          <StatusBadge :status="STATUS_TONE[m.status]" />
        </div>
        <p class="mt-3 whitespace-pre-line text-slate-700">{{ m.message }}</p>
        <p v-if="m.estimate" class="mt-3 inline-flex rounded-xl bg-brand-50 px-3 py-2 text-sm text-brand-800">Estimate: {{ m.estimate.label }} · {{ money(m.estimate.low) }}–{{ money(m.estimate.high) }} · {{ m.estimate.weeks }} weeks</p>
        <div class="mt-4 flex flex-wrap gap-2">
          <a :href="`mailto:${m.email}`" class="btn btn-sm btn-primary"><Mail class="size-3.5" /> Reply</a>
          <button v-for="s in ['contacted', 'won', 'closed']" :key="s" class="btn btn-sm btn-secondary capitalize" @click="setStatus(m, s)">{{ s }}</button>
        </div>
      </div>
      <div v-if="!data.length" class="card p-12 text-center text-slate-500">No enquiries yet — they'll appear here when someone uses the contact form.</div>
    </div>
  </div>
</template>
