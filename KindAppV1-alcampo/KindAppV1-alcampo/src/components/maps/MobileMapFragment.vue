<template>
  <l-marker
    v-if="formattedCurrentPosition.hasCoords"
    :lat-lng="formattedCurrentPosition.coords"
    :icon="formattedCurrentPosition.icon"
  />
  <MapAddressItem v-if="selectedAddress" :address="selectedAddress" />
</template>

<script>
import leaflet from "leaflet"
import { watch, computed, toRefs, onMounted } from 'vue'
import { useLocation, useAddresses, useUI } from 'src/context'
import { useMapDistance, useMapBounds, useMapCurve } from 'src/helpers'
import { LMarker } from '@vue-leaflet/vue-leaflet'
import MapAddressItem from './MapAddressItem'

export default {
  props: ['map'],
  components: {LMarker, MapAddressItem},
  setup(props) {
    const { map } = toRefs(props)
    const { currentPosition } = useLocation()
    const { distanceToCurrentPosition } = useMapDistance()
    const { setMapBoundGroup } = useMapBounds(map)
    const { selectedAddress } = useAddresses()
    const { showCenterMapBtn } = useUI()

    const formattedCurrentPosition = computed(() => {
      const hasCoords = !!currentPosition.value?.lat && !!currentPosition.value?.lng
      return {
        ...currentPosition.value,
        coords: hasCoords ? [currentPosition.value.lat, currentPosition.value.lng] : [],
        hasCoords,
        // distance: distanceToCurrentPosition(currentPosition.value),
        icon: L.icon({ iconUrl: 'seller_pin2.png', iconSize: [50, 50], iconAnchor: [25, 50] })
      }
    })
    const formattedSelectedAddress = computed(() => {
      const hasCoords = !!selectedAddress.value?.lat && !!selectedAddress.value?.lng
      return {
        ...selectedAddress.value,
        coords: hasCoords ? [selectedAddress.value?.lat, selectedAddress.value?.lng] : [],
        hasCoords,
      }
    })


    const formattedCurrentPositionGroup = computed(() => [formattedCurrentPosition.value, formattedSelectedAddress.value])
    const { drawCurve } = useMapCurve(map, formattedCurrentPositionGroup)

    onMounted(() => setMapBoundGroup('currentPosition', formattedCurrentPositionGroup))
    watch([formattedCurrentPosition, formattedSelectedAddress], () => {
      drawCurve()
      setMapBoundGroup('currentPosition', formattedCurrentPositionGroup)
    })
    watch(selectedAddress, () => showCenterMapBtn.value = true)

    return {
      selectedAddress,
      formattedSelectedAddress,
      formattedCurrentPosition,
    }
  },
}
</script>
