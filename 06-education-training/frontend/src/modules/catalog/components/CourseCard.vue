<script setup>
import { BookOpen, Clock, Star } from 'lucide-vue-next'
import { money } from '@/core/format'
import { img } from '@/core/media'

defineProps({ course: Object })
</script>

<template>
  <RouterLink :to="`/course/${course.slug}`" class="group flex flex-col overflow-hidden rounded-2xl bg-white ring-1 ring-slate-200 transition hover:-translate-y-1 hover:shadow-xl">
    <div class="relative aspect-video overflow-hidden">
      <img :src="img(course.image, 600)" :alt="course.title" loading="lazy" class="size-full object-cover transition duration-500 group-hover:scale-105" />
      <span v-if="course.bestseller" class="absolute top-3 left-3 rounded-md bg-amber-400 px-2 py-0.5 text-xs font-bold text-amber-950">Bestseller</span>
    </div>
    <div class="flex flex-1 flex-col p-5">
      <p class="text-xs font-semibold text-brand-600">{{ course.category }} · {{ course.level }}</p>
      <p class="mt-1.5 font-bold leading-snug text-slate-900 group-hover:text-brand-700">{{ course.title }}</p>
      <p class="mt-1 text-sm text-slate-500">{{ course.instructor }}</p>
      <p class="mt-2 flex items-center gap-1 text-sm"><span class="font-bold text-amber-600">{{ course.rating }}</span><Star class="size-3.5 fill-amber-400 text-amber-400" /><span class="text-slate-400">({{ course.reviews.toLocaleString() }})</span></p>
      <div class="mt-auto flex items-center justify-between pt-4 text-sm text-slate-500">
        <span class="flex gap-3"><span class="flex items-center gap-1"><BookOpen class="size-4" />{{ course.lessons_count }}</span><span class="flex items-center gap-1"><Clock class="size-4" />{{ course.hours }}h</span></span>
        <span class="text-lg font-bold text-slate-900">{{ money(course.price) }}</span>
      </div>
    </div>
  </RouterLink>
</template>
