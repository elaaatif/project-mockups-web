<script setup>
import { ref } from 'vue'
import { Building2, CalendarDays, Mail } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, money } from '@/core/format'
import { quotesService } from '../quotes.service'

const { data, error, reload } = useResource(quotesService.list)
const active = ref(null)
const price = ref(0)
function open(q) { active.value = q; price.value = q.quoted_total ?? Math.round(q.estimate * 0.95) }
async function respond(status) {
  const body = { status, quoted_total: status === 'quoted' ? price.value : undefined }
  if (await act(() => quotesService.respond(active.value.id, body), `Quote #${active.value.id} marked ${status}`)) { active.value = null; reload() }
}
</script>

<template>
  <div>
    <PageHeader title="Quote requests" subtitle="B2B requests from the website, with an instant wholesale estimate" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="grid gap-4 lg:grid-cols-2">
      <button v-for="q in data" :key="q.id" class="card p-5 text-left transition hover:shadow-md" @click="open(q)">
        <div class="flex items-start justify-between gap-3">
          <div><p class="font-bold">{{ q.company }}</p><p class="text-sm text-slate-500">#{{ q.id }} · {{ q.contact }} · {{ date(q.created) }}</p></div>
          <StatusBadge :status="q.status" />
        </div>
        <ul class="mt-4 space-y-1 text-sm">
          <li v-for="i in q.items" :key="i.product_id" class="flex justify-between"><span>{{ i.name }}</span><span class="font-semibold">× {{ i.qty }}</span></li>
        </ul>
        <div class="mt-4 flex justify-between border-t border-slate-100 pt-3 text-sm">
          <span class="text-slate-500">Tier estimate {{ money(q.estimate) }}</span>
          <span v-if="q.quoted_total" class="font-bold text-brand-700">Quoted {{ money(q.quoted_total) }}</span>
        </div>
      </button>
    </div>

    <Modal :open="!!active" :title="active?.company" :subtitle="`Quote request #${active?.id}`" @close="active = null">
      <div v-if="active" class="space-y-4 text-sm">
        <p class="flex items-center gap-2"><Mail class="size-4 text-slate-400" />{{ active.email }} {{ active.phone && '· ' + active.phone }}</p>
        <p v-if="active.needed_by" class="flex items-center gap-2"><CalendarDays class="size-4 text-slate-400" />Needed by {{ date(active.needed_by) }}</p>
        <p v-if="active.notes" class="flex gap-2 rounded-xl bg-slate-50 p-3"><Building2 class="size-4 shrink-0 text-slate-400" />{{ active.notes }}</p>
        <div><label class="label">Quoted total ($)</label><input v-model.number="price" type="number" class="input" /><p class="mt-1 text-xs text-slate-500">Wholesale tier estimate: {{ money(active.estimate, 2) }}</p></div>
        <div class="flex flex-wrap justify-end gap-2">
          <button class="btn btn-danger" @click="respond('lost')">Mark lost</button>
          <button class="btn btn-success" @click="respond('won')">Mark won</button>
          <button class="btn btn-primary" @click="respond('quoted')">Send quote</button>
        </div>
      </div>
    </Modal>
  </div>
</template>
