<script setup>
import { useRoute, useRouter } from 'vue-router'
import { Award, BookOpen, Check, Clock, FileText, PlayCircle, Star, Users } from 'lucide-vue-next'
import { act, useResource } from '@/core/resource'
import { money } from '@/core/format'
import { img } from '@/core/media'
import { learningService } from '@/modules/learning/learning.service'
import { catalogService } from '../catalog.service'

const route = useRoute()
const router = useRouter()
const { data: c } = useResource(() => catalogService.detail(route.params.slug))
async function enroll() {
  if (await act(() => learningService.enroll(c.value.slug), `Enrolled in ${c.value.title}`)) router.push(`/learn/${c.value.slug}`)
}
</script>

<template>
  <div v-if="c">
    <section class="bg-slate-950 text-white">
      <div class="mx-auto grid max-w-7xl gap-10 px-6 py-14 lg:grid-cols-3">
        <div class="lg:col-span-2">
          <p class="text-sm font-semibold text-brand-300">{{ c.category }} · {{ c.level }}</p>
          <h1 class="mt-3 text-4xl font-bold tracking-tight">{{ c.title }}</h1>
          <p class="mt-4 max-w-2xl text-lg text-slate-300">{{ c.summary }}</p>
          <p class="mt-5 flex flex-wrap items-center gap-5 text-sm text-slate-300">
            <span class="flex items-center gap-1"><Star class="size-4 fill-amber-400 text-amber-400" /><strong class="text-amber-300">{{ c.rating }}</strong> ({{ c.reviews.toLocaleString() }} ratings)</span>
            <span class="flex items-center gap-1"><Users class="size-4" />{{ c.students.toLocaleString() }} learners</span>
            <span>Created by <strong class="text-white">{{ c.instructor.name }}</strong></span>
          </p>
        </div>
      </div>
    </section>
    <div class="mx-auto grid max-w-7xl gap-10 px-6 py-10 lg:grid-cols-3">
      <div class="space-y-10 lg:col-span-2">
        <section class="rounded-2xl p-6 ring-1 ring-slate-200">
          <h2 class="text-xl font-bold">What you'll learn</h2>
          <div class="mt-4 grid gap-3 sm:grid-cols-2"><p v-for="o in c.outcomes" :key="o" class="flex gap-2 text-slate-700"><Check class="size-5 shrink-0 text-brand-600" />{{ o }}</p></div>
        </section>
        <section>
          <h2 class="text-xl font-bold">Curriculum</h2>
          <p class="mt-1 text-sm text-slate-500">{{ c.lessons.length }} lessons · {{ c.lessons.reduce((s, l) => s + l.minutes, 0) }} min · final assessment</p>
          <ol class="mt-4 divide-y divide-slate-100 rounded-2xl ring-1 ring-slate-200">
            <li v-for="(l, i) in c.lessons" :key="l.id" class="flex items-center gap-3 px-5 py-3.5 text-sm">
              <span class="w-6 text-slate-400">{{ i + 1 }}</span><component :is="l.type === 'video' ? PlayCircle : FileText" class="size-4 text-brand-600" />
              <span class="flex-1">{{ l.title }}</span><span class="text-slate-400">{{ l.minutes }} min</span>
            </li>
            <li class="flex items-center gap-3 bg-brand-50/50 px-5 py-3.5 text-sm font-semibold"><Award class="ml-9 size-4 text-brand-600" /> Final assessment & certificate</li>
          </ol>
        </section>
        <section class="flex gap-5 rounded-2xl bg-slate-50 p-6">
          <img :src="c.instructor.photo + '&w=200&h=200&q=70'" :alt="c.instructor.name" class="size-20 rounded-full object-cover" />
          <div><p class="text-xs font-semibold text-brand-600 uppercase">Instructor</p><p class="text-lg font-bold">{{ c.instructor.name }}</p><p class="text-slate-600">{{ c.instructor.title }}</p><p class="mt-1 text-sm text-slate-500">{{ c.instructor.students.toLocaleString() }} students</p></div>
        </section>
      </div>
      <aside class="lg:-mt-48">
        <div class="card sticky top-24 overflow-hidden shadow-2xl">
          <img :src="img(c.image, 800)" :alt="c.title" class="aspect-video w-full object-cover" />
          <div class="p-6">
            <p class="text-3xl font-bold">{{ money(c.price) }}</p>
            <button class="btn btn-primary mt-4 w-full !py-3.5" @click="enroll">Enroll now</button>
            <RouterLink to="/pricing" class="btn btn-secondary mt-2 w-full">Or get all-access · $29/mo</RouterLink>
            <ul class="mt-6 space-y-2.5 text-sm text-slate-600">
              <li class="flex gap-2"><Clock class="size-4 text-slate-400" />{{ c.hours }} hours on-demand</li>
              <li class="flex gap-2"><BookOpen class="size-4 text-slate-400" />{{ c.lessons.length }} lessons + assessment</li>
              <li class="flex gap-2"><Award class="size-4 text-slate-400" />Verifiable certificate</li>
            </ul>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>
