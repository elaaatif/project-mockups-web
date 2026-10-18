<script setup>
import { reactive, watch } from 'vue'
import { Search } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import CourseCard from '../components/CourseCard.vue'
import { catalogService } from '../catalog.service'

const f = reactive({ q: '', category: '', level: '' })
const { data: categories } = useResource(catalogService.categories)
const { data, loading, reload } = useResource(() => catalogService.list(f))
let t
watch(f, () => { clearTimeout(t); t = setTimeout(reload, 200) })
</script>

<template>
  <div class="mx-auto max-w-7xl px-6 py-12">
    <h1 class="text-4xl font-bold tracking-tight">All courses</h1>
    <div class="mt-6 flex flex-wrap gap-3">
      <div class="relative min-w-64 flex-1"><Search class="absolute top-1/2 left-3.5 size-4 -translate-y-1/2 text-slate-400" /><input v-model="f.q" class="input pl-10" placeholder="What do you want to learn?" /></div>
      <select v-model="f.level" class="input !w-auto"><option value="">All levels</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select>
    </div>
    <div class="mt-4 flex flex-wrap gap-2">
      <button class="rounded-full px-4 py-1.5 text-sm font-semibold ring-1" :class="!f.category ? 'bg-brand-600 text-white ring-brand-600' : 'ring-slate-200'" @click="f.category = ''">All</button>
      <button v-for="c in categories" :key="c" class="rounded-full px-4 py-1.5 text-sm font-semibold ring-1" :class="f.category === c ? 'bg-brand-600 text-white ring-brand-600' : 'ring-slate-200 hover:ring-slate-400'" @click="f.category = c">{{ c }}</button>
    </div>
    <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4" :class="{ 'opacity-60': loading }"><CourseCard v-for="c in data" :key="c.id" :course="c" /></div>
    <p v-if="data && !data.length" class="py-20 text-center text-slate-500">No courses found.</p>
  </div>
</template>
