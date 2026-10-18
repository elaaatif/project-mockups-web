<script setup>
import { ref } from 'vue'
import { ArrowDown, ChevronRight, CheckCircle2, FlaskConical, Loader2, Plus, Trash2, Zap } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { number } from '@/core/format'
import { metaFor, workflowsService } from '../workflows.service'

const { data, error, reload } = useResource(workflowsService.list)

async function toggle(wf) {
  const updated = await act(() => workflowsService.toggle(wf.id), `${wf.name} ${wf.enabled ? 'paused' : 'activated'}`)
  if (updated) Object.assign(wf, updated)
}

// Test run with step-by-step reveal
const testing = ref(null)
const log = ref([])
const revealed = ref(0)
async function test(wf) {
  testing.value = wf
  log.value = []
  revealed.value = 0
  const res = await act(() => workflowsService.test(wf.id))
  if (!res) return (testing.value = null)
  log.value = res.log
  for (let i = 1; i <= res.log.length; i++) {
    await new Promise((r) => setTimeout(r, 450))
    revealed.value = i
  }
  wf.runs = (wf.runs ?? 0) + 1
  wf.last_run = 'just now'
}

// Builder
const showBuilder = ref(false)
const draft = ref(null)
const nextAction = ref('')
function openBuilder() {
  const c = data.value.catalog
  draft.value = { name: '', trigger: { ...c.triggers[1] }, steps: [{ ...c.actions[0] }, { ...c.actions[4] }] }
  showBuilder.value = true
}
function addStep() {
  const a = data.value.catalog.actions.find((x) => x.type === nextAction.value)
  if (a) draft.value.steps.push({ ...a })
  nextAction.value = ''
}
async function save() {
  const payload = { name: draft.value.name, trigger: { type: draft.value.trigger.type, label: draft.value.trigger.label }, steps: draft.value.steps.map(({ type, label }) => ({ type, label })) }
  if (await act(() => workflowsService.create(payload), 'Workflow created and activated')) { showBuilder.value = false; reload() }
}
</script>

