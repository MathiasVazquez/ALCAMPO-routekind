<template>
    
  <!-- MAP -->
  
  <BaseMap :addresses="addresses">
    <template v-slot:map>

      <!-- MOBILES -->

      <div v-if="mobileCoords">
        <l-marker 
          v-for="mobile of mobileCoords"
          :key="mobile.id" 
          :lat-lng="mobile.coords" 
          draggable
          @update:lat-lng="e => {}"
        ></l-marker>
      </div>
    </template>
  </BaseMap>
</template>

<script>
import BaseMap from './BaseMap'
import { usePolygonPins, usePolygons, useMobiles } from 'src/context'
import { toRefs, ref, computed, watch, nextTick } from 'vue'
import { LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl} from "@vue-leaflet/vue-leaflet"

export default {
  components: {BaseMap, LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl},
  props: {addresses: Array},
  setup(props) {
    const { addresses } = toRefs(props)
    const { mobiles } = useMobiles()
    const mobileCoords = computed(() => mobiles.value
      .map(m => { return { ...m, coords: { lat: m.lat, lng: m.lng } } })
      .filter(m => m.coords.lat && m.coords.lng)
    )
    
    return {
      addresses,
      mobileCoords,
    }
  },
}
</script>