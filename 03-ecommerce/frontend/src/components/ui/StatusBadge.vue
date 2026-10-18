<script setup>
import { computed } from 'vue'
import { humanize } from '@/core/format'

const props = defineProps({ status: String, label: String })

// One palette for every status across the app; unknown statuses fall back to slate.
const TONES = {
  emerald: ['paid', 'approved', 'received', 'active', 'in_stock', 'resolved_by_ai', 'completed', 'confirmed', 'delivered',
    'available', 'published', 'passed', 'won', 'hired', 'enabled', 'success', 'occupied', 'certified'],
  amber: ['pending', 'pending_approval', 'submitted', 'in_review', 'low_stock', 'due', 'handed_off', 'processing',
    'scheduled', 'under_offer', 'in_progress', 'negotiation', 'interviewing', 'contacted', 'quoted', 'maintenance'],
  rose: ['overdue', 'rejected', 'out_of_stock', 'expired', 'cancelled', 'failed', 'lost', 'sold', 'late', 'urgent', 'vacant'],
  sky: ['on_leave', 'open', 'shipped', 'new', 'rented', 'qualified', 'checked_in', 'viewing', 'for_rent'],
  slate: ['draft', 'idle', 'archived', 'not_started', 'closed', 'disabled'],
}
const CLASSES = {
  emerald: 'bg-emerald-50 text-emerald-700 ring-emerald-600/15',
  amber: 'bg-amber-50 text-amber-700 ring-amber-600/15',
  rose: 'bg-rose-50 text-rose-700 ring-rose-600/15',
  sky: 'bg-sky-50 text-sky-700 ring-sky-600/15',
  slate: 'bg-slate-100 text-slate-600 ring-slate-500/15',
}
const tone = computed(() => Object.keys(TONES).find((k) => TONES[k].includes(props.status)) ?? 'slate')
</script>

<template>
  <span class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold whitespace-nowrap ring-1 ring-inset" :class="CLASSES[tone]">
    <span class="size-1.5 rounded-full bg-current opacity-70" />{{ label ?? humanize(status) }}
  </span>
</template>
