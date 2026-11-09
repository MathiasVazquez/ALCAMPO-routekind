<template>
  <div v-if="showPolygonEditor && hasVertices">

    <!-- EDIT VERTICES -->
    <div v-if="selectedPolygonEditorOption==='edit'">
      <l-marker draggable v-for="pin of selectedPolygonPins" :key="pin.id"
        :lat-lng="[pin.lat, pin.lng]" @update:lat-lng="onPinUpdated($event, pin)"
      >
        <l-icon :icon-size="[18, 18]" :icon-anchor="[9, 9]" icon-url="poly_vertex_pin1.png"/>
      </l-marker>
    </div>

    <!-- MIDDLE POINTS -->
    <div v-else-if="hasMinVertices && selectedPolygonEditorOption==='add'">
      <l-marker draggable v-for="mid of selectedPoygonMidPoints" :key="mid.id"
        :lat-lng="[mid.lat, mid.lng]" @update:lat-lng="onPinAdded($event, mid)"
      >
        <l-icon :icon-size="[18, 18]" :icon-anchor="[9, 9]" icon-url="agregator_pin1.png"/>
      </l-marker>
    </div>

    <!-- DELETE VERTICES -->
    <div v-else-if="selectedPolygonEditorOption==='delete'">
      <l-marker v-for="pin of selectedPolygonPins" :key="pin.id"
        :lat-lng="[pin.lat, pin.lng]" @click="onPinDelete($event, pin)"
      >
        <l-icon :icon-size="[18, 18]" :icon-anchor="[9, 9]" icon-url="poly_vertex_pin1.png"/>
      </l-marker>
    </div>
  </div>

  <!-- FLAT VERTICES -->
  <div v-if="(!showPolygonEditor || (hasMinVertices && selectedPolygonEditorOption==='add')) && hasVertices">
    <l-circle-marker v-for="pin of selectedPolygonPins" :key="pin.id" :lat-lng="[pin.lat, pin.lng]"
      :radius="5" :fill="true" :color="selectedPolygon.color" :fillColor="selectedPolygon.color"
      :opacity="1" :fillOpacity="1"
    />
  </div>

  <!-- POLYGON JSON -->
  <l-geo-json
    v-if="!updatingGeojson"
    :geojson="polygonPins"
    :options="geojsonOptions"
    :options-style="geojsonStyles"
  />
</template>

<script>
import { toRefs, ref, computed, watch, nextTick, onMounted } from 'vue'
import { usePolygonPins, usePolygons, useZones, useSettings, usePlanning } from 'src/context'
import { LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon} from "@vue-leaflet/vue-leaflet"
import { useMapBounds } from 'src/helpers'

