<script setup>
import { ref } from 'vue'
import { AlertTriangle, Braces, CheckCircle2, Download, FileText, Loader2, Send, Table2, UploadCloud } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import { act, useResource } from '@/core/resource'
import { humanize, money } from '@/core/format'
import { toast } from '@/core/toast'
import { downloadCsv, extractionService } from '../extraction.service'

const { data: lib, reload } = useResource(extractionService.samples)
const STAGES = ['Uploading', 'OCR & layout analysis', 'Classifying document', 'Extracting fields', 'Validating']
const stage = ref(-1)
const result = ref(null)
const view = ref('table')
const dragging = ref(false)

async function run(job) {
  result.value = null
  stage.value = 0
  const ticker = setInterval(() => { if (stage.value < STAGES.length - 1) stage.value++ }, 380)
  const [res] = await Promise.all([act(job), new Promise((r) => setTimeout(r, 1900))])
  clearInterval(ticker)
  stage.value = -1
  if (res) { result.value = res; reload() }
}
const runSample = (s) => run(() => extractionService.runSample(s.name))
function onFiles(files) {
  dragging.value = false
  const file = files?.[0]
  if (file) run(() => extractionService.upload(file))
}
const confTone = (c) => (c >= 0.95 ? 'bg-emerald-500' : c >= 0.88 ? 'bg-amber-400' : 'bg-rose-500')
function exportCsv() { downloadCsv(result.value); toast('CSV downloaded') }
</script>

