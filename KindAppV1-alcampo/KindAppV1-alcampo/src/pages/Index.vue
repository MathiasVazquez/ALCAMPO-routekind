<template>
  <q-page>
    <!-- TOGGLE LEFT DRAWER BUTTON -->
    <q-page-sticky position="top-left" style="z-index: 1000" :offset="[16, 16]">
      <q-btn
        round
        icon="menu"
        color="white"
        text-color="primary"
        @click="showLeftDrawer = !showLeftDrawer"
      />
    </q-page-sticky>

    <q-page-sticky
      position="top-right"
      style="z-index: 1000"
      :offset="[16, 16]"
    >
      <q-btn
        round
        :icon="fullMapVisualization ? 'unfold_less' : 'unfold_more'"
        class="rotate-45"
        :color="fullMapVisualization ? 'white' : 'primary'"
        :text-color="fullMapVisualization ? 'primary' : 'white'"
        @click="
          () => {
            canShowCenterMapButton = false
            fullMapVisualization = !fullMapVisualization
          }
        "
      />
    </q-page-sticky>

    <BaseMap />
    <BottomDrawer v-model="openBottomDrawer" :height="550" :minHeight="200">
      <template #header>
        <SelectedAddressItem :open="openBottomDrawer" />
      </template>
      <template #body>
        <AddressOrderList :address="selectedAddress" />
        <!--<q-item v-if="false">
          <q-item-section>
            <AddressOrderList title="Próximo pedido" :address="nextAddressOrders" />
          </q-item-section>
        </q-item>-->
      </template>
      <template #top>
        <div class="q-pa-sm row justify-between">
          <!-- LEFT OPTIONS -->
          <div class="row q-gutter-x-sm">
            <!-- OPEN IN GOOGLE MAPS -->
            <q-btn
              v-if="currentAddressHasCoords"
              dense
              rounded
              unelevated
              no-caps
              class="bg-white shadow-7 q-px-md text-grey-9"
              @click="openGoogleMaps"
            >
              <q-icon name="o_map" size="20px" />
              <div class="q-ml-xs">Abrir en Google Maps</div>
            </q-btn>
            <!-- ASSIGN ADDRESS COORDS -->
            <q-btn
              v-else
              dense
              rounded
              unelevated
              no-caps
              class="bg-primary text-white shadow-7 q-px-md"
              @click="() => {}"
            >
              <q-icon name="o_add_location_alt" size="20px" />
              <div class="q-ml-xs">Asignar coordenadas</div>
            </q-btn>
            <!-- MORE OPTIONS -->
            <q-btn
              dense
              rounded
              unelevated
              no-caps
              class="bg-white shadow-7 q-px-md text-grey-9"
              @click="handleSyncData"
            >
              <q-spinner-pie v-if="syncing" color="primary" size="1em" />
              <q-icon v-else name="sync" />
              <!-- <q-menu auto-close>
                <q-list>
                  <q-item clickable class="bg-white q-pa-md text-grey-9" @click="() => {}">
                    <q-icon name="o_edit_location" size="20px" />
                    <div class="q-ml-xs">Modificar coordenadas de la ubicación</div>
                  </q-item>
                  <q-item clickable class="bg-white q-pa-md text-grey-9" @click="() => {}">
                    <q-icon name="o_sync" size="20px" />
                    <div class="q-ml-xs">Sincronizar datos</div>
                  </q-item>
                </q-list>
              </q-menu> -->
            </q-btn>
          </div>
          <!-- UPDATE MAP BOUNDS -->
          <q-btn
            v-if="showCenterMapBtn"
            dense
            rounded
            unelevated
            no-caps
            class="bg-white shadow-7 q-px-md text-grey-9"
            @click="centerMap"
          >
            <q-icon name="gps_fixed" size="20px" />
          </q-btn>
        </div>
      </template>
    </BottomDrawer>
  </q-page>
</template>

<script>
import { ref } from "vue"
import {
  useSession,
  loadAllFromServer,
  useUI,
  useAddresses,
  useLocation,
  useSettings,
} from "src/context"
import { useMapHelpers } from "src/helpers"
import { useRouter } from "vue-router"
import BaseMap from "src/components/maps/BaseMap"
import BottomDrawer from "src/components/includes/BottomDrawer"
import SelectedAddressItem from "src/components/addresses/SelectedAddressItem"
import AddressOrderList from "src/components/orders/AddressOrderList"

export default {
  components: { BaseMap, BottomDrawer, SelectedAddressItem, AddressOrderList },
  setup() {
    const { forceUpdateMap } = useMapHelpers()
    const {
      centerMap,
      showCenterMapBtn,
      showLeftDrawer,
      canShowCenterMapButton,
    } = useUI()
    const { isLogged } = useSession()
    const { selectedAddress } = useAddresses()
    const { startWatchLocation } = useLocation()
    const { fullMapVisualization } = useSettings()
    const openBottomDrawer = ref(false)
    const syncing = ref(false)
    const router = useRouter()

    const currentAddressHasCoords = ref(true)
    const openGoogleMaps = () => {
      if (!selectedAddress.value) return
      window.open(
        encodeURI(
          `geo://?q=${selectedAddress.value?.lat},${selectedAddress.value?.lng}`
        ),
        "_system"
      )
    }
    const handleSyncData = async () => {
      if (syncing.value) return
      syncing.value = true
      forceUpdateMap()
      await loadAllFromServer()
      syncing.value = false
    }

    const onCreate = () => {
      if (isLogged.value) {
        startWatchLocation()
        loadAllFromServer()
      } else router.replace("/login")
    }
    onCreate()

    return {
      syncing,
      showLeftDrawer,
      selectedAddress,
      openBottomDrawer,
      showCenterMapBtn,
      fullMapVisualization,
      canShowCenterMapButton,
      currentAddressHasCoords,
      handleSyncData,
      openGoogleMaps,
      centerMap,
    }
  },
}
</script>
