<script setup>
import { Building2 } from 'lucide-vue-next'
import { useResource } from '@/core/resource'
import { ownerService } from '../owner.service'
import { currentBusiness } from '../owner.store'

const { data } = useResource(ownerService.businesses)
</script>

<template>
  <label class="relative inline-flex items-center">
    <Building2 class="pointer-events-none absolute left-3 size-4 text-brand-600" />
    <select v-model="currentBusiness" class="input !w-auto pl-9 font-semibold">
      <option v-for="b in data" :key="b.slug" :value="b.slug">{{ b.name }}</option>
    </select>
  </label>
</template>