<template>
  <div>
    <PageHeader title="Document & PDF extraction" subtitle="Turn invoices, receipts, contracts and POs into structured data" />

    <div class="grid gap-6 xl:grid-cols-3">
      <div class="space-y-6">
        <label
          class="flex cursor-pointer flex-col items-center gap-3 rounded-3xl border-2 border-dashed p-10 text-center transition"
          :class="dragging ? 'border-brand-500 bg-brand-50' : 'border-slate-200 bg-white hover:border-brand-300 hover:bg-brand-50/40'"
          @dragover.prevent="dragging = true" @dragleave="dragging = false" @drop.prevent="onFiles($event.dataTransfer.files)"
        >
          <span class="grid size-14 place-items-center rounded-2xl bg-brand-100 text-brand-600"><UploadCloud class="size-7" /></span>
          <span class="font-semibold">Drop a document here</span>
          <span class="text-sm text-slate-500">PDF, PNG, JPG or TXT · up to 15 MB</span>
          <span class="btn btn-sm btn-primary mt-1">Browse files</span>
          <input type="file" class="hidden" accept=".pdf,.png,.jpg,.jpeg,.txt,.csv" @change="onFiles($event.target.files)" />
        </label>

        <div class="card p-5">
          <p class="text-sm font-bold">Or try a sample</p>
          <button v-for="s in lib?.samples" :key="s.name" class="mt-2 flex w-full items-center gap-3 rounded-xl border border-slate-100 p-3 text-left text-sm transition hover:border-brand-200 hover:bg-brand-50/40" @click="runSample(s)">
            <FileText class="size-5 text-rose-500" />
            <span class="flex-1 truncate font-medium">{{ s.name }}</span>
            <span class="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] text-slate-500">{{ humanize(s.type) }}</span>
          </button>
        </div>

        <div v-if="lib?.history.length" class="card p-5">
          <p class="text-sm font-bold">Processed this session</p>
          <ul class="mt-3 space-y-2 text-sm">
            <li v-for="h in lib.history" :key="h.id" class="flex items-center gap-2"><CheckCircle2 class="size-4 text-emerald-500" /><span class="flex-1 truncate">{{ h.filename }}</span><span class="font-mono text-xs text-slate-400">{{ Math.round(h.avg_confidence * 100) }}%</span></li>
          </ul>
        </div>
      </div>

      <div class="xl:col-span-2">
        <!-- Processing -->
        <div v-if="stage >= 0" class="card p-8">
          <p class="font-bold">Processing document…</p>
          <ol class="mt-6 space-y-4">
            <li v-for="(s, i) in STAGES" :key="s" class="flex items-center gap-3 text-sm" :class="i > stage ? 'text-slate-400' : 'text-slate-800'">
              <Loader2 v-if="i === stage" class="size-5 animate-spin text-brand-600" />
              <CheckCircle2 v-else-if="i < stage" class="size-5 text-emerald-500" />
              <span v-else class="size-5 rounded-full border-2 border-slate-200" />
              {{ s }}
            </li>
          </ol>
          <div class="mt-6 h-1.5 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full bg-gradient-to-r from-brand-500 to-fuchsia-500 transition-all duration-300" :style="{ width: ((stage + 1) / STAGES.length) * 100 + '%' }" /></div>
        </div>

        <!-- Result -->
        <div v-else-if="result" class="card overflow-hidden">
          <div class="flex flex-wrap items-center gap-4 border-b border-slate-100 p-6">
            <span class="grid size-12 place-items-center rounded-2xl bg-rose-50 text-rose-500"><FileText class="size-6" /></span>
            <div class="flex-1">
              <p class="font-bold">{{ result.filename }}</p>
              <p class="text-sm text-slate-500">{{ humanize(result.doc_type) }} · {{ result.pages }} page{{ result.pages > 1 ? 's' : '' }} · processed in {{ (result.processing_ms / 1000).toFixed(1) }}s</p>
            </div>
            <div class="text-right"><p class="text-2xl font-extrabold text-emerald-600">{{ (result.avg_confidence * 100).toFixed(1) }}%</p><p class="text-xs text-slate-500">avg. confidence</p></div>
          </div>
          <div v-if="result.needs_review.length" class="flex items-center gap-2 bg-amber-50 px-6 py-3 text-sm text-amber-800">
            <AlertTriangle class="size-4" /> Human review suggested for: <strong>{{ result.needs_review.join(', ') }}</strong>
          </div>
          <div class="flex items-center gap-2 px-6 pt-5">
            <div class="inline-flex rounded-xl bg-slate-100 p-1">
              <button class="tab !py-1.5" :class="{ 'tab-active': view === 'table' }" @click="view = 'table'"><Table2 class="mr-1 inline size-4" />Fields</button>
              <button class="tab !py-1.5" :class="{ 'tab-active': view === 'json' }" @click="view = 'json'"><Braces class="mr-1 inline size-4" />JSON</button>
            </div>
            <button class="btn btn-sm btn-secondary ml-auto" @click="exportCsv"><Download class="size-3.5" /> CSV</button>
            <button class="btn btn-sm btn-primary" @click="toast('Sent to ERP as draft bill')"><Send class="size-3.5" /> Send to ERP</button>
          </div>

          <div v-if="view === 'table'" class="p-6">
            <div class="grid gap-3 sm:grid-cols-2">
              <div v-for="f in result.fields" :key="f.key" class="rounded-xl border border-slate-100 p-3">
                <div class="flex items-center justify-between"><p class="label !mb-0">{{ f.label }}</p><span class="font-mono text-[11px] text-slate-400">{{ (f.confidence * 100).toFixed(1) }}%</span></div>
                <input v-model="f.value" class="mt-1 w-full bg-transparent font-semibold text-slate-800 outline-none" />
                <div class="mt-2 h-1 overflow-hidden rounded-full bg-slate-100"><div class="h-full rounded-full" :class="confTone(f.confidence)" :style="{ width: f.confidence * 100 + '%' }" /></div>
              </div>
            </div>
            <table v-if="result.line_items.length" class="table-base mt-6">
              <thead><tr><th>Line item</th><th class="text-right">Qty</th><th class="text-right">Unit price</th><th class="text-right">Amount</th></tr></thead>
              <tbody><tr v-for="l in result.line_items" :key="l.description"><td>{{ l.description }}</td><td class="text-right">{{ l.qty }}</td><td class="text-right">{{ money(l.unit_price, 2) }}</td><td class="text-right font-semibold">{{ money(l.amount, 2) }}</td></tr></tbody>
            </table>
          </div>
          <pre v-else class="m-6 max-h-[480px] overflow-auto rounded-2xl bg-slate-950 p-5 font-mono text-xs leading-relaxed text-emerald-300">{{ JSON.stringify(result, null, 2) }}</pre>
        </div>

        <div v-else class="card grid h-full min-h-96 place-items-center p-10 text-center">
          <div>
            <span class="mx-auto grid size-16 place-items-center rounded-3xl bg-gradient-to-br from-brand-100 to-fuchsia-100 text-brand-600"><FileText class="size-8" /></span>
            <p class="mt-4 font-bold">Extraction results appear here</p>
            <p class="mt-1 max-w-sm text-sm text-slate-500">Upload your own file or pick a sample. Text files are parsed for real values (totals, dates, invoice numbers).</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
