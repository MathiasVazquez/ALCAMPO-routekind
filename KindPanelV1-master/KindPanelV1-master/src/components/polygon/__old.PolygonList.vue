<template>
  <q-list class="text-black bg-white">

    <!-- HEADER -->
    <q-item class="q-pa-none">
      <q-item-section>
        <q-item-label header overline class="bg-grey-2 full-width">
          <div class="row items-center q-gutter-x-xs">
            <div>FIGURAS</div>
            <q-space />
            <q-btn flat round dense no-caps icon="done_all" size="12px"
              :class="{'text-white bg-primary': showAllPolygons}"
              @click="toggleShowAllPolygons"
            >
              <q-tooltip>Mostrar todo</q-tooltip>
            </q-btn>
            <q-btn flat round dense no-caps icon="add" @click="handleAddPolygon">
              <q-tooltip>Nueva figura</q-tooltip>
            </q-btn>
          </div>
        </q-item-label>
      </q-item-section>
    </q-item>

    <q-separator />

    <!-- FIGURE LIST -->

    <div v-for="poly of enabledPolygons || []" :key="poly.id">
      <PolygonItem :poly="poly" />
    </div>
    <EmptyListFace v-if="!polygons.length" label="Nueva figura" @click="handleAddPolygon">
      Todavía no creaste ninguna figura en esta zona
    </EmptyListFace>
    <EmptyListFace v-else-if="!enabledPolygons.length" label="Nueva figura" @click="handleAddPolygon">
      No hay ninguna figura visible
    </EmptyListFace>

    <!-- DISABLED LIST -->
    <q-item-label v-if="disablePolygons.length" header overline
      class="bg-grey-2"
    >
      <div class="row items-center justify-between no-wrap">
        <div>FIGURAS DESHABILITADAS ({{disablePolygons.length}})</div>
        <q-btn flat dense round size="12px" icon="info">
          <q-tooltip>Los clientes en estas figuras no se mostrarán a los repartidores</q-tooltip>
        </q-btn>
      </div>
    </q-item-label>
    <q-separator v-if="disablePolygons.length"/>
    <div v-for="poly of disablePolygons || []" :key="'u'+poly.id">
      <PolygonItem :poly="poly" />
    </div>
  </q-list>
</template>

<script>
import { ref, computed } from 'vue'
import PolygonItem from './PolygonItem'
import EmptyListFace from 'src/components/includes/EmptyListFace'
import { usePolygons } from 'src/context'

export default {
  components: {PolygonItem, EmptyListFace},
  setup() {
    const { polygons, showAllPolygons, toggleShowAllPolygons, addPolygon } = usePolygons()

    const disablePolygons = computed(_ => polygons.value.filter(p => p.disabled))
    const enabledPolygons = computed(_ => polygons.value.filter(p => !p.disabled))

    //
    // ADD POLYGON
    //
    const adding = ref(false)
    const addingErrorMessage = ref(false)
    const handleAddPolygon = async () => {
      adding.value = true
      const { error } = await addPolygon()
      if (error) addingErrorMessage.value = "No fue posible agregar la figura, por favor vuelva a intentarlo"
      adding.value = false
    }

    return {
      polygons,
      showAllPolygons,
      disablePolygons,
      enabledPolygons,
      handleAddPolygon,
      toggleShowAllPolygons
    }
  },
}
</script>
