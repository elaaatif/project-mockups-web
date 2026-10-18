<script setup>
import { computed, ref } from 'vue'
import { Flame, Mail } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, money } from '@/core/format'
import { crmService } from '../crm.service'

const { data, error, reload } = useResource(crmService.rfqs)
const priority = ref('all')
const rows = computed(() => data.value.filter((r) => priority.value === 'all' || r.priority === priority.value))
const STAGES = ['new', 'qualified', 'quoted', 'negotiation', 'won', 'lost']
const P_TONE = { hot: 'bg-orange-100 text-orange-700', warm: 'bg-amber-50 text-amber-700', cold: 'bg-slate-100 text-slate-500' }
const active = ref(null)

async function setStage(r, stage) {
  const res = await act(() => crmService.updateRfq(r.id, { stage }), `${r.id} → ${stage}`)
  if (res) Object.assign(r, res)
}
</script>

<template>
  <div>
    <PageHeader title="Quote requests" subtitle="Auto-scored RFQs from the website, sorted by priority" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="card overflow-hidden">
      <div class="border-b border-slate-100 p-4"><div class="inline-flex rounded-xl bg-slate-100 p-1"><button v-for="p in ['all', 'hot', 'warm', 'cold']" :key="p" class="tab capitalize" :class="{ 'tab-active': priority === p }" @click="priority = p">{{ p }}</button></div></div>
      <div class="overflow-x-auto">
        <table class="table-base">
          <thead><tr><th>Ref</th><th>Company</th><th>Products</th><th>Budget / timeline</th><th>Score</th><th class="text-right">Est. value</th><th>Stage</th></tr></thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id" class="cursor-pointer hover:bg-slate-50" @click="active = r">
              <td class="font-mono text-xs font-bold">{{ r.id }}</td>
              <td><p class="font-semibold">{{ r.company }}</p><p class="text-xs text-slate-500">{{ r.industry }} · {{ r.source }}</p></td>
              <td class="max-w-56 text-sm"><p v-for="l in r.lines" :key="l.product_id" class="truncate">{{ l.qty }} × {{ l.name }}</p></td>
              <td class="text-sm"><p>{{ r.budget }}</p><p class="text-xs text-slate-500">{{ r.timeline }}</p></td>
              <td><span class="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-bold capitalize" :class="P_TONE[r.priority]"><Flame v-if="r.priority === 'hot'" class="size-3" />{{ r.score }} · {{ r.priority }}</span></td>
              <td class="text-right font-semibold">{{ money(r.value) }}</td>
              <td @click.stop><select :value="r.stage" class="input !w-auto !py-1.5 capitalize" @change="setStage(r, $event.target.value)"><option v-for="s in STAGES" :key="s" :value="s">{{ s }}</option></select></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <Modal :open="!!active" :title="active?.company" :subtitle="`${active?.id} · received ${date(active?.created)}`" @close="active = null">
      <div v-if="active" class="space-y-4 text-sm">
        <div class="grid grid-cols-2 gap-3 rounded-2xl bg-slate-50 p-4">
          <div><p class="label">Contact</p><p class="font-semibold">{{ active.name }}</p><p class="text-slate-500">{{ active.email }}</p></div>
          <div><p class="label">Country</p><p class="font-semibold">{{ active.country }}</p></div>
          <div><p class="label">Services</p><p class="font-semibold">{{ active.services.join(', ') || '—' }}</p></div>
          <div><p class="label">Lead score</p><p class="font-semibold">{{ active.score }}/100</p></div>
        </div>
        <ul class="space-y-1"><li v-for="l in active.lines" :key="l.product_id">• {{ l.qty }} × {{ l.name }} <span v-if="l.notes" class="text-slate-500">({{ l.notes }})</span></li></ul>
        <p v-if="active.message" class="rounded-xl bg-slate-50 p-3 text-slate-600">“{{ active.message }}”</p>
        <a :href="`mailto:${active.email}?subject=Your quotation ${active.id}`" class="btn btn-primary w-full"><Mail class="size-4" /> Reply with quotation</a>
      </div>
    </Modal>
  </div>
</template>
