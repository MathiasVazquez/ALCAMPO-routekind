<template>
  <l-circle-marker
    v-if="formattedAddress.hasCoords && !hideAddress"
    :lat-lng="formattedAddress.coords"
    :radius="6"
    :color="markerColor"
    :fillColor="markerColor"
    :fill="true"
    :fillOpacity="0.5"
  >
    <!-- @click="$emit('click', { e: $event, address })" -->
    <l-tooltip
      :options="{ interactive: false, permanent: permanentTooltip }"
      style="z-index: 9999; min-width: 150px"
    >
      <q-item
        class="row items-center no-wrap q-pa-none bg-white rounded-borders overflow-hidden"
        clickable
        v-ripple
        @click="$emit('click', { e: $event, address })"
      >
        <div
          :style="markerBgColorStyle"
          class="absolute-left"
          style="width: 10px; height: 100%"
        ></div>
        <div class="column q-pa-xs q-ml-md">
          <div v-if="address.visitLater.value">Visitar más tarde</div>
          <div>
            <div
              v-if="formattedAddress.distance?.label"
              class="text-weight-light"
              :style="`font-size:22px;font-family:roboto;${markerColorStyle}`"
            >
              {{ formattedAddress.distance.label }}
            </div>
            <div class="text-caption">
              <strong>{{ formattedAddress.fullName }}</strong>
            </div>
            <div class="text-caption overflow-hidden" style="max-width: 40vw">
              {{ formattedAddress.description }}
            </div>
            <!--<div class="text-caption">({{formattedAddress.coords[0]}}, {{formattedAddress.coords[1]}})</div>-->
          </div>
        </div>
        <q-space />
        <q-avatar
          round
          :style="markerColorStyle"
          size="36px"
          class="q-mr-sm bg-grey-3"
          icon="near_me"
        />
      </q-item>
    </l-tooltip>
  </l-circle-marker>
</template>

<script>
import { computed, toRefs } from "vue"
import { LTooltip, LCircleMarker } from "@vue-leaflet/vue-leaflet"
import { useAddresses } from "src/context"
import { useMapDistance } from "src/helpers"
import { getCssVar } from "quasar"

export default {
  props: ["address", "permanentTooltip", "hideSelectedAddress"],
  emits: ["click"],
  components: { LTooltip, LCircleMarker },
  setup(props) {
    const { address } = toRefs(props)
    const { selectedAddress } = useAddresses()
    const { distanceToCurrentPosition } = useMapDistance()

    const markerColor = computed(() =>
      address.value.visitLater.value
        ? getCssVar("secondary")
        : getCssVar("primary")
    )

    const formattedAddress = computed(() => {
      const hasCoords = !!address.value.lat && !!address.value.lng
      return {
        ...address.value.customer,
        ...address.value,
        coords: hasCoords ? [address.value.lat, address.value.lng] : null,
        distance: hasCoords ? distanceToCurrentPosition(address.value) : null,
        hasCoords,
      }
    })

    const hideAddress = computed(
      () =>
        props.hideSelectedAddress &&
        address.value &&
        selectedAddress.value &&
        address.value.id === selectedAddress.value?.id
    )

    return {
      hideAddress,
      markerColor,
      formattedAddress,
      markerColorStyle: computed(() => `color:${markerColor.value};`),
      markerBgColorStyle: computed(
        () => `background-color:${markerColor.value};`
      ),
    }
  },
}
</script>

<style>
.leaflet-container {
  font: 12px !important;
}
</style>
