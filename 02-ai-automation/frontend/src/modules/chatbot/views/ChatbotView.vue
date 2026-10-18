<script setup>
import { nextTick, ref } from 'vue'
import { Bot, Globe, Mail, MessageCircle, RotateCcw, SendHorizontal, Star, UserRound } from 'lucide-vue-next'
import PageHeader from '@/components/ui/PageHeader.vue'
import StatusBadge from '@/components/ui/StatusBadge.vue'
import { useResource } from '@/core/resource'
import { avatarGradient, initials } from '@/core/format'
import { chatbotService } from '../chatbot.service'

const greeting = { from: 'bot', text: "Hi! I'm Nova, Lumen Home's assistant. Ask me about orders, returns, shipping or products.", suggestions: ['Where is my order?', 'Return policy', 'Shipping times'] }
const messages = ref([greeting])
const draft = ref('')
const typing = ref(false)
const scroller = ref(null)

const { data: inbox } = useResource(chatbotService.conversations)
const channelIcon = { web: Globe, whatsapp: MessageCircle, email: Mail }

const bold = (t) => t.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c]).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')

async function scrollDown() {
  await nextTick()
  scroller.value?.scrollTo({ top: scroller.value.scrollHeight, behavior: 'smooth' })
}

async function send(text = draft.value) {
  text = text.trim()
  if (!text || typing.value) return
  messages.value.push({ from: 'user', text })
  draft.value = ''
  typing.value = true
  scrollDown()
  try {
    const [res] = await Promise.all([chatbotService.send(text), new Promise((r) => setTimeout(r, 650))])
    messages.value.push({ from: 'bot', text: res.reply, suggestions: res.suggestions, meta: res })
  } catch (e) {
    messages.value.push({ from: 'bot', text: `⚠️ ${e.message}` })
  } finally {
    typing.value = false
    scrollDown()
  }
}
const reset = () => { messages.value = [greeting] }
</script>

