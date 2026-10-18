<script setup>
import { X } from 'lucide-vue-next'

defineProps({ open: Boolean, title: String, subtitle: String, wide: Boolean })
const emit = defineEmits(['close'])
</script>

<template>
  <Teleport to="body">
    <Transition enter-from-class="opacity-0" leave-to-class="opacity-0" enter-active-class="transition duration-200" leave-active-class="transition duration-150">
      <div v-if="open" class="fixed inset-0 z-50 grid place-items-center bg-slate-900/50 p-4 backdrop-blur-sm" @click.self="emit('close')">
        <div class="card max-h-[90vh] w-full overflow-y-auto p-6 shadow-2xl" :class="wide ? 'max-w-3xl' : 'max-w-lg'">
          <div class="mb-5 flex items-start justify-between gap-4">
            <div>
              <h3 class="text-lg font-bold text-slate-900">{{ title }}</h3>
              <p v-if="subtitle" class="mt-0.5 text-sm text-slate-500">{{ subtitle }}</p>
            </div>
            <button class="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-700" @click="emit('close')"><X class="size-5" /></button>
          </div>
          <slot />
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
