<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Award, Link2, Printer } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { date } from '@/core/format'
import { toast } from '@/core/toast'
import { learningService } from '../learning.service'

const route = useRoute()
const { data: cert, error } = useResource(() => learningService.certificate(route.params.id))
const verifyUrl = computed(() => `${location.origin}/verify?id=${cert.value?.id}`)
const print = () => window.print()
const copy = () => navigator.clipboard?.writeText(verifyUrl.value).then(() => toast('Verification link copied'))
</script>

<template>
  <div class="min-h-screen bg-slate-100 px-6 py-10">
    <div class="mx-auto flex max-w-5xl items-center gap-2">
      <RouterLink to="/my-learning" class="btn btn-ghost"><ArrowLeft class="size-4" /> My learning</RouterLink>
      <button class="btn btn-secondary ml-auto" @click="copy"><Link2 class="size-4" /> Share link</button>
      <button class="btn btn-primary" @click="print"><Printer class="size-4" /> Print / PDF</button>
    </div>
    <p v-if="error" class="mt-20 text-center text-slate-500">{{ error }}</p>
    <div v-if="cert" class="print-area mx-auto mt-6 max-w-5xl">
      <div class="relative aspect-[1.414] overflow-hidden rounded-xl bg-white p-3 shadow-2xl">
        <div class="flex size-full flex-col items-center justify-center border-[3px] border-double border-brand-800/60 p-10 text-center">
          <div class="absolute top-0 left-0 size-40 -translate-x-1/2 -translate-y-1/2 rounded-full bg-brand-600/10" />
          <div class="absolute right-0 bottom-0 size-56 translate-x-1/3 translate-y-1/3 rounded-full bg-amber-400/15" />
          <p class="flex items-center gap-2 text-sm font-bold tracking-[.3em] text-brand-700 uppercase"><Award class="size-5" /> Brightpath Academy</p>
          <p class="mt-6 text-sm tracking-[.4em] text-slate-500 uppercase">Certificate of completion</p>
          <p class="mt-4 text-6xl text-slate-900" style="font-family: 'Great Vibes', cursive">{{ cert.learner }}</p>
          <p class="mt-4 max-w-xl text-slate-600">has successfully completed all lessons and passed the final assessment with a score of <strong>{{ cert.score }}%</strong> for</p>
          <p class="mt-3 text-2xl font-bold text-brand-900">{{ cert.course }}</p>
          <div class="mt-12 grid w-full max-w-2xl grid-cols-3 items-end gap-6 text-sm">
            <div><p class="border-t border-slate-300 pt-2 font-semibold">{{ cert.instructor }}</p><p class="text-xs text-slate-500">Instructor</p></div>
            <div class="grid place-items-center"><span class="grid size-20 place-items-center rounded-full bg-amber-400 text-amber-950 shadow-inner ring-4 ring-amber-200"><Award class="size-9" /></span></div>
            <div><p class="border-t border-slate-300 pt-2 font-semibold">{{ date(cert.issued) }}</p><p class="text-xs text-slate-500">Date issued · {{ cert.hours }} hours</p></div>
          </div>
          <p class="mt-10 font-mono text-xs text-slate-400">Credential ID {{ cert.id }} · verify at brightpath.academy/verify</p>
        </div>
      </div>
    </div>
  </div>
</template>
