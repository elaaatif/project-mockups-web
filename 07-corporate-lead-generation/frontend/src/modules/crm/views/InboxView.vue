<script setup>
import { Mail } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date } from '@/core/format'
import { crmService } from '../crm.service'

const { data, error, reload } = useResource(crmService.messages)
async function close(m) { const r = await act(() => crmService.updateMessage(m.id, 'closed'), 'Marked as handled'); if (r) Object.assign(m, r) }
</script>

<template>
  <div>
    <PageHeader title="Contact inbox" subtitle="Messages from the website contact form" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="space-y-3">
      <div v-for="m in data" :key="m.id" class="card p-5" :class="{ 'opacity-60': m.status === 'closed' }">
        <div class="flex flex-wrap items-start gap-3">
          <div class="flex-1"><p class="font-bold">{{ m.name }} <span class="font-normal text-slate-500">· {{ m.company || 'No company' }}</span></p><p class="text-xs text-slate-500">{{ m.email }} · {{ date(m.created) }} · {{ m.topic }}</p></div>
          <StatusBadge :status="m.status" />
        </div>
        <p class="mt-3 text-slate-700">{{ m.message }}</p>
        <div class="mt-4 flex gap-2"><a :href="`mailto:${m.email}`" class="btn btn-sm btn-secondary"><Mail class="size-3.5" /> Reply</a><button v-if="m.status !== 'closed'" class="btn btn-sm btn-success" @click="close(m)">Mark handled</button></div>
      </div>
      <p v-if="!data.length" class="card p-10 text-center text-slate-500">Inbox zero 🎉</p>
    </div>
  </div>
</template>
