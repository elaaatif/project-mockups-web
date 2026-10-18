<script setup>
import { computed } from 'vue'
import { Clock, MapPin, UserRound } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { useResource } from '@/core/resource'
import { agentService } from '../agent.service'

const { data, error, reload } = useResource(agentService.appointments)
const byDay = computed(() => {
  const g = {}
  for (const v of data.value ?? []) (g[v.date] ??= []).push(v)
  return Object.entries(g)
})
const label = (d) => new Date(d + 'T00:00').toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' })
</script>

<template>
  <div>
    <PageHeader title="Viewings" subtitle="Upcoming accompanied viewings — booked online or by the team" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="space-y-8">
      <section v-for="[d, list] in byDay" :key="d">
        <h3 class="mb-3 text-sm font-bold tracking-wide text-slate-500 uppercase">{{ label(d) }}</h3>
        <div class="grid gap-3 md:grid-cols-2 xl:grid-cols-3">
          <div v-for="v in list" :key="v.id" class="card flex gap-4 p-4">
            <div class="grid w-16 shrink-0 place-items-center rounded-xl bg-slate-900 text-white"><Clock class="size-4 text-brand-400" /><span class="font-bold">{{ v.time }}</span></div>
            <div class="min-w-0">
              <RouterLink :to="`/property/${v.property_title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`" class="block truncate font-semibold hover:text-brand-700">{{ v.property_title }}</RouterLink>
              <p class="flex items-center gap-1 truncate text-xs text-slate-500"><MapPin class="size-3.5" />{{ v.address }}</p>
              <p class="mt-2 flex items-center gap-1 text-sm"><UserRound class="size-4 text-slate-400" />{{ v.name }}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