export default {
  components: {LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon},
  props: ['map'],
  setup(props) {
    const { map } = toRefs(props)
    const { setMapBoundGroup } = useMapBounds(map)

    const processing = ref(false)

    const { addPolygonPin, updatePolygonPin, deletePolygonPin } = usePolygonPins()
    const { selectedZonePolygonsJson, selectZone, selectedZone, getRouteById } = useZones()
    const { selectedPlanningPolygonsJson } = usePlanning()
    const { polygonVisualization, addressesVisualization, selectedZoneListMainTab } = useSettings()
    const showCustomers = computed(() => addressesVisualization.value !== 'none')

    const {
      updatePolygon,
      selectPolygon,
      getPolygonById,
      getPolygonJson,
      selectedPolygon,
      showPolygonEditor,
      selectedPolygonEditorOption
    } = usePolygons()

    const selectedPolygonPins = computed(() => selectedPolygon.value?.polygonPins.value || [])
    const hasMinVertices = computed(() => selectedPolygonPins.value.length >= 3)
    const hasVertices = computed(() => selectedPolygonPins.value.length > 0)
    const selectedPolygonJson = computed(() => getPolygonJson(selectedPolygon.value))
    const selectedPoygonMidPoints = computed(() => {
      const midPoints = []
      const vertices = selectedPolygonPins.value.map(p => { return { id: p.id, lat: p.lat, lng: p.lng } })
      const addMidPoint = (next, prev) => {
        midPoints.push({
          id: `${prev}->${next}`,
          lat: (vertices[next].lat + vertices[prev].lat) / 2.0,
          lng: (vertices[next].lng + vertices[prev].lng) / 2.0,
          prevId: vertices[prev].id
        })
      }
      for (let i = 1; i < vertices.length; i++) addMidPoint(i, i - 1)
      if (vertices.length > 2) addMidPoint(0, vertices.length - 1)

      return midPoints
    })

    const updatingGeojson = ref(false)
    const geojsonOptions = computed(() => {
      return {
        onEachFeature: (feature, layer) => {
          // feature.properties.code
          layer.setStyle({
            color: feature.properties.color || '#223366',
            fillColor: feature.properties.color || '#223366',
            fillOpacity: feature.properties?.id === selectedPolygon.value?.id ? 0.45 : 0.1,
          })
          /*layer.bindTooltip(
            `<div style="margin:10px">${feature.properties.name || `Figura ${feature.properties.id}`}</div>`,
            { permanent: false, sticky: true }
          )*/
          layer.on('click', e => {
            if (showPolygonEditor.value) return

            const doSelection = () => {
              selectPolygon(getPolygonById(feature.properties.id))
              if (selectedZone.value?.id !== feature.properties.zone)
                selectZone(getRouteById(feature.properties.zone))
            }

            if (selectedZoneListMainTab.value !== "zones") {
              selectedZoneListMainTab.value = "zones"
              setTimeout(doSelection, 1)
            }
            else doSelection()


            // setTimeout(() => selectPolygon(getPolygonById(feature.properties.id)), 1)
          })
          /*layer.bindPopup(`<div>${feature.properties.name || `Figura ${feature.properties.id}`}</div>`)*/
        }
      }
    })
    const geojsonStyles = computed(() => {
      return {
        weight: 2,
        color: "#ECEFF1",
        opacity: 1,
        fillColor: "#FF0000",
        fillOpacity: 1
      }
    })

    const polygonPins = computed(() =>
      polygonVisualization.value === 'zone' ? selectedZonePolygonsJson.value :
      polygonVisualization.value === 'figure' ? selectedPolygonJson.value :
      polygonVisualization.value === 'all' ? selectedPlanningPolygonsJson.value : [])

    const jsonVertices = computed(() => polygonPins.value?.features?.reduce((result, feature) => [...result, ...feature.geometry.coordinates[0]], []) || [])
    onMounted(() => setMapBoundGroup('figures', jsonVertices))
    watch(jsonVertices, () => setMapBoundGroup('figures', jsonVertices))

    /*watch(selectedPolygonJson, async () => {
      updatingGeojson.value = true
      await nextTick()
      updatingGeojson.value = false
    })*/

    const onClickMap = async e => {
      if (!e.latlng) return
      const len = selectedPolygonPins.value.length
      if (!hasMinVertices.value && showPolygonEditor.value && selectedPolygonEditorOption.value==='add' && e.latlng) {
        await addPolygonPin({
          lat: e.latlng.lat,
          lng: e.latlng.lng,
          prev: len > 0 ? selectedPolygonPins.value[len - 1].id : null,
          polygon: selectedPolygon.value.id
        })
      }
    }

    const onPinUpdated =  async (e, pin) => {
      if (processing.value || !showPolygonEditor.value) return
      processing.value = true
      await updatePolygonPin({ id: pin.id, lat: e.lat, lng: e.lng })
      setTimeout(() => processing.value = false, 100)
    }
    const onPinAdded = async (e, point) => {
      if (processing.value || !showPolygonEditor.value) return
      processing.value = true
      await addPolygonPin({ lat: e.lat, lng: e.lng, prev: point.prevId, polygon: selectedPolygon.value.id })
      setTimeout(() => processing.value = false, 100)
    }
    const onPinDelete = async (e, pin) => {
      if (processing.value || !showPolygonEditor.value) return
      processing.value = true
      await deletePolygonPin(pin)
      setTimeout(() => processing.value = false, 100)
    }

    onMounted(() => {
      map.value._events.click.push({ ctx: false, fn: onClickMap })
    })

    return {
      polygonPins,
      updatePolygon,
      selectedPolygon,
      selectedPolygonPins,

      geojsonStyles,
      geojsonOptions,
      updatingGeojson,
      selectedPolygonJson,

      onClickMap,
      onPinUpdated,

      onPinAdded,
      onPinDelete,
      hasVertices,
      showCustomers,
      hasMinVertices,
      showPolygonEditor,
      polygonVisualization,
      selectedPoygonMidPoints,
      selectedZonePolygonsJson,
      selectedPolygonEditorOption,
      selectedPlanningPolygonsJson,
    }
  },
}
</script>
