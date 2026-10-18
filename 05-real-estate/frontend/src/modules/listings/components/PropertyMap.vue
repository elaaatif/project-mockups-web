<script setup>
// Leaflet map with price pins. Emits `select` when a pin is hovered; click opens the property.
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { shortPrice } from '../listings.service'

const props = defineProps({ properties: { type: Array, default: () => [] }, activeId: Number, zoom: { type: Number, default: 11 } })
const emit = defineEmits(['select'])
const router = useRouter()
const el = ref(null)
let map
let layer
const markers = new Map()

const pin = (p) => L.divIcon({ className: '', html: `<div class="price-pin ${p.id === props.activeId ? 'active' : ''}">${shortPrice(p)}</div>`, iconSize: [0, 0] })

function render() {
  if (!map) return
  layer.clearLayers()
  markers.clear()
  for (const p of props.properties) {
    const m = L.marker([p.lat, p.lng], { icon: pin(p) }).addTo(layer)
      .on('mouseover', () => emit('select', p.id))
      .on('click', () => router.push(`/property/${p.slug}`))
    markers.set(p.id, m)
  }
  const bounds = props.properties.map((p) => [p.lat, p.lng])
  if (bounds.length > 1) map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 })
  else if (bounds.length === 1) map.setView(bounds[0], props.zoom)
}

onMounted(() => {
  map = L.map(el.value, { scrollWheelZoom: false }).setView([51.507, -0.128], props.zoom)
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '&copy; OpenStreetMap contributors', maxZoom: 19, className: 'map-tiles' }).addTo(map)
  layer = L.layerGroup().addTo(map)
  render()
})
watch(() => props.properties, render)
watch(() => props.activeId, () => props.properties.forEach((p) => markers.get(p.id)?.setIcon(pin(p))))
onBeforeUnmount(() => map?.remove())
</script>

<template>
  <div ref="el" class="z-0 size-full min-h-80 overflow-hidden rounded-2xl" />
</template>
