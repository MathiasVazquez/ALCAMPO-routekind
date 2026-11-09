<template>
  <l-circle-marker
    v-for="(address, index) in addresses"
    :key="index"
    :lat-lng="[address.lat || 0, address.lng || 0]"
    :fillOpacity="0"
  >
    <l-tooltip :options="{ permanent: true, direction: 'top' }">
      <q-item class="rounded-tooltip-item column flex-center">
        <q-icon size="28px" name="priority_high" />
        <q-badge rounded floating color="primary" style="margin-top: -5px">
          <strong>Visitar</strong>
          <!-- <div class="q-ml-xs">
            {{ mobile.coordsDate ? moment(mobile.coordsDate).fromNow() : "" }}
          </div> -->
        </q-badge>
      </q-item>
    </l-tooltip>
  </l-circle-marker>
</template>

<script>
import leaflet from "leaflet"
import { LTooltip, LCircleMarker } from "@vue-leaflet/vue-leaflet"
import { computed } from "vue"

import moment from "moment"
import "moment/locale/es"
import { useAddresses } from "src/context"
moment.locale("es")

export default {
  components: { LCircleMarker, LTooltip },
  props: ["map"],
  setup() {
    const { addresses } = useAddresses()

    return {
      moment,
      addresses: computed(() =>
        addresses.value.filter((a) => a.task && !a.hasVisit.value)
      ),
    }
  },
}
</script>

<style scoped>
.rounded-tooltip-item {
  background-color: white;
  border-radius: 200px;
  min-width: 40px;
  width: 40px;
  height: 40px;
  max-height: 40px;
  min-height: 40px;
  max-height: 40px;
  min-height: 40px;
  display: flex;
  align-content: center;
  align-items: center;
  box-shadow: 0 0 10px 5px #0005;
  font-size: 12px;
}
</style>
