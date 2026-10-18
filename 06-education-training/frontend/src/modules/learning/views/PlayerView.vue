<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Award, CheckCircle2, ChevronRight, Circle, FileText, Lock, PlayCircle, RotateCcw, XCircle } from 'lucide-vue-next'
import { act } from '@/core/resource'
import { img } from '@/core/media'
import { catalogService } from '@/modules/catalog/catalog.service'
import { learningService } from '../learning.service'

const route = useRoute()
const slug = route.params.slug
const course = ref(null)
const progress = ref(null)
const currentId = ref(null)
const mode = ref('lesson') // lesson | quiz | result
const quiz = ref(null)
const answers = ref([])
const result = ref(null)

const lesson = computed(() => course.value?.lessons.find((l) => l.id === currentId.value))
const isDone = (id) => progress.value?.completed.includes(id)
const allDone = computed(() => progress.value && progress.value.completed.length === course.value.lessons.length)

onMounted(async () => {
  course.value = await catalogService.detail(slug)
  progress.value = await learningService.progress(slug).catch(() => learningService.enroll(slug))
  currentId.value = course.value.lessons.find((l) => !isDone(l.id))?.id ?? course.value.lessons[0].id
})

async function completeAndNext() {
  const p = await act(() => learningService.complete(slug, currentId.value))
  if (!p) return
  progress.value = p
  const idx = course.value.lessons.findIndex((l) => l.id === currentId.value)
  if (idx < course.value.lessons.length - 1) currentId.value = course.value.lessons[idx + 1].id
  else openQuiz()
}
async function openQuiz() {
  quiz.value = await act(() => learningService.quiz(slug))
  answers.value = Array(quiz.value.questions.length).fill(null)
  mode.value = 'quiz'
}
async function submitQuiz() {
  const r = await act(() => learningService.submitQuiz(slug, answers.value))
  if (r) { result.value = r; mode.value = 'result'; progress.value = await learningService.progress(slug) }
}
</script>

