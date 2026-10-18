<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, ArrowRight, CheckCircle2, Flame, Plus, Trash2 } from 'lucide-vue-next'
import { http } from '@/core/http'
import { act, useResource } from '@/core/resource'
import { productsService } from '@/modules/products/products.service'

const route = useRoute()
const { data: products } = useResource(() => productsService.list())
const step = ref(1)
const STEPS = ['Products', 'Project', 'Contact']
const lines = ref([{ product_id: route.query.product ? +route.query.product : 1, qty: 1, notes: '' }])
const project = ref({ industry: 'Food & beverage', timeline: '1-3 months', budget: '£10k–£50k', services: [] })
const contact = ref({ company: '', name: '', email: '', phone: '', country: 'United Kingdom', message: '' })
const result = ref(null)
const SERVICES = ['Installation', 'Commissioning', 'Maintenance contract', 'Engineering design', 'Operator training']
const INDUSTRIES = ['Food & beverage', 'Water treatment', 'Pharmaceutical', 'Automotive', 'Energy & utilities', 'Aerospace', 'Other']
const productName = (id) => products.value?.find((p) => p.id === id)?.name
const canNext = computed(() => (step.value === 1 ? lines.value.every((l) => l.product_id && l.qty > 0) : true))

async function submit() {
  const res = await act(() => http.post('/quotes', { lines: lines.value, ...project.value, ...contact.value }))
  if (res) { result.value = res; step.value = 4 }
}
</script>

<template>
  <div class="bg-slate-50 py-16">
    <div class="mx-auto max-w-3xl px-6">
      <p class="text-sm font-bold tracking-[.2em] text-brand-600 uppercase">Request for quotation</p>
      <h1 class="mt-2 text-4xl font-black uppercase">Get a costed proposal</h1>
      <div v-if="step < 4" class="mt-8 grid grid-cols-3 gap-2">
        <div v-for="(s, i) in STEPS" :key="s"><div class="h-1.5" :class="step > i ? 'bg-brand-500' : 'bg-slate-200'" /><p class="mt-2 text-xs font-bold tracking-wide uppercase" :class="step > i ? 'text-slate-900' : 'text-slate-400'">{{ i + 1 }}. {{ s }}</p></div>
      </div>

      <div class="mt-8 bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <!-- 1 products -->
        <div v-if="step === 1" class="space-y-4">
          <p class="font-bold">Which products do you need?</p>
          <div v-for="(l, i) in lines" :key="i" class="grid grid-cols-12 gap-2">
            <select v-model.number="l.product_id" class="input col-span-7 !rounded-none"><option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option></select>
            <input v-model.number="l.qty" type="number" min="1" class="input col-span-2 !rounded-none" title="Quantity" />
            <input v-model="l.notes" class="input col-span-2 !rounded-none" placeholder="Size/spec" />
            <button class="col-span-1 grid place-items-center text-slate-400 hover:text-rose-600 disabled:opacity-30" :disabled="lines.length === 1" @click="lines.splice(i, 1)"><Trash2 class="size-4" /></button>
          </div>
          <button class="btn btn-sm btn-ghost text-brand-700" @click="lines.push({ product_id: 1, qty: 1, notes: '' })"><Plus class="size-4" /> Add another product</button>
        </div>

        <!-- 2 project -->
        <div v-else-if="step === 2" class="grid gap-5 sm:grid-cols-2">
          <div><label class="label">Industry</label><select v-model="project.industry" class="input !rounded-none"><option v-for="i in INDUSTRIES" :key="i">{{ i }}</option></select></div>
          <div><label class="label">Timeline</label><select v-model="project.timeline" class="input !rounded-none"><option value="asap">As soon as possible</option><option>1-3 months</option><option>3-6 months</option><option>6+ months</option></select></div>
          <div class="sm:col-span-2"><label class="label">Approximate budget</label>
            <div class="grid grid-cols-2 gap-2 sm:grid-cols-4"><button v-for="b in ['< £10k', '£10k–£50k', '£50k–£250k', '£250k+']" :key="b" type="button" class="py-3 text-sm font-bold ring-1" :class="project.budget === b ? 'bg-slate-950 text-white ring-slate-950' : 'ring-slate-200'" @click="project.budget = b">{{ b }}</button></div></div>
          <div class="sm:col-span-2"><label class="label">Additional services</label>
            <div class="flex flex-wrap gap-2"><label v-for="s in SERVICES" :key="s" class="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm ring-1" :class="project.services.includes(s) ? 'bg-brand-50 ring-brand-500' : 'ring-slate-200'"><input v-model="project.services" type="checkbox" :value="s" class="accent-brand-600" />{{ s }}</label></div></div>
        </div>

        <!-- 3 contact -->
        <form v-else-if="step === 3" id="contact-form" class="grid gap-4 sm:grid-cols-2" @submit.prevent="submit">
          <div><label class="label">Company</label><input v-model="contact.company" required minlength="2" class="input !rounded-none" /></div>
          <div><label class="label">Your name</label><input v-model="contact.name" required minlength="2" class="input !rounded-none" /></div>
          <div><label class="label">Work email</label><input v-model="contact.email" required type="email" class="input !rounded-none" /></div>
          <div><label class="label">Phone</label><input v-model="contact.phone" class="input !rounded-none" /></div>
          <div class="sm:col-span-2"><label class="label">Anything else?</label><textarea v-model="contact.message" rows="3" class="input !rounded-none" placeholder="Duty point, media, site constraints…" /></div>
          <div class="bg-slate-50 p-4 text-sm sm:col-span-2"><p class="font-bold">Summary</p><p v-for="l in lines" :key="l.product_id" class="text-slate-600">{{ l.qty }} × {{ productName(l.product_id) }}</p><p class="text-slate-600">{{ project.industry }} · {{ project.timeline }} · {{ project.budget }}</p></div>
        </form>

        <!-- 4 done -->
        <div v-else class="py-6 text-center">
          <CheckCircle2 class="mx-auto size-16 text-brand-600" />
          <p class="mt-4 text-2xl font-black uppercase">Request received</p>
          <p class="mt-2 text-slate-600">Your reference is <strong class="font-mono">{{ result.reference }}</strong>. An application engineer will reply {{ result.response_time }}.</p>
          <p v-if="result.priority === 'hot'" class="mx-auto mt-4 inline-flex items-center gap-1.5 bg-orange-50 px-3 py-1 text-sm font-bold text-orange-700"><Flame class="size-4" /> Priority response</p>
          <div class="mt-8"><RouterLink to="/products" class="btn btn-secondary !rounded-none">Back to products</RouterLink></div>
        </div>

        <div v-if="step < 4" class="mt-8 flex justify-between border-t border-slate-100 pt-6">
          <button class="btn btn-ghost !rounded-none" :class="{ invisible: step === 1 }" @click="step--"><ArrowLeft class="size-4" /> Back</button>
          <button v-if="step < 3" class="btn btn-primary !rounded-none" :disabled="!canNext" @click="step++">Continue <ArrowRight class="size-4" /></button>
          <button v-else form="contact-form" class="btn btn-primary !rounded-none">Submit request <ArrowRight class="size-4" /></button>
        </div>
      </div>
    </div>
  </div>
</template>
