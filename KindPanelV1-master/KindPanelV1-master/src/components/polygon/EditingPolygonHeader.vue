<template>
  <!-- LOAD GEOJSON DIALOG -->
  <q-dialog v-model="showLoadGeoJson" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Cargar GeoJson</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input dense v-model="geoJsonData" type="textarea" autofocus />
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cancelar" color="grey-8" v-close-popup />
        <q-btn flat label="Cargar" @click="onConfirmGeoJson" />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <!-- LOAD BARRIO DIALOG -->
  <q-dialog v-model="showSearchPlaces" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Busca el barrio</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-input dense v-model="searchGeoJsonCoords" autofocus
          placeholder="Ej.: Asunción San Vicente"
        />
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-list>
          <q-item v-for="(place, index) of filteredPlaces" :key="`${index}-${place.b}`" clickable
            @click="addGeoJson(place.c, `${place.t}, ${place.d}, ${place.b}`, true)"
          >
            <q-item-section avatar>
              <div>{{index + 1}}</div>
            </q-item-section>
            <q-item-section>
              <div><strong>Departamento:</strong> {{place.t}}</div>
              <div><strong>Distrito:</strong> {{place.d}}</div>
              <div><strong>Barrio:</strong> {{place.b}}</div>
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cerrar" color="grey-8" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <!-- HEADER -->
  <q-header bordered>
    <q-toolbar>
      <q-btn flat icon="close" style="margin-right:10px" 
        @click="setEditingPolygon(false)" 
      />
      <div class="row q-gutter-x-md">
        <q-btn flat rounded no-caps @click="move" 
          :class="{'bg-white text-primary': moving}">
          Mover
        </q-btn>
        <q-btn flat rounded no-caps @click="add"
          :class="{'bg-white text-primary': adding}">
          Agregar
        </q-btn>
        <q-btn flat rounded no-caps @click="remove"
          :class="{'bg-white text-primary': removing}">
          Eliminar
        </q-btn>
      </div>
      <q-space />
      <q-btn flat rounded no-caps @click="showSearchPlaces=true">
          Cargar Barrio
      </q-btn>
      <q-btn flat rounded no-caps @click="showLoadGeoJson=true">
          Cargar GeoJson
      </q-btn>
    </q-toolbar>
  </q-header>
</template>

<script>
import { ref, computed } from 'vue'
import { usePolygons, usePolygonPins } from 'src/context'
import places from 'src/assets/places.json'

export default {
  setup() {
    const {
      updatePolygon,
      setEditingPolygon,
      setEditingPolygonState,
      editingPolygonState,
      selectedPolygon,
    } = usePolygons()

    const { replaceAllPins } = usePolygonPins()

    const showLoadGeoJson = ref(false)
    const showSearchPlaces = ref(false)
    const searchGeoJsonCoords = ref("")
    const geoJsonData = ref("")
    
    const moving = computed(_ => editingPolygonState.value.moving)
    const adding = computed(_ => editingPolygonState.value.adding)
    const removing = computed(_ => editingPolygonState.value.removing)

    const move = () => setEditingPolygonState({ moving: true, adding: false, removing: false })
    const add = () => setEditingPolygonState({ moving: false, adding: true, removing: false })
    const remove = () => setEditingPolygonState({ moving: false, adding: false, removing: true })
    const loadGeoJson = () => {
      showLoadGeoJson.value = true
    }
    const addGeoJson = async (geoJson, name = "", invertLatLan = true) => {
      await replaceAllPins(geoJson.map(([lat, lng]) => { return invertLatLan ? [lng, lat] : [lat, lng] }))
      if (name) await updatePolygon({ ...selectedPolygon.value, name })
      searchGeoJsonCoords.value = ''
      showLoadGeoJson.value = false
      showSearchPlaces.value = false
    }
    const onConfirmGeoJson = async () => {
      const geoJson = JSON.parse(geoJsonData.value)
      await addGeoJson(geoJson, "", false)
    }

    const formatedPlaces = computed(() => places.features.map(f => {
      return {
        t: `${f.properties.DPTO_DESC}`,
        d: `${f.properties.DIST_DESC}`,
        b: `${f.properties.BARLO_DESC}`,
        c: f.geometry.coordinates[0][0]
      }
    }))
    const filteredPlaces = computed(() => {
      if (!searchGeoJsonCoords.value) return []
      const words = searchGeoJsonCoords.value.split(",")
      return places.features.filter(p => words.every(word => 
        p.t.toLowerCase().includes(word.toLowerCase()) ||
        p.d.toLowerCase().includes(word.toLowerCase()) ||
        p.b.toLowerCase().includes(word.toLowerCase())
      ))
    })

    const onCreate = () => {
      if (!moving.value && !adding.value && !removing.value) move()
      //console.log(formatedPlaces.value)
    }
    onCreate()

    return {
      moving,
      adding,
      removing,
      geoJsonData,
      filteredPlaces,
      showLoadGeoJson,
      showSearchPlaces,
      searchGeoJsonCoords,
      add,
      move,
      remove,
      addGeoJson,
      loadGeoJson,
      onConfirmGeoJson,
      setEditingPolygon,
    }
  },
}
</script>

<style scoped>

</style>