<template>
  <div class="flex h-screen flex-col bg-slate-950 text-slate-200">
    <header class="flex h-14 shrink-0 items-center gap-4 border-b border-white/10 px-4">
      <RouterLink to="/my-learning" class="rounded-lg p-2 hover:bg-white/10"><ArrowLeft class="size-5" /></RouterLink>
      <p class="truncate font-semibold text-white">{{ course?.title }}</p>
      <div v-if="progress" class="ml-auto flex items-center gap-3 text-sm">
        <div class="hidden h-1.5 w-40 overflow-hidden rounded-full bg-white/10 sm:block"><div class="h-full rounded-full bg-brand-500 transition-all" :style="{ width: progress.progress + '%' }" /></div>
        <span>{{ progress.progress }}% complete</span>
      </div>
    </header>

    <div v-if="course && progress" class="flex min-h-0 flex-1">
      <main class="min-w-0 flex-1 overflow-y-auto">
        <!-- Lesson -->
        <template v-if="mode === 'lesson' && lesson">
          <div class="relative aspect-video max-h-[62vh] w-full bg-black">
            <img :src="img(course.image, 1400)" alt="" class="size-full object-cover opacity-40" />
            <div class="absolute inset-0 grid place-items-center text-center">
              <div>
                <component :is="lesson.type === 'video' ? PlayCircle : FileText" class="mx-auto size-20 text-white/90" />
                <p class="mt-4 text-2xl font-bold text-white">{{ lesson.title }}</p>
                <p class="text-white/60">{{ lesson.type === 'video' ? 'Video' : 'Reading' }} · {{ lesson.minutes }} min</p>
              </div>
            </div>
          </div>
          <div class="mx-auto max-w-3xl p-8">
            <p class="text-sm text-brand-300">Lesson {{ course.lessons.indexOf(lesson) + 1 }} of {{ course.lessons.length }}</p>
            <h1 class="mt-1 text-2xl font-bold text-white">{{ lesson.title }}</h1>
            <p class="mt-4 leading-relaxed text-slate-400">In this lesson we cover the key ideas behind <strong class="text-slate-200">{{ lesson.title.toLowerCase() }}</strong>, walk through a worked example, and finish with a short practice task you can apply at work today. Download the exercise file from the resources tab to follow along.</p>
            <div class="mt-8 flex flex-wrap gap-3">
              <button class="btn btn-primary" @click="completeAndNext"><CheckCircle2 class="size-4" />{{ isDone(lesson.id) ? 'Next lesson' : 'Mark complete & continue' }}</button>
              <button v-if="allDone" class="btn bg-amber-400 text-amber-950 hover:bg-amber-300" @click="openQuiz"><Award class="size-4" /> Take the assessment</button>
            </div>
          </div>
        </template>

        <!-- Quiz -->
        <div v-else-if="mode === 'quiz'" class="mx-auto max-w-3xl p-8">
          <p class="text-sm text-brand-300">Final assessment · pass mark {{ quiz.pass_mark }}%</p>
          <h1 class="mt-1 text-2xl font-bold text-white">Show what you've learned</h1>
          <div class="mt-8 space-y-6">
            <div v-for="(q, i) in quiz.questions" :key="q.id" class="rounded-2xl bg-white/5 p-6 ring-1 ring-white/10">
              <p class="font-semibold text-white">{{ i + 1 }}. {{ q.q }}</p>
              <div class="mt-4 grid gap-2">
                <label v-for="(o, oi) in q.options" :key="oi" class="flex cursor-pointer items-center gap-3 rounded-xl px-4 py-3 ring-1 transition" :class="answers[i] === oi ? 'bg-brand-600/20 ring-brand-500' : 'ring-white/10 hover:bg-white/5'">
                  <input v-model="answers[i]" type="radio" :value="oi" class="accent-brand-500" />{{ o }}
                </label>
              </div>
            </div>
          </div>
          <button class="btn btn-primary mt-8 w-full !py-3.5" :disabled="answers.includes(null)" @click="submitQuiz">Submit answers</button>
        </div>

        <!-- Result -->
        <div v-else-if="mode === 'result'" class="mx-auto max-w-2xl p-8 text-center">
          <component :is="result.passed ? Award : XCircle" class="mx-auto size-20" :class="result.passed ? 'text-amber-400' : 'text-rose-400'" />
          <p class="mt-4 text-5xl font-bold text-white">{{ result.score }}%</p>
          <p class="mt-2 text-lg">{{ result.passed ? 'Congratulations — you passed!' : `You need ${result.pass_mark}% to pass. Review and try again.` }}</p>
          <div class="mt-6 flex justify-center gap-2">
            <span v-for="(r, i) in result.results" :key="i" class="grid size-10 place-items-center rounded-full" :class="r.correct ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'">{{ i + 1 }}</span>
          </div>
          <div class="mt-8 flex justify-center gap-3">
            <RouterLink v-if="result.certificate" :to="`/certificate/${result.certificate.id}`" class="btn bg-amber-400 text-amber-950 hover:bg-amber-300"><Award class="size-4" /> View certificate</RouterLink>
            <button v-else class="btn btn-primary" @click="openQuiz"><RotateCcw class="size-4" /> Retake</button>
          </div>
        </div>
      </main>

      <aside class="hidden w-80 shrink-0 overflow-y-auto border-l border-white/10 lg:block">
        <p class="px-5 pt-5 pb-3 text-xs font-semibold tracking-wider text-slate-500 uppercase">Course content</p>
        <button v-for="(l, i) in course.lessons" :key="l.id" class="flex w-full items-center gap-3 px-5 py-3 text-left text-sm transition hover:bg-white/5" :class="{ 'bg-white/10 text-white': mode === 'lesson' && l.id === currentId }" @click="currentId = l.id; mode = 'lesson'">
          <CheckCircle2 v-if="isDone(l.id)" class="size-5 shrink-0 text-emerald-400" /><Circle v-else class="size-5 shrink-0 text-slate-600" />
          <span class="flex-1">{{ i + 1 }}. {{ l.title }}</span><span class="text-xs text-slate-500">{{ l.minutes }}m</span>
        </button>
        <button class="flex w-full items-center gap-3 border-t border-white/10 px-5 py-4 text-left text-sm font-semibold" :class="allDone ? 'text-amber-300 hover:bg-white/5' : 'cursor-not-allowed text-slate-600'" :disabled="!allDone" @click="openQuiz">
          <component :is="allDone ? Award : Lock" class="size-5" /> Final assessment<ChevronRight class="ml-auto size-4" />
        </button>
      </aside>
    </div>
  </div>
</template>
