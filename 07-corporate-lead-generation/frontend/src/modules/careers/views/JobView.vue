<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, CheckCircle2, MapPin, Paperclip, Wallet } from 'lucide-vue-next'
import { act, useResource } from '@/core/resource'
import { setSeo } from '@/core/seo'
import { careersService } from '../careers.service'

const route = useRoute()
const { data: j } = useResource(() => careersService.job(route.params.slug))
watch(j, (v) => v && setSeo({ title: v.title, description: v.summary, jsonLd: {
  '@type': 'JobPosting', title: v.title, description: v.summary, datePosted: v.posted, employmentType: v.type.toUpperCase().replace('-', '_'),
  hiringOrganization: { '@type': 'Organization', name: 'Vertex Industrial' }, jobLocation: { '@type': 'Place', address: { '@type': 'PostalAddress', addressLocality: v.location } } } }))

const form = ref({ name: '', email: '', phone: '', linkedin: '', cover: '' })
const cv = ref(null)
const done = ref(null)
async function apply() {
  const res = await act(() => careersService.apply(j.value.slug, form.value, cv.value))
  if (res) done.value = res
}
</script>

<template>
  <div v-if="j" class="mx-auto grid max-w-7xl gap-12 px-6 py-14 lg:grid-cols-5">
    <article class="lg:col-span-3">
      <RouterLink to="/careers" class="flex items-center gap-1 text-sm text-slate-500 hover:text-slate-900"><ArrowLeft class="size-4" /> All roles</RouterLink>
      <p class="mt-6 text-sm font-bold tracking-widest text-brand-600 uppercase">{{ j.department }}</p>
      <h1 class="mt-2 text-4xl font-black uppercase">{{ j.title }}</h1>
      <p class="mt-4 flex flex-wrap gap-5 text-slate-600"><span class="flex items-center gap-1.5"><MapPin class="size-4" />{{ j.location }} · {{ j.remote }}</span><span class="flex items-center gap-1.5"><Wallet class="size-4" />{{ j.salary }}</span></p>
      <p class="mt-8 text-lg text-slate-700">{{ j.summary }}</p>
      <h2 class="mt-10 text-xl font-black uppercase">What you'll do</h2>
      <ul class="mt-4 space-y-2"><li v-for="r in j.responsibilities" :key="r" class="flex gap-2"><CheckCircle2 class="mt-0.5 size-5 shrink-0 text-brand-600" />{{ r }}</li></ul>
      <h2 class="mt-10 text-xl font-black uppercase">What you'll bring</h2>
      <ul class="mt-4 space-y-2"><li v-for="r in j.requirements" :key="r" class="flex gap-2"><CheckCircle2 class="mt-0.5 size-5 shrink-0 text-slate-400" />{{ r }}</li></ul>
    </article>
    <aside class="lg:col-span-2">
      <div class="sticky top-24 bg-slate-950 p-8 text-white">
        <div v-if="done" class="py-6 text-center"><CheckCircle2 class="mx-auto size-14 text-brand-500" /><p class="mt-4 text-xl font-black uppercase">Application sent</p><p class="mt-2 text-slate-400">Reference <span class="font-mono text-white">{{ done.reference }}</span>. Our talent team reviews every application within 5 working days.</p></div>
        <form v-else class="space-y-3" @submit.prevent="apply">
          <h2 class="text-xl font-black uppercase">Apply now</h2>
          <input v-model="form.name" required minlength="2" class="input !rounded-none" placeholder="Full name" />
          <input v-model="form.email" required type="email" class="input !rounded-none" placeholder="Email" />
          <input v-model="form.phone" class="input !rounded-none" placeholder="Phone" />
          <input v-model="form.linkedin" class="input !rounded-none" placeholder="LinkedIn URL (optional)" />
          <label class="flex cursor-pointer items-center gap-3 border border-dashed border-white/30 p-4 text-sm hover:border-brand-500">
            <Paperclip class="size-5 text-brand-500" /><span class="flex-1 truncate">{{ cv?.name ?? 'Attach CV (PDF or Word, max 5 MB)' }}</span>
            <input type="file" required accept=".pdf,.doc,.docx" class="sr-only" @change="cv = $event.target.files[0]" />
          </label>
          <textarea v-model="form.cover" rows="4" class="input !rounded-none" placeholder="Why this role? (optional)" />
          <button class="btn btn-primary w-full !rounded-none">Submit application</button>
        </form>
      </div>
    </aside>
  </div>
</template>