<template>
  <div>
    <PageHeader title="AI Support Chatbot" subtitle="Test the live assistant, then see how it performs across channels" />

    <div class="grid gap-6 xl:grid-cols-5">
      <!-- Playground -->
      <div class="card flex h-[640px] flex-col overflow-hidden xl:col-span-3">
        <div class="flex items-center gap-3 bg-gradient-to-r from-brand-600 to-fuchsia-600 px-5 py-4 text-white">
          <span class="grid size-10 place-items-center rounded-full bg-white/20"><Bot class="size-5" /></span>
          <div class="flex-1"><p class="font-semibold">Nova — Lumen Home</p><p class="text-xs text-brand-100">Trained on 214 help articles · order system connected</p></div>
          <button class="rounded-lg p-2 hover:bg-white/15" title="Reset conversation" @click="reset"><RotateCcw class="size-4" /></button>
        </div>
        <div ref="scroller" class="flex-1 space-y-4 overflow-y-auto bg-slate-50 p-5">
          <div v-for="(m, i) in messages" :key="i" class="flex gap-2.5" :class="m.from === 'user' ? 'flex-row-reverse' : ''">
            <span class="grid size-8 shrink-0 place-items-center rounded-full" :class="m.from === 'user' ? 'bg-slate-200 text-slate-600' : 'bg-brand-100 text-brand-700'">
              <component :is="m.from === 'user' ? UserRound : Bot" class="size-4" />
            </span>
            <div class="max-w-[78%]">
              <p class="rounded-2xl px-4 py-2.5 text-sm leading-relaxed" :class="m.from === 'user' ? 'rounded-tr-md bg-brand-600 text-white' : 'rounded-tl-md bg-white text-slate-700 shadow-sm ring-1 ring-slate-100'" v-html="bold(m.text)" />
              <div v-if="m.meta" class="mt-1.5 flex flex-wrap gap-1.5 font-mono text-[11px]">
                <span class="rounded bg-brand-50 px-1.5 py-0.5 text-brand-700">{{ m.meta.intent }}</span>
                <span class="rounded bg-emerald-50 px-1.5 py-0.5 text-emerald-700">{{ Math.round(m.meta.confidence * 100) }}%</span>
                <span class="rounded bg-slate-100 px-1.5 py-0.5 text-slate-500">{{ m.meta.latency_ms }}ms</span>
                <span v-if="m.meta.handoff" class="rounded bg-amber-50 px-1.5 py-0.5 text-amber-700">→ human handoff</span>
                <span v-for="(v, k) in m.meta.entities" :key="k" class="rounded bg-sky-50 px-1.5 py-0.5 text-sky-700">{{ k }}={{ v }}</span>
              </div>
              <div v-if="m.suggestions?.length && i === messages.length - 1" class="mt-2 flex flex-wrap gap-2">
                <button v-for="s in m.suggestions" :key="s" class="rounded-full border border-brand-200 bg-white px-3 py-1 text-xs font-medium text-brand-700 transition hover:bg-brand-50" @click="send(s)">{{ s }}</button>
              </div>
            </div>
          </div>
          <div v-if="typing" class="flex gap-2.5">
            <span class="grid size-8 place-items-center rounded-full bg-brand-100 text-brand-700"><Bot class="size-4" /></span>
            <p class="typing flex gap-1 rounded-2xl rounded-tl-md bg-white px-4 py-3.5 shadow-sm"><span class="size-1.5 rounded-full bg-slate-400" /><span class="size-1.5 rounded-full bg-slate-400" /><span class="size-1.5 rounded-full bg-slate-400" /></p>
          </div>
        </div>
        <form class="flex gap-2 border-t border-slate-100 bg-white p-4" @submit.prevent="send()">
          <input v-model="draft" class="input" placeholder="Try: “Where is order 10482?” or “I want to talk to a human”" />
          <button class="btn btn-primary !px-3.5" :disabled="!draft.trim() || typing"><SendHorizontal class="size-5" /></button>
        </form>
      </div>

      <!-- Inbox -->
      <div class="space-y-6 xl:col-span-2">
        <div v-if="inbox" class="grid grid-cols-3 gap-3">
          <div class="card p-4 text-center"><p class="text-2xl font-extrabold text-brand-600">{{ inbox.stats.ai_resolution }}%</p><p class="text-xs text-slate-500">AI resolved</p></div>
          <div class="card p-4 text-center"><p class="flex items-center justify-center gap-1 text-2xl font-extrabold text-amber-500">{{ inbox.stats.csat }}<Star class="size-4 fill-current" /></p><p class="text-xs text-slate-500">CSAT</p></div>
          <div class="card p-4 text-center"><p class="text-2xl font-extrabold text-emerald-600">{{ inbox.stats.avg_response_s }}s</p><p class="text-xs text-slate-500">First reply</p></div>
        </div>
        <div class="card overflow-hidden">
          <h3 class="border-b border-slate-100 px-5 py-4 font-bold">Recent conversations</h3>
          <ul class="max-h-[490px] divide-y divide-slate-100 overflow-y-auto">
            <li v-for="c in inbox?.conversations" :key="c.id" class="flex items-center gap-3 px-5 py-3.5 hover:bg-slate-50">
              <span class="relative grid size-10 shrink-0 place-items-center rounded-full bg-gradient-to-br text-xs font-bold text-white" :class="avatarGradient(c.customer)">
                {{ initials(c.customer) }}
                <span class="absolute -right-1 -bottom-1 grid size-5 place-items-center rounded-full bg-white text-slate-500 ring-1 ring-slate-200"><component :is="channelIcon[c.channel]" class="size-3" /></span>
              </span>
              <div class="min-w-0 flex-1">
                <div class="flex items-center justify-between gap-2"><p class="truncate text-sm font-semibold">{{ c.customer }}</p><span class="text-[11px] text-slate-400">{{ c.minutes_ago < 60 ? c.minutes_ago + 'm' : Math.floor(c.minutes_ago / 60) + 'h' }}</span></div>
                <p class="truncate text-xs text-slate-500">{{ c.last_message }}</p>
              </div>
              <StatusBadge :status="c.status" :label="c.status === 'resolved_by_ai' ? 'AI resolved' : undefined" />
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
