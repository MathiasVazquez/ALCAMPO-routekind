<template>
  <q-page class="row" style="overflow: hidden">
    <!-- ROUTES -->

    <q-list
      class="main-container scroll"
      :class="{ 'main-container-hidden': !showZoneList || showPolygonEditor }"
    >
      <!-- MULTIPLE MOBILES SELECTOR -->
      <q-item class="basic-item bordered">
        <!--<MobileSelector />-->
        <div class="full-width">
          <MultipleMobileSelector />
        </div>
      </q-item>

      <!-- TABS -->
      <q-item class="column basic-item bordered" style="padding: 0">
        <q-tabs
          v-model="selectedZoneListMainTab"
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab name="zones" label="Zonas" />
          <q-tab name="orders" label="Pedidos" />
          <q-tab name="events" label="Eventos" />
        </q-tabs>

        <q-separator />

        <q-tab-panels v-model="selectedZoneListMainTab" animated>
          <q-tab-panel name="zones" class="q-pa-none q-ma-none">
            <ZoneList />
          </q-tab-panel>

          <q-tab-panel name="orders" class="q-pa-none q-ma-none">
            <OrderList />
          </q-tab-panel>

          <q-tab-panel name="events" class="q-pa-none q-ma-none">
            <EventList />
          </q-tab-panel>
        </q-tab-panels>
      </q-item>
    </q-list>

    <!-- SESSION OPTIONS -->

    <q-list class="session-options-container scroll">
      <q-item class="basic-item bordered bg-transparent" style="padding: 0">
        <div class="full-width">
          <SessionOptions />
        </div>
      </q-item>
    </q-list>

    <!-- ROUTE DETAILS -->

    <q-list
      class="main-container scroll"
      :class="[
        { 'details-container-hidden': !showDetails },
        { 'details-container-displaced-left': showPolygonEditor },
      ]"
      style="left: 385px"
    >
      <q-item class="basic-item bordered" style="padding: 0">
        <div class="full-width">
          <ZoneDetails v-if="showZoneDetails" />
          <OrderSettings v-else-if="showOrderSettings" />
        </div>
      </q-item>
      <q-item
        v-if="showOrderSettings"
        class="basic-item bordered"
        style="padding: 0"
      >
        <div class="full-width"><OrderDetails /></div>
      </q-item>
    </q-list>

    <!-- POLYGON EDITOR -->

    <q-list
      class="main-container scroll"
      :class="{ 'editor-container-hidden': !showPolygonEditor }"
      style="left: 385px; width: 270px"
    >
      <q-item class="basic-item" style="padding: 0">
        <div class="full-width">
          <PolygonEditTools />
        </div>
      </q-item>
    </q-list>

    <!-- MAP -->

    <div class="flex" style="flex-grow: 1">
      <BaseMap />
    </div>
  </q-page>
</template>

<script>
import { defineComponent, ref, watch, computed } from "vue"
import {
  useZones,
  useCustomerAddresses,
  usePolygons,
  useSettings,
  useOrders,
} from "src/context"
import BaseMap from "src/components/map/BaseMap"
import CustomerList from "src/components/customer/CustomerList"
import ZoneList from "src/components/zone/ZoneList"
import ZoneDetails from "src/components/zone/ZoneDetails"
import MobileList from "src/components/mobile/MobileList"
import MobileSelector from "src/components/mobile/MobileSelector"
import MultipleMobileSelector from "src/components/mobile/MultipleMobileSelector"
import PolygonEditTools from "src/components/polygon/PolygonEditTools"
import SessionOptions from "src/components/security/SessionOptions"
import OrderList from "src/components/orders/OrderList"
import OrderSettings from "src/components/orders/OrderSettings"
import OrderDetails from "src/components/orders/OrderDetails"
import EventList from "src/components/events/EventList"

export default defineComponent({
  name: "PageIndex",
  components: {
    BaseMap,
    EventList,
    CustomerList,
    OrderList,
    OrderDetails,
    OrderSettings,
    ZoneList,
    MobileList,
    MobileSelector,
    MultipleMobileSelector,
    ZoneDetails,
    PolygonEditTools,
    SessionOptions,
  },
  setup() {
    const {
      showSelectedZonePolygonDetails,
      selectedZoneDirections,
      selectedZone,
      selectZone,
    } = useZones()
    const { selectedOrder, selectOrder } = useOrders()
    const { showPolygonEditor, selectPolygon } = usePolygons()
    const { selectedZoneListMainTab, viewScope } = useSettings()

    const showZoneList = computed(() => true)

    watch(selectedZoneListMainTab, () => {
      selectZone(null)
      selectOrder(null)
      // Set view scope
      viewScope.value = selectedZoneListMainTab.value
    })
    const showZoneDetails = computed(() => !!selectedZone.value)
    const showOrderSettings = computed(() => !!selectedOrder.value)
    const showDetails = computed(
      () => showZoneDetails.value || showOrderSettings.value
    )

    // Close editor on close zone details
    watch(showZoneDetails, () => {
      if (showZoneDetails.value) return
      showPolygonEditor.value = false
      selectPolygon(null)
    })

    return {
      showDetails,
      showZoneList,
      selectedOrder,
      showZoneDetails,
      showOrderSettings,
      showPolygonEditor,
      selectedZoneDirections,
      selectedZoneListMainTab,
      showSelectedZonePolygonDetails,
    }
  },
})
</script>

<style scoped>
.main-container {
  top: 0;
  left: 60px;
  width: 340px;
  z-index: 500;
  max-height: 100vh;
  position: absolute;
  transition: all 0.3s;
  transition-property: top, left;
}
.session-options-container {
  top: 0;
  right: 0;
  width: 340px;
  z-index: 500;
  max-height: 100vh;
  position: absolute;
  transition: all 0.3s;
  transition-property: top, left;
}
.bordered {
  border: 1px solid #ddd;
}
.main-container-hidden {
  left: -400px !important;
}
.details-container-hidden {
  top: 120vh !important;
}
.details-container-displaced-left {
  left: 60px !important;
}
.editor-container-hidden {
  top: -100% !important;
}
.main-container::-webkit-scrollbar {
  display: none;
}
</style>
