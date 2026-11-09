<template>
  <l-circle-marker
    v-for="(mobile, index) of mobiles" :key="mobile.id"
    :lat-lng="[mobile.lat || 0, mobile.lng || 0]"
    :radius="7" :color="primaryColor"
    :fill="true" :fillColor="primaryColor" :fillOpacity="1"
    @click="handleClickMobile(mobile)"
  >
    <l-tooltip :options="{permanent: true, direction: 'top'}">
      <q-item class="rounded-tooltip-item column flex-center">
        <q-icon size="28px" name="o_local_shipping" />
        <!-- <div>This is a popup open by default</div> -->
        <q-badge rounded floating color="primary" style="margin-top:-5px">
          <strong>{{mobile.name}}</strong>
          <div class="q-ml-xs">{{mobile.coordsDate ? moment(mobile.coordsDate).fromNow() : ''}}</div>
        </q-badge>
      </q-item>
    </l-tooltip>
  </l-circle-marker>
</template>

<script>
import leaflet from "leaflet"
import { colors } from 'quasar'
import { toRefs, ref, computed, watch, nextTick, onMounted } from 'vue'
import { useSettings, useMobiles } from 'src/context'
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
    const { setMapBoundGroup } = useMapBounds(map)
    const { orderVisualization, selectedZoneListMainTab } = useSettings()
    const { mobiles, getMobileById } = useMobiles()

    const popups = ref([])
    const openPopups = () => {
      if (popups.value.length === 0) return
      // debugger
      console.log('popups.value.leafletObject:', popups.value[0].leafletObject)
      console.log('popups.value.leafletObject.options:', popups.value[0].leafletObject.options)
      popups.value.forEach(popup => {
        popup.leafletObject.options['autoClose'] = false
        popup.leafletObject.options['closeButton'] = false
        popup.leafletObject.options['closeOnEscapeKeyn'] = false
        popup.leafletObject.options['keepInView'] = true
        popup.leafletObject.options['autoPan'] = false
        // console.log('popup.leafletObject:', popup.leafletObject)
      })
    }
    // watch(popups, openPopups)
    // onMounted(async () => {
    //   await nextTick()
    //   openPopups()
    // })

    const showMobiles = computed(() => true)
    const primaryColor = computed(() => colors.getPaletteColor('primary'))
    const handleClickMobile = async event => {}

    const mobilesToBound = computed(() => showMobiles.value ?  mobiles.value.filter(m => m.visible.value) : [])
    onMounted(() => setMapBoundGroup('mobiles', mobilesToBound))
    watch(mobilesToBound, () => setMapBoundGroup('mobiles', mobilesToBound))

    return {
      moment,
      popups,
      mobiles: mobilesToBound,
      showMobiles,
      primaryColor,
      handleClickMobile,
    }
  },
}
</script>

<style scoped>
.rounded-tooltip-item {
  background-color: white;
  border-radius: 200px;
  min-width: 50px;
  height: 50px;
  max-height: 50px;
  min-height: 50px;
  max-height: 50px;
  min-height: 50px;
  display: flex;
  align-content: center;
  align-items: center;
  box-shadow: 0 0 10px 5px #0005;
  font-size: 12px;
}
</style>
