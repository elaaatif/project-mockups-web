<script setup>
import { ref } from 'vue'
import { AlertTriangle, Car, Fuel, Gauge, ShieldCheck, Truck, User, Wrench } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date, money, number } from '@/core/format'
import { fleetService } from '../fleet.service'

const { data, error, reload } = useResource(fleetService.list)
const serviceProgress = (v) => Math.max(0, Math.min(100, 100 - (v.km_to_service / 10000) * 100))

const target = ref(null)
const form = ref({ notes: 'Oil & filter change', cost: 180 })
async function logService() {
  if (await act(() => fleetService.logService(target.value.id, form.value), `Service logged for ${target.value.plate}`)) {
    target.value = null
    reload()
  }
}
async function renew(v) {
  if (await act(() => fleetService.renewInsurance(v.id), `Insurance renewed for ${v.plate} (12 months)`)) reload()
}
</script>

<template>
  <div>
    <PageHeader title="Fleet & Insurance" subtitle="Mileage-based maintenance, service history and insurance renewals" />

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <template v-else>
      <div v-if="data.alerts.length" class="mb-6 flex flex-wrap items-center gap-x-6 gap-y-2 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-4 text-sm text-amber-800">
        <AlertTriangle class="size-5 shrink-0" />
        <span v-for="(a, i) in data.alerts" :key="i" class="font-medium">{{ a.message }}</span>
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div v-for="v in data.vehicles" :key="v.id" class="card p-5">
          <div class="flex items-start gap-3">
            <span class="grid size-12 place-items-center rounded-2xl" :class="v.type === 'Truck' ? 'bg-amber-50 text-amber-600' : 'bg-brand-50 text-brand-600'">
              <component :is="v.type === 'Car' ? Car : Truck" class="size-6" />
            </span>
            <div class="flex-1">
              <p class="font-bold text-slate-900">{{ v.model }}</p>
              <p class="font-mono text-xs tracking-wider text-slate-500">{{ v.plate }} · {{ v.type }}</p>
            </div>
            <StatusBadge :status="v.status" />
          </div>
          <div class="mt-4 grid grid-cols-3 gap-2 text-xs text-slate-600">
            <span class="flex items-center gap-1"><User class="size-3.5" />{{ v.driver.split(' ')[0] }}</span>
            <span class="flex items-center gap-1"><Gauge class="size-3.5" />{{ number(v.mileage) }} km</span>
            <span class="flex items-center gap-1"><Fuel class="size-3.5" />{{ v.fuel_efficiency }} km/l</span>
          </div>
          <div class="mt-4">
            <div class="flex justify-between text-xs"><span class="font-semibold text-slate-600">Next service</span>
              <span :class="v.service_due ? 'font-bold text-rose-600' : 'text-slate-500'">{{ v.km_to_service <= 0 ? `${number(-v.km_to_service)} km overdue` : `in ${number(v.km_to_service)} km` }}</span></div>
            <div class="mt-1.5 h-2 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full" :class="v.service_due ? 'bg-rose-500' : 'bg-brand-500'" :style="{ width: serviceProgress(v) + '%' }" /></div>
          </div>
          <div class="mt-3 flex items-center justify-between rounded-xl px-3 py-2 text-xs" :class="v.insurance_alert ? 'bg-rose-50 text-rose-700' : 'bg-emerald-50 text-emerald-700'">
            <span class="flex items-center gap-1.5 font-semibold"><ShieldCheck class="size-4" />{{ v.insurance_provider }}</span>
            <span>{{ v.insurance_days_left < 0 ? 'Expired' : `${v.insurance_days_left} days left` }}</span>
          </div>
          <div class="mt-4 flex gap-2">
            <button class="btn btn-sm btn-secondary flex-1" @click="target = v"><Wrench class="size-3.5" /> Log service</button>
            <button v-if="v.insurance_alert" class="btn btn-sm btn-primary flex-1" @click="renew(v)"><ShieldCheck class="size-3.5" /> Renew</button>
          </div>
        </div>
      </div>

      <div class="card mt-6 overflow-x-auto">
        <h3 class="px-6 pt-5 pb-3 font-bold">Maintenance history</h3>
        <table class="table-base">
          <thead><tr><th>Date</th><th>Vehicle</th><th>Work done</th><th class="text-right">Cost</th></tr></thead>
          <tbody>
            <tr v-for="l in data.logs" :key="l.id"><td class="text-slate-500">{{ date(l.date) }}</td><td class="font-mono text-xs font-semibold">{{ l.plate }}</td><td>{{ l.notes }}</td><td class="text-right font-semibold">{{ money(l.cost, 2) }}</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <Modal :open="!!target" :title="`Log service · ${target?.plate}`" subtitle="Resets the next service interval to +10,000 km" @close="target = null">
      <form class="space-y-4" @submit.prevent="logService">
        <div><label class="label">Work performed</label>
          <select v-model="form.notes" class="input"><option>Oil & filter change</option><option>Tyre rotation</option><option>Brake inspection</option><option>Annual inspection</option><option>Major service</option></select></div>
        <div><label class="label">Cost ($)</label><input v-model.number="form.cost" type="number" min="0" class="input" /></div>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="target = null">Cancel</button><button class="btn btn-primary">Save record</button></div>
      </form>
    </Modal>
  </div>
</template>
