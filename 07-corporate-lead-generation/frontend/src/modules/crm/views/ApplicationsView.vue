<script setup>
import { FileText, Star } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { avatarGradient, date, humanize, initials } from '@/core/format'
import { crmService } from '../crm.service'

const { data, error, reload } = useResource(crmService.applications)
const COLUMNS = ['new', 'interviewing', 'hired', 'rejected']
const TONE = { new: 'bg-sky-500', interviewing: 'bg-amber-500', hired: 'bg-emerald-500', rejected: 'bg-slate-400' }
async function move(a, status) { const r = await act(() => crmService.updateApplication(a.id, status), `${a.name} → ${humanize(status)}`); if (r) Object.assign(a, r) }
</script>

<template>
  <div>
    <PageHeader title="Job applications" subtitle="Candidates from the recruitment portal" />
    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="grid gap-4 lg:grid-cols-4">
      <div v-for="c in COLUMNS" :key="c" class="rounded-2xl bg-slate-100/80 p-3">
        <p class="mb-3 flex items-center gap-2 px-1 text-sm font-bold capitalize"><span class="size-2.5 rounded-full" :class="TONE[c]" />{{ c }}<span class="ml-auto rounded-full bg-white px-2 text-xs text-slate-500">{{ data.filter((a) => a.status === c).length }}</span></p>
        <div class="space-y-3">
          <div v-for="a in data.filter((x) => x.status === c)" :key="a.id" class="card p-4">
            <div class="flex items-center gap-3">
              <span class="grid size-9 place-items-center rounded-full bg-gradient-to-br text-xs font-bold text-white" :class="avatarGradient(a.name)">{{ initials(a.name) }}</span>
              <div class="min-w-0"><p class="truncate font-semibold">{{ a.name }}</p><p class="truncate text-xs text-slate-500">{{ a.job_title }}</p></div>
            </div>
            <div class="mt-3 flex items-center justify-between text-xs text-slate-500">
              <span class="flex items-center gap-1"><FileText class="size-3.5" />{{ a.cv_name }}</span>
              <span v-if="a.rating" class="flex">
                <Star v-for="i in 5" :key="i" class="size-3" :class="i <= a.rating ? 'fill-amber-400 text-amber-400' : 'text-slate-300'" />
              </span>
            </div>
            <p class="mt-1 text-xs text-slate-400">Applied {{ date(a.created) }}</p>
            <div class="mt-3 flex flex-wrap gap-1">
              <button v-for="s in COLUMNS.filter((x) => x !== c)" :key="s" class="rounded-md bg-slate-100 px-2 py-1 text-[11px] font-semibold capitalize hover:bg-slate-200" @click="move(a, s)">→ {{ s }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
