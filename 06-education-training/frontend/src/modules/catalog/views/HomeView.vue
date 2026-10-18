<script setup>
import { ArrowRight, Award, Building2, CheckCircle2, PlayCircle, School, Users } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { img } from '@/core/media'
import CourseCard from '../components/CourseCard.vue'
import { catalogService } from '../catalog.service'

const { data: courses } = useResource(() => catalogService.list())
const AUDIENCES = [
  { icon: Users, title: 'Individuals', text: 'Self-paced courses with assessments and shareable certificates.', to: '/courses', cta: 'Browse courses' },
  { icon: Building2, title: 'Companies', text: 'Assign mandatory and growth training, and track compliance by team.', to: '/app', cta: 'See the L&D dashboard' },
  { icon: School, title: 'Schools & training centres', text: 'Run cohorts, timetables, attendance and fees in one place.', to: '/app/academy', cta: 'See administration' },
]
</script>

<template>
  <div>
    <section class="relative overflow-hidden bg-brand-950 text-white">
      <div class="absolute -top-32 -right-32 size-[36rem] rounded-full bg-brand-600/30 blur-3xl" />
      <div class="relative mx-auto grid max-w-7xl items-center gap-12 px-6 py-20 lg:grid-cols-2">
        <div>
          <p class="inline-flex items-center gap-2 rounded-full bg-white/10 px-3 py-1 text-xs font-semibold text-brand-200"><Award class="size-4" /> 180,000 certificates issued</p>
          <h1 class="mt-6 text-5xl leading-[1.08] font-bold tracking-tight sm:text-6xl">Learn the skills your next role needs.</h1>
          <p class="mt-5 max-w-lg text-lg text-brand-100/80">Practical courses from industry experts, assessments that prove what you know, and certificates employers can verify.</p>
          <div class="mt-8 flex flex-wrap gap-3">
            <RouterLink to="/courses" class="btn bg-white !px-6 !py-3.5 text-brand-800 hover:bg-brand-50">Explore courses <ArrowRight class="size-4" /></RouterLink>
            <RouterLink to="/learn/excel-data-analysis-masterclass" class="btn !px-6 !py-3.5 text-white ring-1 ring-white/30 hover:bg-white/10"><PlayCircle class="size-5" /> Resume demo course</RouterLink>
          </div>
          <div class="mt-10 flex flex-wrap gap-6 text-sm text-brand-100/80">
            <span v-for="t in ['Self-paced', 'Graded assessments', 'Verifiable certificates']" :key="t" class="flex items-center gap-2"><CheckCircle2 class="size-4 text-emerald-400" />{{ t }}</span>
          </div>
        </div>
        <div class="relative hidden lg:block">
          <img :src="img('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop', 1000)" alt="" class="aspect-[4/3] w-full rounded-3xl object-cover shadow-2xl" />
          <div class="absolute -bottom-6 -left-6 w-72 rounded-2xl bg-white p-4 text-slate-900 shadow-2xl">
            <p class="text-xs font-semibold text-slate-500">Excel & Data Analysis</p>
            <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100"><div class="h-full w-4/7 rounded-full bg-brand-600" /></div>
            <p class="mt-2 text-sm font-bold">57% complete · 3 lessons left</p>
          </div>
        </div>
      </div>
    </section>

    <section class="mx-auto max-w-7xl px-6 py-20">
      <div class="flex items-end justify-between"><h2 class="text-3xl font-bold tracking-tight">Popular courses</h2><RouterLink to="/courses" class="flex items-center gap-1 text-sm font-semibold text-brand-700">View all <ArrowRight class="size-4" /></RouterLink></div>
      <div class="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4"><CourseCard v-for="c in courses?.slice(0, 8)" :key="c.id" :course="c" /></div>
    </section>

    <section class="bg-slate-50 py-20">
      <div class="mx-auto max-w-7xl px-6">
        <h2 class="text-center text-3xl font-bold tracking-tight">One platform, three ways to learn</h2>
        <div class="mt-12 grid gap-6 md:grid-cols-3">
          <div v-for="a in AUDIENCES" :key="a.title" class="rounded-3xl bg-white p-8 ring-1 ring-slate-200">
            <span class="grid size-12 place-items-center rounded-2xl bg-brand-100 text-brand-700"><component :is="a.icon" class="size-6" /></span>
            <h3 class="mt-5 text-xl font-bold">{{ a.title }}</h3><p class="mt-2 text-slate-600">{{ a.text }}</p>
            <RouterLink :to="a.to" class="mt-5 inline-flex items-center gap-1 text-sm font-semibold text-brand-700">{{ a.cta }} <ArrowRight class="size-4" /></RouterLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
