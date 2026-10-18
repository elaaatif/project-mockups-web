<script setup>
import { Award, PlayCircle } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { date } from '@/core/format'
import { img } from '@/core/media'
import { learningService } from '../learning.service'

const { data } = useResource(learningService.myCourses)
</script>

<template>
  <div class="mx-auto max-w-5xl px-6 py-12">
    <h1 class="text-4xl font-bold tracking-tight">My learning</h1>
    <p class="mt-2 text-slate-600">Welcome back, Alex. Pick up where you left off.</p>
    <div class="mt-8 space-y-4">
      <div v-for="e in data" :key="e.slug" class="card flex flex-col gap-5 p-5 sm:flex-row sm:items-center">
        <img :src="img(e.image, 300)" :alt="e.title" class="aspect-video w-full rounded-xl object-cover sm:w-48" />
        <div class="flex-1">
          <p class="text-xs font-semibold text-brand-600">{{ e.category }}</p>
          <p class="mt-1 text-lg font-bold">{{ e.title }}</p>
          <p class="text-sm text-slate-500">Enrolled {{ date(e.enrolled) }} · {{ e.completed.length }}/{{ e.lessons_total }} lessons</p>
          <div class="mt-3 flex items-center gap-3"><div class="h-2 flex-1 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-brand-600" :style="{ width: e.progress + '%' }" /></div><span class="text-sm font-bold">{{ e.progress }}%</span></div>
        </div>
        <div class="flex shrink-0 flex-col gap-2">
          <RouterLink :to="`/learn/${e.slug}`" class="btn btn-primary"><PlayCircle class="size-4" />{{ e.progress === 100 ? 'Review' : e.progress ? 'Continue' : 'Start' }}</RouterLink>
          <RouterLink v-if="e.certificate_id" :to="`/certificate/${e.certificate_id}`" class="btn btn-secondary"><Award class="size-4 text-amber-500" /> Certificate</RouterLink>
        </div>
      </div>
      <p v-if="data && !data.length" class="rounded-2xl bg-slate-50 p-10 text-center text-slate-500">No courses yet. <RouterLink to="/courses" class="font-semibold text-brand-700">Browse the catalogue →</RouterLink></p>
    </div>
  </div>
</template>
