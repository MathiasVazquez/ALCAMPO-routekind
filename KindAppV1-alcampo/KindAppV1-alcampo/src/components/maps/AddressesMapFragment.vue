<template>
  <!-- ADDRESESS MARKS -->
  <l-layer-group>
    <!--
      <marker-cluster :options="{ showCoverageOnHover: false, chunkedLoading: true }">
      </marker-cluster>
    -->
    <MapAddressItem v-for="address of addresses" :key="address.id" :address="address"
      :hideSelectedAddress="hideSelectedAddress" @click="handleAddressClick"
    />
  </l-layer-group>
</template>

<script>
import leaflet from "leaflet"
import 'leaflet/dist/leaflet.css';
import { computed, watch, toRefs, onMounted, nextTick } from 'vue'
import { useAddresses, useSettings, useUI } from 'src/context';
import { LLayerGroup} from "@vue-leaflet/vue-leaflet"
import { useMapBounds } from 'src/helpers'
import MarkerCluster from "./MarkerCluster.vue"
import MapAddressItem from "./MapAddressItem.vue"

export default {
  components: {LLayerGroup, MarkerCluster, MapAddressItem},
  props: ['map', 'hideSelectedAddress'],
  setup(props) {
    const { map } = toRefs(props)
    const { addresses, selectAddress } = useAddresses()
    const { fullMapVisualization } = useSettings()
    const { setMapBoundGroup } = useMapBounds(map)
    const { centerMap } = useUI()

    const visibleAddresses = computed(() => addresses.value.filter(a => a.showInMap?.value))
    const addressesToBound = computed(() => fullMapVisualization.value ? visibleAddresses.value : [])

    onMounted(() => setMapBoundGroup('addresses', addressesToBound))
    watch(addressesToBound, () => setMapBoundGroup('addresses', addressesToBound))
    watch(fullMapVisualization, centerMap)

    const handleAddressClick = ({ address }) => selectAddress(address)

    return {
      addresses: visibleAddresses,
      handleAddressClick,
    }
  },
}
</script>
