<template>
  <div style="width: 100%">
    <l-map
      v-if="!forceReloadMap"
      ref="map"
      style="height: 100vh"
      :maxZoom="19"
      :zoomAnimation="true"
      :fadeAnimation="true"
      :markerZoomAnimation="true"
      :useGlobalLeaflet="true"
      :options="mapOptions"
      @click="handleMapClick"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        :attribution="attribution"
      />

      <!-- REFRESH MAP -->
      <l-control v-if="false">
        <q-btn
          flat
          rounded
          no-caps
          class="text-white text-caption"
          @click="centerMap"
        >
          <strong>¿Problemas visualizando el mapa?</strong>
          <q-tooltip><strong>Click para refrescar</strong></q-tooltip>
        </q-btn>
      </l-control>

      <!-- MAP EXTRAS -->
      <slot name="map" />

      <!-- MAP FRAGMENTS -->
      <AddressesMapFragment :map="mapObject" />
      <EditModeMapFragment :map="mapObject" />
      <OrdersMapFragment :map="mapObject" />
      <EventsMapFragment :map="mapObject" />
      <MobileMapFragment :map="mapObject" />
    </l-map>
  </div>
</template>

<script>
import leaflet from "leaflet";
import "leaflet/dist/leaflet.css";
import {
  LPopup,
  LTooltip,
  LPolyline,
  LMap,
  LTileLayer,
  LMarker,
  LGeoJson,
  LControl,
  LCircleMarker,
} from "@vue-leaflet/vue-leaflet";
import { ref, toRefs, computed, watch, nextTick } from "vue";
import { useMapHelpers, useMapBounds } from "src/helpers";
import { useUI } from "src/context";
import AddressesMapFragment from "./AddressesMapFragment";
import EditModeMapFragment from "./EditModeMapFragment";
import OrdersMapFragment from "./OrdersMapFragment";
import EventsMapFragment from "./EventsMapFragment";
import MobileMapFragment from "./MobileMapFragment";

export default {
  name: "FullRouteMap",
  components: {
    AddressesMapFragment,
    MobileMapFragment,
    EditModeMapFragment,
    EventsMapFragment,
    OrdersMapFragment,
    LPopup,
    LTooltip,
    LPolyline,
    LMap,
    LTileLayer,
    LMarker,
    LGeoJson,
    LControl,
    LCircleMarker,
  },
  props: ["padding"],
  emit: ["click:map"],
  setup(props, { emit }) {
    const { padding } = toRefs(props);
    const { attribution, url, mapOptions } = useMapHelpers();
    const { updatingMap, centerMap, forceReloadMap, centerMapCoords } = useUI();

    const map = ref(null);
    const mapObject = computed(() => (map.value || {}).leafletObject);
    const mapIsReady = computed(() => !!(mapObject.value || {}).fitBounds);

    // Map events
    const handleMapClick = (e) => e.latlng && emit("click:map", e);

    // Set initial padding and first update
    const { updateBounds, setMapPadding, centerMapTo } =
      useMapBounds(mapObject);
    watch(mapIsReady, async () => {
      if (!mapIsReady.value) return;
      setMapPadding(padding);
      await nextTick();
      updateBounds();
      await new Promise((resolve) => setTimeout(resolve, 1500));
      updateBounds();
    });
    watch(centerMapCoords, () => {
      if (centerMapCoords.value) {
        centerMapTo(centerMapCoords.value);
      }
    });

    return {
      url,
      map,
      mapObject,
      mapOptions,
      attribution,
      updatingMap,
      forceReloadMap,
      handleMapClick,
      centerMap,
    };
  },
};
</script>

<style scoped>
.header-container {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000;
}
.footer-container {
  position: absolute;
  top: 100vh;
  transform: translateY(-100%);
  left: 0;
  z-index: 1000;
}
</style>
