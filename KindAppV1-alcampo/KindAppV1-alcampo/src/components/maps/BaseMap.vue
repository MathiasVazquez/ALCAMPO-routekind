<template>
  <div style="width: 100%">
    <l-map
      v-if="!forcingUpdateMap"
      ref="map"
      style="height: calc(100vh - 200px)"
      :maxZoom="19"
      :zoomAnimation="true"
      :fadeAnimation="true"
      :markerZoomAnimation="true"
      :useGlobalLeaflet="true"
      :options="mapOptions"
      @click="handleMapClick"
      @update:center="centerUpdate"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        :attribution="attribution"
      />

      <!-- MAP EXTRAS -->
      <slot name="map" />

      <!-- MAP FRAGMENTS -->
      <AddressesMapFragment :map="mapObject" :hideSelectedAddress="true" />
      <MobileMapFragment :map="mapObject" />
      <OrdersMapFragment :map="mapObject" />
      <VisitRequiredMapFragment :map="mapObject" />
    </l-map>
  </div>
</template>

<script>
import leaflet from "leaflet"
import "leaflet/dist/leaflet.css"
import {
  LPopup,
  LTooltip,
  LPolyline,
  LMap,
  LTileLayer,
  LMarker,
  LGeoJson,
  LControl,
  LCircleMarker,
} from "@vue-leaflet/vue-leaflet"
import { ref, toRefs, computed, watch, nextTick, onMounted } from "vue"
import { useMapHelpers, useMapBounds } from "src/helpers"
import { useUI, useSettings } from "src/context"
import AddressesMapFragment from "./AddressesMapFragment"
import MobileMapFragment from "./MobileMapFragment"
import OrdersMapFragment from "./OrdersMapFragment"
import VisitRequiredMapFragment from "./VisitRequiredMapFragment.vue"

export default {
  name: "FullRouteMap",
  components: {
    VisitRequiredMapFragment,
    AddressesMapFragment,
    MobileMapFragment,
    OrdersMapFragment,
    LPopup,
    LTooltip,
    LPolyline,
    LMap,
    LTileLayer,
    LMarker,
    LGeoJson,
    LControl,
    LCircleMarker,
  },
  props: ["padding"],
  emit: ["click:map"],
  setup(props, { emit }) {
    const { padding } = toRefs(props)
    const { attribution, url, mapOptions, forcingUpdateMap } = useMapHelpers()
    const { updatingMap, showCenterMapBtn, canShowCenterMapButton } = useUI()

    const map = ref(null)
    const mapObject = computed(() => (map.value || {}).leafletObject)
    const mapIsReady = computed(() => !!(mapObject.value || {}).fitBounds)

    // Map events
    const handleMapClick = (e) => e.latlng && emit("click:map", e)

    // Set initial padding and first update
    const { updateBounds, setMapPadding } = useMapBounds(mapObject)
    watch(mapIsReady, async () => {
      if (!mapIsReady.value) return
      setMapPadding(padding)
      await nextTick()
      updateBounds()
      await new Promise((resolve) => setTimeout(resolve, 1500))
      updateBounds()
      await new Promise((resolve) => setTimeout(resolve, 500))
      canShowCenterMapButton.value = true
    })
    watch(updatingMap, () => updatingMap.value && updateBounds())

    const centerUpdate = () =>
      canShowCenterMapButton.value && (showCenterMapBtn.value = true)
    return {
      url,
      map,
      mapObject,
      mapOptions,
      attribution,
      forcingUpdateMap,
      handleMapClick,
      centerUpdate,
    }
  },
}
</script>

<style scoped>
.header-container {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000;
}
.footer-container {
  position: absolute;
  top: 100vh;
  transform: translateY(-100%);
  left: 0;
  z-index: 1000;
}
</style>
