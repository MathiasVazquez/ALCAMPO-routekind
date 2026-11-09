<template>
  <div v-for="(visitsGroup, visitId) of (showEvents ? visitsGroupByMobile : [])" :key="visitId" class="event-map-fragment">
    <!-- PATHS -->
    <l-polyline :lat-lngs="visitsGroup" :color="primaryColor"></l-polyline>
    <!-- CIRCLES -->
    <l-circle-marker
      v-for="(visit, index) of visitsGroup" :key="visit.id"
      :lat-lng="[visit.lat || 0, visit.lng || 0]"
      :radius="7" :color="primaryColor"
      :fill="selectedVisit?.id !== visit.id"
      :fillColor="primaryColor" :fillOpacity="1"
      @click="handleClickEvent(visit)"
    >
      <l-tooltip :options="{permanent: true}">
        <q-item clickable class="q-pa-none rounded-tooltip-item flex flex-center text-primary"
          :class="selectedVisit?.id === visit.id ? 'bg-primary text-white' : ''"
          :style="selectedVisit?.id === visit.id ? `border:2px solid ${primaryColor}` : `border:2px solid white`"
          @click="handleClickEvent(visit)"
        >
          <div class="row items-center no-wrap">
            <q-badge rounded color="primary" style="margin-left:1px">
              <strong>{{index + 1}}</strong>
            </q-badge>
            <strong class="q-px-sm">{{moment(visit.checkDate).fromNow()}}</strong>
          </div>
          <!-- <q-badge color="primary" floating rounded style="margin-top:-5px">
            {{visit.mobile.name}}
          </q-badge> -->
          <q-badge color="transparent" floating rounded style="margin-top:-8px">
              <q-badge rounded :color="selectedVisit?.id === visit.id ? 'white' : 'primary'"
                :class="selectedVisit?.id === visit.id ? 'text-primary' : 'text-white'"
              >
                <strong>{{visit.mobile.name}}</strong>
              </q-badge>
          </q-badge>
          <!-- <q-badge floating rounded v-if="address.order.hasVisit.value" style="margin-top:-22px"
            :color="address.order.hasDelivered.value ? 'green' : address.order.visitLater.value ? 'purple' : 'red'"
          >
            {{address.order.hasDelivered.value ? 'Entregado' : address.order.visitLater.value ? 'Volver más tarde' : 'No entregado'}}
          </q-badge> -->
        </q-item>
      </l-tooltip>
    </l-circle-marker>
  </div>
</template>

<script>
import leaflet from "leaflet"
import { colors } from 'quasar'
import { toRefs, ref, computed, watch, nextTick, onMounted } from 'vue'
import { useSettings, useMobiles, useVisits } from 'src/context'
import { LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon} from "@vue-leaflet/vue-leaflet"
import { useMapBounds } from 'src/helpers'

import moment from 'moment'
import 'moment/locale/es'
moment.locale('es')

export default {
  components: {LPopup, LTooltip, LPolyline, LMap, LTileLayer, LMarker, LGeoJson, LControl, LCircleMarker, LIcon},
  props: ['map'],
  setup(props) {
    const { map } = toRefs(props)
    const { visitsGroupByMobile, visits, selectedVisit, selectVisit } = useVisits()
    const { setMapBoundGroup } = useMapBounds(map)
    const { eventVisualization, selectedZoneListMainTab } = useSettings()
    const { getMobileById } = useMobiles()

    const showEvents = computed(() => eventVisualization.value !== 'none')
    const primaryColor = computed(() => colors.getPaletteColor('primary'))
    const handleClickEvent = async event => {
      if (selectedZoneListMainTab.value !== 'events') {
        selectVisit(null)
        selectedZoneListMainTab.value = 'events'
        await nextTick()
      }
      selectVisit(event)
    }

    const visitsToBound = computed(() => showEvents.value ?  visits.value.filter(v => v.visible.value): [])
    onMounted(() => setMapBoundGroup('visits', visitsToBound))
    watch(visitsToBound, () => setMapBoundGroup('visits', visitsToBound))

    return {
      moment,
      showEvents,
      primaryColor,
      selectedVisit,
      visitsGroupByMobile,
      handleClickEvent,
      getMobileById,
    }
  },
}
</script>

<style scoped>
.rounded-tooltip-item {
  background-color: white;
  border-radius: 14px;
  min-width: 80px;
  height: 30px;
  max-height: 35px;
  min-height: 35px;
  display: flex;
  align-content: center;
  align-items: center;
  box-shadow: 0 0 10px 5px #0005;
  font-size: 12px;
}
</style>
