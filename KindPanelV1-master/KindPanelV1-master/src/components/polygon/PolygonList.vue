<template>
  <q-list class="text-black">
    <!-- HEADER -->
    <q-item class="column">
      <q-item-section class="q-my-sm" style="margin: 0">
        <q-input
          v-model="searchFigure"
          dense
          outlined
          :placeholder="`Buscar figura en ${selectedZone.alias}`"
        />
      </q-item-section>
      <q-item-section style="margin: 0">
        <div class="row q-my-sm q-gutter-x-xs no-wrap items-center">
          <q-btn
            no-caps
            dense
            flat
            icon="add"
            class="bg-primary text-grey-1 q-pr-sm"
            @click="handleAddPolygon"
          >
            Nueva figura
          </q-btn>
          <q-checkbox
            :model-value="selectedZone.includeInternalCustomers ?? true"
            @update:model-value="
              updateZone({
                id: selectedZone.id,
                includeInternalCustomers: $event,
              })
            "
            label="Incluir clientes"
          />
          <!--<q-btn no-caps dense flat icon="rule" class="bg-grey-4 text-grey-9 q-pr-sm">
            <q-menu>
              <EditableMapOptionsMenu />
            </q-menu>
          </q-btn>-->
          <!--<q-btn no-caps dense flat icon="o_edit" class="bg-grey-2 text-grey-6" @click="showPolygonEditor=true">Modificar</q-btn>-->
        </div>
      </q-item-section>
    </q-item>
    <!-- LIST OF POLYGONS -->
    <div v-for="section of selectedZonePolygonsGroups" :key="section.id">
      <!-- SUB LIST TITLE -->
      <q-item-label
        v-if="section.list.length > 0"
        caption
        class="q-ma-md text-grey-7"
        >{{ section.title }}</q-item-label
      >
      <!-- ITEMS -->
      <GenericEntityItem
        v-for="polygon of section.list"
        :key="polygon.id"
        alias="Figura"
        :entity="polygon"
        :entityManager="polygonsManager"
        :color="polygon.color"
        selectedClass="bg-grey-3"
      >
        <template #final="{ entity, selected }">
          <q-item-section v-if="selected" side>
            <div class="row no-wrap">
              <!-- EDIT MODE -->
              <q-btn
                :flat="!showPolygonEditor"
                :color="showPolygonEditor ? 'primary' : 'grey-7'"
                dense
                round
                icon="o_edit"
                @click="showPolygonEditor = !showPolygonEditor"
              >
                <q-tooltip>
                  {{ showPolygonEditor ? "Terminar edición" : "Editar figura" }}
                </q-tooltip>
              </q-btn>
              <!-- DELETE POLYGON -->
              <q-btn
                v-if="!showPolygonEditor"
                flat
                dense
                round
                icon="more_vert"
              >
                <q-menu>
                  <q-list>
                    <q-item
                      clickable
                      @click="
                        updatePolygon({
                          id: entity.id,
                          isActive: !entity.isActive,
                        })
                      "
                    >
                      <q-item-section avatar
                        ><q-avatar
                          :icon="
                            entity.isActive ? 'o_toggle_off' : 'toggle_on'
                          "
                      /></q-item-section>
                      <q-item-section>{{
                        entity.isActive ? "Inactivar" : "Activar"
                      }}</q-item-section>
                    </q-item>
                    <q-item clickable>
                      <q-item-section avatar
                        ><q-avatar icon="o_palette"
                      /></q-item-section>
                      <q-item-section>Cambiar color</q-item-section>
                    </q-item>
                    <q-item clickable @click="deletePolygon(entity)">
                      <q-item-section avatar
                        ><q-avatar text-color="red" icon="o_delete"
                      /></q-item-section>
                      <q-item-section class="text-red">Eliminar</q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </div>
          </q-item-section>
        </template>
      </GenericEntityItem>
    </div>
    <!-- EMPTY LIST MESSAGE -->
    <EmptyListFace
      v-if="selectedZonePolygons.length === 0"
      label="Nueva figura"
      @click="handleAddPolygon"
    >
      Todavía no creaste ninguna figura para
      <strong>{{ selectedZone.alias }}</strong>
    </EmptyListFace>
  </q-list>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { usePolygons, useZones, useSettings } from "src/context"
import { getRandomColor } from "src/utils/statics"
import EmptyListFace from "src/components/includes/EmptyListFace"
import GenericEntityItem from "src/components/includes/GenericEntityItem"

const { viewScope } = useSettings()
const { selectedZone, selectZone, updateZone } = useZones()
const {
  polygonsManager,
  addPolygon,
  showPolygonEditor,
  deletePolygon,
  updatePolygon,
} = usePolygons()

const searchFigure = ref("")
const selectedZonePolygons = computed(() => {
  let polys = selectedZone.value.polygons.value

  if (searchFigure.value) {
    polys = polys.filter((p) =>
      p.name.toLowerCase().includes(searchFigure.value.toLowerCase())
    )
  }

  return polys
})

const selectedZonePolygonsGroups = computed(() => {
  return [
    {
      title: "FIGURAS ACTIVAS",
      list: selectedZonePolygons.value.filter((r) => r.isActive),
    },
    {
      title: "FIGURAS INACTIVAS",
      list: selectedZonePolygons.value.filter((r) => !r.isActive),
    },
  ]
})

const deselectZone = () => selectZone(null)
const handleAddPolygon = () =>
  addPolygon({ zone: selectedZone.value.id, color: getRandomColor() })

watch(
  showPolygonEditor,
  () => (viewScope.value = showPolygonEditor.value ? "editmode" : "zones")
)
</script>

<style scoped>
.list-container {
  position: absolute;
  left: 80px;
  top: 20px;
  z-index: 9999;
}
</style>
