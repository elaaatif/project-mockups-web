<script setup>
import { computed, ref } from 'vue'
import { Check, CheckCircle2, Circle, FileText, Upload, X, XCircle } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import Modal from '@/components/ui/Modal.vue'
import LoadingState from '@/components/ui/LoadingState.vue'
import { act, useResource } from '@/core/resource'
import { date } from '@/core/format'
import { documentsService } from '../documents.service'

const { data, error, reload } = useResource(documentsService.list)
const filter = ref('all')
const selectedId = ref(null)
const comment = ref('')

const docs = computed(() => (data.value?.documents ?? []).filter((d) =>
  filter.value === 'all' || (filter.value === 'open' ? ['submitted', 'in_review'].includes(d.status) : d.status === filter.value)))
const selected = computed(() => data.value?.documents.find((d) => d.id === selectedId.value) ?? docs.value[0])
const open = computed(() => selected.value && ['submitted', 'in_review'].includes(selected.value.status))
const currentStep = computed(() => selected.value?.steps.find((s) => s.status === 'pending'))

async function decide(decision) {
  const doc = await act(() => documentsService.decide(selected.value.id, decision, comment.value), decision === 'approve' ? 'Approved — routed to next approver' : 'Document rejected')
  if (doc) { comment.value = ''; await reload(); selectedId.value = doc.id }
}

const showNew = ref(false)
const form = ref({ title: '', type: 'Contract' })
const fileName = ref('')
function pickFile(e) {
  fileName.value = e.target.files[0]?.name ?? ''
  if (!form.value.title) form.value.title = fileName.value.replace(/\.\w+$/, '')
}
async function create() {
  const doc = await act(() => documentsService.create(form.value), 'Document submitted for approval')
  if (doc) { showNew.value = false; form.value = { title: '', type: 'Contract' }; fileName.value = ''; await reload(); selectedId.value = doc.id }
}
</script>

<template>
  <div>
    <PageHeader title="Documents & Approvals" subtitle="Route contracts, policies and requests through a three-step approval chain">
      <button class="btn btn-primary" @click="showNew = true"><Upload class="size-4" /> Upload document</button>
    </PageHeader>

    <LoadingState v-if="!data" :error="error" @retry="reload" />
    <div v-else class="grid gap-6 lg:grid-cols-5">
      <div class="card overflow-hidden lg:col-span-2">
        <div class="flex gap-1 border-b border-slate-100 p-3">
          <button v-for="f in ['all', 'open', 'approved', 'rejected']" :key="f" class="tab !py-1.5 capitalize" :class="{ '!bg-brand-50 !text-brand-700': filter === f }" @click="filter = f">{{ f }}</button>
        </div>
        <ul class="max-h-[560px] divide-y divide-slate-100 overflow-y-auto">
          <li v-for="d in docs" :key="d.id">
            <button class="flex w-full items-start gap-3 p-4 text-left transition hover:bg-slate-50" :class="{ 'bg-brand-50/60': selected?.id === d.id }" @click="selectedId = d.id">
              <span class="grid size-10 shrink-0 place-items-center rounded-xl bg-slate-100 text-slate-500"><FileText class="size-5" /></span>
              <div class="min-w-0 flex-1"><p class="truncate font-semibold text-slate-800">{{ d.title }}</p><p class="text-xs text-slate-500">{{ d.type }} · {{ d.owner }} · {{ date(d.created) }}</p></div>
              <StatusBadge :status="d.status" />
            </button>
          </li>
        </ul>
      </div>

      <div v-if="selected" class="card p-6 lg:col-span-3">
        <div class="flex items-start justify-between gap-4">
          <div><p class="text-xs font-semibold text-brand-600 uppercase">{{ selected.type }}</p><h2 class="mt-1 text-xl font-extrabold">{{ selected.title }}</h2>
            <p class="mt-1 text-sm text-slate-500">Submitted by {{ selected.owner }} on {{ date(selected.created) }} · {{ selected.size_kb }} KB PDF</p></div>
          <StatusBadge :status="selected.status" />
        </div>

        <div class="mt-6 grid h-40 place-items-center rounded-2xl border border-dashed border-slate-200 bg-slate-50 text-sm text-slate-400">
          <div class="text-center"><FileText class="mx-auto size-10 text-slate-300" /><p class="mt-2">Document preview</p></div>
        </div>

        <h3 class="mt-8 font-bold">Approval chain</h3>
        <ol class="relative mt-4 space-y-6 border-l-2 border-slate-100 pl-6">
          <li v-for="(s, i) in selected.steps" :key="i" class="relative">
            <span class="absolute top-0 -left-[35px] grid size-6 place-items-center rounded-full bg-white">
              <CheckCircle2 v-if="s.status === 'approved'" class="size-6 text-emerald-500" />
              <XCircle v-else-if="s.status === 'rejected'" class="size-6 text-rose-500" />
              <Circle v-else class="size-6" :class="s === currentStep && open ? 'animate-pulse text-amber-400' : 'text-slate-300'" />
            </span>
            <p class="font-semibold text-slate-800">{{ s.role }} <span class="font-normal text-slate-500">· {{ s.approver }}</span></p>
            <p class="text-xs text-slate-500">{{ s.at ? `${s.status} on ${date(s.at)}` : s === currentStep && open ? 'Awaiting decision' : 'Waiting' }}</p>
            <p v-if="s.comment" class="mt-1.5 rounded-lg bg-slate-50 px-3 py-2 text-sm text-slate-600">“{{ s.comment }}”</p>
          </li>
        </ol>

        <div v-if="open" class="mt-8 rounded-2xl bg-slate-50 p-4">
          <p class="text-sm font-semibold">Acting as <span class="text-brand-700">{{ currentStep.approver }}</span> ({{ currentStep.role }})</p>
          <textarea v-model="comment" rows="2" class="input mt-3" placeholder="Add a comment (optional)" />
          <div class="mt-3 flex justify-end gap-2">
            <button class="btn btn-danger" @click="decide('reject')"><X class="size-4" /> Reject</button>
            <button class="btn btn-primary" @click="decide('approve')"><Check class="size-4" /> Approve</button>
          </div>
        </div>
      </div>
    </div>

    <Modal :open="showNew" title="Upload document" subtitle="It will start at the Department Head step" @close="showNew = false">
      <form class="space-y-4" @submit.prevent="create">
        <label class="flex cursor-pointer flex-col items-center gap-2 rounded-2xl border-2 border-dashed border-slate-200 p-8 text-center transition hover:border-brand-400 hover:bg-brand-50/40">
          <Upload class="size-8 text-brand-500" />
          <span class="text-sm font-semibold">{{ fileName || 'Click to choose a PDF or DOCX' }}</span>
          <span class="text-xs text-slate-500">Max 20 MB</span>
          <input type="file" class="hidden" accept=".pdf,.doc,.docx" @change="pickFile" />
        </label>
        <div><label class="label">Title</label><input v-model="form.title" required minlength="3" class="input" /></div>
        <div><label class="label">Type</label><select v-model="form.type" class="input"><option v-for="t in data?.types" :key="t">{{ t }}</option></select></div>
        <div class="flex justify-end gap-2"><button type="button" class="btn btn-ghost" @click="showNew = false">Cancel</button><button class="btn btn-primary">Submit for approval</button></div>
      </form>
    </Modal>
  </div>
</template>
