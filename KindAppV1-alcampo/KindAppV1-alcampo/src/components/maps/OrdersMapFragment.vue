<template>
  <l-circle-marker
    v-for="(address, index) of orderAddresses" :key="address.id"
    :lat-lng="[address.lat || 0, address.lng || 0]"
    :radius="7" :color="primaryColor"
    :fill="address.order && selectedOrder?.id !== address.order.id" :fillColor="primaryColor" :fillOpacity="1"
    @click="handleClickOrder(address)"
  >
    <div class="leaflet-tooltip-round">
    <l-tooltip :options="{permanent: true}" >
      <q-item clickable class="q-pa-md rounded-tooltip flex flex-center text-primary"
        :class="selectedOrder?.id === address.order.id ? 'bg-primary text-white' : ''"
        :style="selectedOrder?.id === address.order.id ? `border:2px solid ${primaryColor}` : `border:2px solid white`"
        @click="handleClickOrder(address)"
      >
        <strong>{{index + 1}}</strong>
        <q-badge :color="address.order.hasDelivered.value ? 'green' : 'red'" floating rounded>
          <div>{{address.order.hasDelivered.value ? 'Entregado' : 'Pendiente'}}</div>
          <q-icon class="q-ml-sm" v-if="address.order.hasDelivered.value" name="done_all"></q-icon>
        </q-badge>
      </q-item>
    </l-tooltip>
    </div>
  </l-circle-marker>
  <!-- PATH -->
  <l-polyline :lat-lngs="orderAddresses.filter(a => a.order.hasSorted && a.lat && a.lng)" color="#656565"></l-polyline>
</template>


<script>
import leaflet from "leaflet"
import { colors } from 'quasar'
import { toRefs, ref, computed, watch, nextTick, onMounted } from 'vue'
import { useAddresses, useOrders } from 'src/context'
import { LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon} from "@vue-leaflet/vue-leaflet"
import { useMapBounds } from 'src/helpers'

export default {
  components: {LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon},
  props: ['map'],
  setup(props) {
    const { getOrderById, sortedOrders } = useOrders()
    const { selectedAddress, selectAddress, getAddressById } = useAddresses()

    const primaryColor = computed(() => colors.getPaletteColor('primary'))

    const orderAddresses = computed(() => sortedOrders.value.map(order => { return { ...order.customerAddress, order } }))
    const selectedOrder = computed(() => orderAddresses.value.find(a => a.id === selectedAddress.value?.id)?.order)
    const selectOrder = order => selectAddress(orderAddresses.value.find(a => a.order.id === order.id))

    const handleClickOrder = address => selectOrder(getOrderById(address.order.id))

    return {
      primaryColor,
      selectedOrder,
      orderAddresses,
      handleClickOrder,
    }
  },
}
</script>

<style>
.leaflet-tooltip {
  padding: 0 !important;
  border: 0 !important;
  background-color: transparent;
  box-shadow: none !important;
  pointer-events: auto !important;
}
.rounded-tooltip {
  background-color: white;
  border-radius: 200px;
  width: 50px;
  height: 50px;
  display: flex;
  align-content: center;
  align-items: center;
  box-shadow: 0 0 10px 5px #0005;
  font-size: 18px;
}
</style>