<template>
  <div>
    <PageHeader title="Email & WhatsApp workflows" subtitle="Trigger → AI steps → actions. Toggle, test and build flows visually.">
      <button class="btn btn-primary" :disabled="!data" @click="openBuilder"><Plus class="size-4" /> New workflow</button>
    </PageHeader>

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="space-y-4">
      <div v-for="wf in data.workflows" :key="wf.id" class="card p-5 transition" :class="{ 'opacity-60': !wf.enabled }">
        <div class="flex flex-wrap items-center gap-4">
          <div class="min-w-48 flex-1">
            <p class="font-bold text-slate-900">{{ wf.name }}</p>
            <p class="text-xs text-slate-500">{{ number(wf.runs) }} runs · {{ wf.success_rate }}% success · last run {{ wf.last_run }}</p>
          </div>
          <button class="btn btn-sm btn-secondary" @click="test(wf)"><FlaskConical class="size-3.5" /> Test run</button>
          <button class="relative h-6 w-11 rounded-full transition" :class="wf.enabled ? 'bg-brand-600' : 'bg-slate-300'" :aria-pressed="wf.enabled" @click="toggle(wf)">
            <span class="absolute top-0.5 left-0.5 size-5 rounded-full bg-white shadow transition" :class="{ 'translate-x-5': wf.enabled }" />
          </button>
        </div>
        <div class="mt-4 flex flex-wrap items-center gap-2">
          <span class="inline-flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-xs font-semibold ring-2 ring-white" :class="metaFor(wf.trigger.type).tone">
            <Zap class="size-3.5" /><component :is="metaFor(wf.trigger.type).icon" class="size-3.5" />{{ wf.trigger.label }}
          </span>
          <template v-for="(s, i) in wf.steps" :key="i">
            <ChevronRight class="size-4 text-slate-300" />
            <span class="inline-flex items-center gap-1.5 rounded-xl px-3 py-1.5 text-xs font-medium" :class="metaFor(s.type).tone"><component :is="metaFor(s.type).icon" class="size-3.5" />{{ s.label }}</span>
          </template>
        </div>
      </div>
    </div>

    <!-- Test run log -->
    <Modal :open="!!testing" :title="`Test run · ${testing?.name}`" subtitle="Executed with a sample payload" @close="testing = null">
      <ol class="space-y-3">
        <li v-for="(s, i) in log" :key="i" class="flex gap-3 rounded-xl border p-3 transition" :class="i < revealed ? 'border-emerald-100 bg-emerald-50/40' : 'border-slate-100 opacity-50'">
          <CheckCircle2 v-if="i < revealed" class="mt-0.5 size-5 shrink-0 text-emerald-500" />
          <Loader2 v-else-if="i === revealed" class="mt-0.5 size-5 shrink-0 animate-spin text-brand-500" />
          <span v-else class="mt-0.5 size-5 shrink-0 rounded-full border-2 border-slate-200" />
          <div class="min-w-0 flex-1">
            <div class="flex justify-between gap-2 text-sm"><p class="font-semibold">{{ s.label }}</p><span class="font-mono text-xs text-slate-400">{{ s.duration_ms }}ms</span></div>
            <p v-if="i < revealed" class="mt-0.5 font-mono text-xs text-slate-600">{{ s.output }}</p>
          </div>
        </li>
        <li v-if="!log.length" class="flex items-center gap-2 text-sm text-slate-500"><Loader2 class="size-4 animate-spin" /> Starting run…</li>
      </ol>
      <p v-if="log.length && revealed === log.length" class="mt-4 rounded-xl bg-slate-900 px-4 py-3 text-sm text-emerald-300">✓ Completed in {{ (log.reduce((a, s) => a + s.duration_ms, 0) / 1000).toFixed(2) }}s</p>
    </Modal>

    <!-- Builder -->
    <Modal :open="showBuilder" title="Build a workflow" subtitle="Pick a trigger, then chain AI steps and actions" wide @close="showBuilder = false">
      <form v-if="draft" class="space-y-5" @submit.prevent="save">
        <div><label class="label">Workflow name</label><input v-model="draft.name" required minlength="3" class="input" placeholder="e.g. WhatsApp order updates" /></div>
        <div class="rounded-2xl bg-slate-50 p-5">
          <label class="label">When this happens…</label>
          <select v-model="draft.trigger" class="input">
            <option v-for="t in data.catalog.triggers" :key="t.type" :value="t">{{ t.label }}</option>
          </select>
          <div class="my-3 flex justify-center"><ArrowDown class="size-5 text-slate-300" /></div>
          <label class="label">…do these steps</label>
          <TransitionGroup tag="ol" class="space-y-2" enter-from-class="opacity-0 -translate-y-1" enter-active-class="transition">
            <li v-for="(s, i) in draft.steps" :key="s.type + i" class="flex items-center gap-3 rounded-xl bg-white p-3 ring-1 ring-slate-200">
              <span class="grid size-8 place-items-center rounded-lg" :class="metaFor(s.type).tone"><component :is="metaFor(s.type).icon" class="size-4" /></span>
              <input v-model="s.label" class="flex-1 bg-transparent text-sm font-medium outline-none" />
              <span class="font-mono text-xs text-slate-400">#{{ i + 1 }}</span>
              <button type="button" class="rounded-lg p-1.5 text-slate-400 hover:bg-rose-50 hover:text-rose-600" :disabled="draft.steps.length === 1" @click="draft.steps.splice(i, 1)"><Trash2 class="size-4" /></button>
            </li>
          </TransitionGroup>
          <div class="mt-3 flex gap-2">
            <select v-model="nextAction" class="input"><option value="" disabled>Add a step…</option><option v-for="a in data.catalog.actions" :key="a.type" :value="a.type">{{ a.label }}</option></select>
            <button type="button" class="btn btn-secondary shrink-0" :disabled="!nextAction" @click="addStep"><Plus class="size-4" /> Add</button>
          </div>
        </div>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showBuilder = false">Cancel</button><button class="btn btn-primary">Save & activate</button></div>
      </form>
    </Modal>
  </div>
</template>
