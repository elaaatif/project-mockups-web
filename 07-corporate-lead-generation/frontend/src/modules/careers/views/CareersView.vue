<script setup>
import { ref, watch } from 'vue'
import { ArrowRight, Briefcase, GraduationCap, HeartPulse, MapPin, PiggyBank, Search } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import { careersService } from '../careers.service'

const dept = ref('')
const q = ref('')
const { data, reload } = useResource(() => careersService.jobs({ department: dept.value, q: q.value }))
watch([dept, q], reload)
</script>

<template>
  <div>
    <section class="relative bg-slate-950 text-white">
      <img :src="img('https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop', 1800)" alt="Vertex team workshop" class="absolute inset-0 size-full object-cover opacity-25" />
      <div class="relative mx-auto max-w-7xl px-6 py-28"><p class="text-sm font-bold tracking-[.2em] text-brand-400 uppercase">Careers</p><h1 class="mt-4 max-w-3xl text-5xl font-black uppercase">Build things that keep the world running</h1><p class="mt-4 max-w-xl text-lg text-slate-300">1,450 engineers, makers and problem-solvers. Employee-owned, so you share in what we build.</p></div>
    </section>
    <section class="mx-auto grid max-w-7xl gap-6 px-6 py-14 md:grid-cols-4">
      <div v-for="b in [[PiggyBank, 'Employee ownership', 'Annual profit share for everyone'], [GraduationCap, 'Chartership support', 'IMechE & IET paid membership'], [HeartPulse, 'Private healthcare', 'For you and your family'], [Briefcase, '33 days holiday', 'Including bank holidays']]" :key="b[1]" class="border-l-4 border-brand-500 bg-slate-50 p-5">
        <component :is="b[0]" class="size-6 text-brand-600" /><p class="mt-3 font-bold">{{ b[1] }}</p><p class="text-sm text-slate-500">{{ b[2] }}</p>
      </div>
    </section>
    <section class="mx-auto max-w-7xl px-6">
      <div class="flex flex-wrap items-center gap-3">
        <h2 class="mr-auto text-3xl font-black uppercase">Open roles <span class="text-slate-400">({{ data?.jobs.length ?? '…' }})</span></h2>
        <div class="relative"><Search class="absolute top-1/2 left-3 size-4 -translate-y-1/2 text-slate-400" /><input v-model="q" class="input !rounded-none pl-9" placeholder="Title or location" /></div>
        <select v-model="dept" class="input !w-auto !rounded-none"><option value="">All departments</option><option v-for="d in data?.departments" :key="d">{{ d }}</option></select>
      </div>
      <div class="mt-6 divide-y divide-slate-200 border-y border-slate-200">
        <RouterLink v-for="j in data?.jobs" :key="j.id" :to="`/careers/${j.slug}`" class="group flex flex-wrap items-center gap-4 py-6 hover:bg-slate-50 sm:px-4">
          <div class="min-w-64 flex-1"><p class="text-lg font-bold group-hover:text-brand-700">{{ j.title }}</p><p class="text-sm text-slate-500">{{ j.department }} · {{ j.type }}</p></div>
          <span class="flex items-center gap-1 text-sm text-slate-600"><MapPin class="size-4" />{{ j.location }} · {{ j.remote }}</span>
          <span class="w-40 text-sm font-semibold">{{ j.salary }}</span>
          <ArrowRight class="size-5 text-slate-300 transition group-hover:translate-x-1 group-hover:text-brand-600" />
        </RouterLink>
      </div>
    </section>
  </div>
</template>
