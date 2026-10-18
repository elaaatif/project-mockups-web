<script setup>
import { watch } from 'vue'
import { Clock, ExternalLink, UserRound } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { money } from '@/core/format'
import BusinessSwitcher from '../components/BusinessSwitcher.vue'
import { ownerService } from '../owner.service'
import { currentBusiness } from '../owner.store'

const { data, error, reload } = useResource(() => ownerService.business(currentBusiness.value))
watch(currentBusiness, reload)
</script>

<template>
  <div>
    <PageHeader title="Services & team" subtitle="What customers can book and who delivers it">
      <BusinessSwitcher />
      <RouterLink v-if="data" :to="`/b/${data.slug}`" class="btn btn-secondary"><ExternalLink class="size-4" /> Public page</RouterLink>
    </PageHeader>
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="grid gap-6 lg:grid-cols-2">
      <div class="card p-6">
        <h3 class="font-bold">Services</h3>
        <div class="mt-4 divide-y divide-slate-100">
          <div v-for="s in data.services" :key="s.id" class="flex items-center gap-4 py-3">
            <div class="flex-1"><p class="font-semibold">{{ s.name }}</p><p class="flex items-center gap-1 text-xs text-slate-500"><Clock class="size-3.5" />{{ s.minutes }} min · slots every {{ data.slot_minutes }} min</p></div>
            <span v-if="s.deposit" class="rounded-full bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-700">{{ money(s.deposit) }} deposit</span>
            <p class="w-20 text-right font-bold">{{ s.price ? money(s.price) + (s.per_person ? ' pp' : '') : 'Free' }}</p>
          </div>
        </div>
      </div>
      <div class="card p-6">
        <h3 class="font-bold">{{ data.kind === 'table' ? 'Seating areas' : 'Team members' }}</h3>
        <div class="mt-4 grid gap-3 sm:grid-cols-2">
          <div v-for="s in data.staff" :key="s.id" class="flex items-center gap-3 rounded-2xl bg-slate-50 p-4">
            <span class="grid size-11 place-items-center rounded-full bg-white text-brand-600 ring-1 ring-slate-200"><UserRound class="size-5" /></span>
            <div><p class="font-semibold">{{ s.name }}</p><p class="text-xs text-slate-500">{{ s.role }}</p></div>
          </div>
        </div>
        <p class="mt-6 rounded-xl bg-brand-50 p-4 text-sm text-brand-900">Opening hours: <strong>{{ data.open }}–{{ data.close }}</strong>, every day.</p>
      </div>
    </div>
  </div>
</template>
