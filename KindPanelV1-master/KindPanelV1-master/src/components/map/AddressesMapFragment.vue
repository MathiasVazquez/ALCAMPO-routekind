<template>
  <!-- ADDRESESS MARKS -->
  <l-layer-group :visible="showAddresses">
    <marker-cluster :options="{ showCoverageOnHover: false, chunkedLoading: true }">
      <l-circle-marker v-for="address of addresses" :key="address.id"
        :lat-lng="address.coords" :radius="6" :fill="true"
        :color="markerColor" :fillColor="markerColor"
      >
        <l-tooltip :options="{interactive: false}" style="z-index:9999">
          <q-item class="row no-wrap q-pa-none bg-white rounded-borders overflow-hidden" clickable v-ripple>
            <div class="bg-primary" style="width:10px"></div>
            <div class="column q-pa-xs">
              <div class="q-py-sm q-gutter-y-xs">
                <div class="text-caption text-grey-7">{{address.customer.document}}</div>
                <div class="text-caption"><strong>{{address.customer.firstName}} {{address.customer.lastName}}</strong></div>
                <div class="text-caption">{{address.description}}</div>
                <div class="text-caption">({{address.coords[0]}}, {{address.coords[1]}})</div>
              </div>
            </div>
          </q-item>
        </l-tooltip>
      </l-circle-marker>
    </marker-cluster>
  </l-layer-group>
</template>

<script>
import leaflet from "leaflet"
import 'leaflet/dist/leaflet.css';
import { computed, watch, toRefs, onMounted, onBeforeUnmount } from 'vue'
import { useCustomerAddresses, useSettings, useZones } from 'src/context';
import { LTooltip, LCircleMarker, LLayerGroup} from "@vue-leaflet/vue-leaflet"
import { useMapBounds } from 'src/helpers'
import { getCssVar } from 'quasar'
import MarkerCluster from "./MarkerCluster.vue"

export default {
  components: {LTooltip, LCircleMarker, LLayerGroup, MarkerCluster},
  props: ['map'],
  setup(props) {
    const { map } = toRefs(props)
    const { customerAddresses } = useCustomerAddresses()
    const { setMapBoundGroup } = useMapBounds(map)
    const { addressesVisualization } = useSettings()
    const { selectedZoneAddresses } = useZones()

    const markerColor = computed(() => getCssVar('primary'))

    const showAddresses = computed(() => addressesVisualization.value !== 'none')
    // SCOPES: all, zone, figure, none
    const baseAddressList = computed(() => addressesVisualization.value === 'zone' ? selectedZoneAddresses.value : customerAddresses.value)

    const formatMark = d => { return { ...d.customer, ...d, coords: d.lat && d.lng ? [d.lat, d.lng] : null } }
		const addresses = computed(() => baseAddressList.value.map(d => formatMark(d)).filter(d => d.coords && d.coords[0] && d.coords[1]))

    const addressesToBound = computed(() => showAddresses.value ? addresses.value : [])

    onMounted(() => setMapBoundGroup('addresses', addressesToBound))
    watch(addressesToBound, () => setMapBoundGroup('addresses', addressesToBound))

    return {
      addresses,
      markerColor,
      showAddresses,
      addressesVisualization,
      markerColorStyle: computed(() => `color:${markerColor.value};`),
      markerBgColorStyle: computed(() => `background-color:${markerColor.value};`),
    }
  },
}
</script>
