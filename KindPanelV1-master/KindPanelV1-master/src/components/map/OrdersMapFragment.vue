<template>
  <div v-for="(ordersGroup, orderId) of (showOrders ? ordersGroupByMobileWithUnassigned : [])" :key="orderId"
    class="order-map-fragment"
  >
    <!-- PATHS -->
    <l-polyline :lat-lngs="getPolylineCoords(ordersGroup)" :color="primaryColor"></l-polyline>
    <!-- CIRCLES -->
    <l-circle-marker
      v-for="(address, index) of getOrdersAddress(ordersGroup)" :key="address.order.id"
      :lat-lng="[address.lat || 0, address.lng || 0]"
      :radius="7" :color="primaryColor"
      :fill="address.order && selectedOrder?.id !== address.order.id" :fillColor="primaryColor" :fillOpacity="1"
      @click="handleClickOrder(address.order)"
    >
      <div class="leaflet-tooltip-round">
      <l-tooltip :options="{permanent: true}" >
        <q-item clickable class="q-pa-md rounded-tooltip flex flex-center text-primary"
          :class="selectedOrder?.id === address.order.id ? 'bg-primary text-white' : ''"
          :style="selectedOrder?.id === address.order.id ? `border:2px solid ${primaryColor}` : `border:2px solid white`"
          @click="handleClickOrder(address.order)"
        >
          <strong>{{index + 1}}</strong>
          <q-badge color="transparent" floating rounded style="margin-top:-5px">
              <q-badge rounded :color="!address.order.mobile && !address.order.autoAssignedToMobile ? 'red' : address.order.hasSorted ? 'green' : 'orange'">
                {{getMobileById(address.order.mobile || address.order.autoAssignedToMobile)?.name || 'Ninguno'}}
              </q-badge>
              <q-badge v-if="address.order.hasDelivered.value" rounded color="green">
                <q-icon name="done_all" color="white" size="14px" />
              </q-badge>
          </q-badge>
          <!-- <q-badge floating rounded v-if="address.order.hasVisit.value" style="margin-top:-22px"
            :color="address.order.hasDelivered.value ? 'green' : address.order.visitLater.value ? 'purple' : 'red'"
          >
            {{address.order.hasDelivered.value ? 'Entregado' : address.order.visitLater.value ? 'Volver más tarde' : 'No entregado'}}
          </q-badge> -->
        </q-item>
      </l-tooltip>
      </div>
    </l-circle-marker>
  </div>
</template>

<script>
import leaflet from "leaflet"
import { colors } from 'quasar'
import { toRefs, ref, computed, watch, nextTick, onMounted } from 'vue'
import { usePolygonPins, usePolygons, useZones, useCustomerAddresses, useSettings, usePlanning, useOrders, useMobiles } from 'src/context'
import { LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon} from "@vue-leaflet/vue-leaflet"
import { useMapBounds } from 'src/helpers'

export default {
  components: {LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon},
  props: ['map'],
  setup(props) {
    const { map } = toRefs(props)
    const { setMapBoundGroup } = useMapBounds(map)
    const { orders, getOrderById, selectOrder, selectedOrder, ordersGroupByMobileWithUnassigned } = useOrders()
    const { getCustomerAddressById } = useCustomerAddresses()
    const { orderVisualization, selectedZoneListMainTab } = useSettings()
    const { getMobileById } = useMobiles()
    const { selectZone } = useZones()

    const showOrders = computed(() => orderVisualization.value === 'all')
    const primaryColor = computed(() => colors.getPaletteColor('primary'))
    const handleClickOrder = async order => {
      if (selectedZoneListMainTab.value !== 'orders') {
        selectZone(null)
        selectedZoneListMainTab.value = 'orders'
        await nextTick()
      }
      selectOrder(order)
    }

    const getOrdersAddress = orders => orders.map(order => {
      const customerAddress = order.customerAddress
      return customerAddress ? { ...customerAddress, order } : null
    }).filter(o => o)

    const ordersAddressToBound = computed(() => showOrders.value ?  getOrdersAddress(orders.value): [])
    onMounted(() => setMapBoundGroup('orders', ordersAddressToBound))
    watch(ordersAddressToBound, () => setMapBoundGroup('orders', ordersAddressToBound))

    const getPolylineCoords = orders => getOrdersAddress(orders).filter(a => a.order.hasSorted && a.lat && a.lng)

    return {
      showOrders,
      primaryColor,
      selectedOrder,
      ordersGroupByMobileWithUnassigned,
      getPolylineCoords,
      getOrdersAddress,
      handleClickOrder,
      getMobileById,
    }
  },
}
</script>

<style scoped>
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
