import leaflet from "leaflet";
import { ref, computed } from "vue";
import { useLocation, useMap, useUI } from "src/context";

//
// DEFAULT MAP SETTINGS
//

const attribution = ref(
  '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
);
const url = ref("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
const mapOptions = ref({ zoomSnap: 0.2, zoomControl: false, maxZoom: 40 });

export const useMapHelpers = () => {
  return {
    attribution: computed(() => attribution.value),
    url: computed(() => url.value),
    mapOptions: computed(() => mapOptions.value),
  };
};

//
// BOUNDS
//

const mapsBoundGroups = ref({ empty: [] });
const mapsPadding = ref({});
const defaultCoords = ref([
  { lat: "-25.255892", lng: "-57.725735" },
  { lat: "-25.368553", lng: "-57.456055" },
]);

export const useMapBounds = (map) => {
  const mapId = computed(() => map.value?._leaflet_id || -1);

  const padding = computed(
    () => mapsPadding.value[mapId.value] || [5, 5, 25, 5]
  );
  const listToBound = computed(() => {
    const result = Object.values(mapsBoundGroups.value[mapId.value]).reduce(
      (result, group) => [...result, ...(group || [])],
      []
    );
    return result.length === 0 ? defaultCoords.value : result;
  });

  const bounds = computed(() => {
    let firstSelected = false;
    let maxLat = 0.0,
      maxLng = 0.0,
      minLat = 0.0,
      minLng = 0.0;
    for (let elem of listToBound.value) {
      if (
        !elem ||
        !(elem.lat || elem[1]) ||
        !(elem.lng || elem[0]) ||
        elem.lat === "null" ||
        elem.lng === "null"
      )
        continue;
      const lat = parseFloat(elem.lat || elem[1]);
      const lng = parseFloat(elem.lng || elem[0]);
      if (lat > maxLat || !firstSelected) maxLat = lat;
      if (lat < minLat || !firstSelected) minLat = lat;
      if (lng > maxLng || !firstSelected) maxLng = lng;
      if (lng < minLng || !firstSelected) minLng = lng;
      firstSelected = true;
    }
    const mult = 0.02 * 0.1;
    const [p1, p2, p3, p4] = Array.isArray(padding.value)
      ? [
          padding.value[0] * mult,
          padding.value[1] * mult,
          padding.value[2] * mult,
          padding.value[3] * mult,
        ]
      : [
          padding.value * mult,
          padding.value * mult,
          padding.value * mult,
          padding.value * mult,
        ];

    return [
      [maxLat + p1, maxLng + p2],
      [minLat - p3, minLng - p4],
    ];
  });

  const setMapBoundGroup = (groupName, groupValue) => {
    if (!mapsBoundGroups.value[mapId.value])
      mapsBoundGroups.value[mapId.value] = {};
    mapsBoundGroups.value[mapId.value][groupName] = groupValue;
    mapsBoundGroups.value = { ...mapsBoundGroups.value };
  };

  const setMapPadding = (padding) => {
    if (!mapsPadding.value[mapId.value]) mapsPadding.value[mapId.value] = [];
    mapsPadding.value[mapId.value] = padding;
    mapsPadding.value = { ...mapsPadding.value };
  };

  function centerMapTo(coords) {
    if (!coords || !coords.lat || !coords.lng) return;
    console.log("# coords:", coords);
    map.value?.flyTo([coords.lat, coords.lng], coords.zoom, { duration: 1 });
  }

  return {
    centerMapTo,
    setMapPadding,
    setMapBoundGroup,
    updateBounds: () => map.value.fitBounds(bounds.value),
  };
};
