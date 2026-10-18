<script setup>
defineProps({ error: String })
defineEmits(['retry'])
</script>

<template>
  <div v-if="error" class="card grid place-items-center gap-3 p-12 text-center">
    <p class="font-semibold text-slate-800">Couldn't reach the API</p>
    <p class="max-w-sm text-sm text-slate-500">{{ error }} — make sure the FastAPI backend is running.</p>
    <button class="btn btn-secondary" @click="$emit('retry')">Try again</button>
  </div>
  <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
    <div v-for="i in 8" :key="i" class="h-28 animate-pulse rounded-2xl bg-slate-200/60" />
  </div>
</template>
