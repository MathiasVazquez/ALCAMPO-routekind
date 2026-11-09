<template>
  <q-list class="text-black q-mt-sm">
    <!-- HEADER -->
    <q-item class="column">
      <q-item-section class="q-my-sm" style="margin: 0">
        <q-input v-model="searchZone" dense outlined placeholder="Buscar zona">
          <template #append>
            <q-btn
              v-if="searchZone"
              flat
              round
              icon="close"
              @click="searchZone = ''"
            />
          </template>
        </q-input>
      </q-item-section>
      <q-item-section style="margin: 0">
        <div class="row q-my-sm q-gutter-x-xs">
          <q-btn
            no-caps
            dense
            flat
            icon="add"
            class="bg-primary text-grey-1 q-pr-sm"
          >
            Nueva zona
            <q-menu><AddZoneMenu /></q-menu>
          </q-btn>
          <!--<q-btn no-caps dense flat icon="o_edit" class="bg-grey-2 text-grey-6" @click="showPolygonEditor=true">Modificar</q-btn>-->
        </div>
      </q-item-section>
    </q-item>
    <!-- LIST -->
    <q-list
      v-for="(zoneGroup, mobileId) in filteredZonesGroupedByMobile"
      :key="mobileId"
    >
      <q-item-label caption class="q-ma-md text-grey-7">{{
        getMobileById(mobileId)?.name.toUpperCase()
      }}</q-item-label>
      <GenericEntityItem
        v-for="zone of zoneGroup"
        :key="zone.id"
        :alias="zone.alias"
        :entity="zone"
        :entityManager="zonesManager"
        selectedClass="bg-grey-3"
      >
        <template v-slot="{ selected }">
          <div
            v-if="!zone.isActive && !selected"
            class="bg-red text-white q-px-xs rounded-borders"
          >
            Inactivo
          </div>
        </template>

        <template #final="{ entity, selected }">
          <q-item-section side>
            <div class="row items-center">
              <!-- ROUTE OPTIONS -->
              <q-btn v-if="selected" icon="more_vert" flat dense rounded>
                <q-menu>
                  <q-list>
                    <!-- ACTIVATE / INACIVATE -->
                    <q-item
                      clickable
                      @click="
                        updateZone({
                          id: selectedZone.id,
                          isActive: !selectedZone.isActive,
                        })
                      "
                    >
                      <q-item-section avatar>
                        <q-avatar
                          text-color="grey-7"
                          :icon="
                            selectedZone.isActive ? 'o_toggle_off' : 'toggle_on'
                          "
                        />
                      </q-item-section>
                      <q-item-section class="text-grey-7">
                        {{ selectedZone.isActive ? "Inactivar" : "Activar" }}
                      </q-item-section>
                    </q-item>
                    <!-- DELETE -->
                    <q-item clickable @click="handleDeleteZone">
                      <q-item-section avatar>
                        <q-avatar icon="o_delete" text-color="red-5" />
                      </q-item-section>
                      <q-item-section class="text-red-5">
                        Eliminar
                      </q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </div>
          </q-item-section>
        </template>

        <!-- DAYS -->
        <template #under="{ selected }">
          <div v-if="!zone.isActive && selected" class="row">
            <div class="bg-red text-white q-px-xs rounded-borders q-mb-sm">
              Inactivo
            </div>
          </div>
          <ZoneDaysList
            :zone="zone"
            :canRemove="true"
            style="margin-top: -6px"
          />
        </template>
      </GenericEntityItem>
    </q-list>
  </q-list>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useZones, useMobiles, usePolygons } from "src/context"
import ZoneDaysList from "src/components/zone/ZoneDaysList"
import GenericEntityItem from "src/components/includes/GenericEntityItem"
import AddZoneMenu from "src/components/zone/AddZoneMenu"

const { getMobileById } = useMobiles()
const {
  zonesManager,
  selectedZone,
  deleteZone,
  updateZone,
  zonesGroupedByMobile,
  selectZone,
} = useZones()
const { getPolygonById, selectPolygon, selectedPolygon } = usePolygons()

const selectedZoneFirstPolygon = computed(() =>
  getPolygonById(selectedZone.value?.polygons[0])
)

watch(
  selectedZone,
  () =>
    selectedZoneFirstPolygon.value &&
    selectedPolygon.value?.zone !== selectedZone.value?.id &&
    selectPolygon(selectedZoneFirstPolygon.value)
)

const searchZone = ref("")
const filteredZonesGroupedByMobile = computed(() => {
  if (!searchZone.value) return zonesGroupedByMobile.value
  const result = {}
  for (const mobileId in zonesGroupedByMobile.value) {
    result[mobileId] = zonesGroupedByMobile.value[mobileId].filter((zone) =>
      zone.name.toLowerCase().includes(searchZone.value.toLowerCase())
    )
  }
  return result
})

async function handleDeleteZone() {
  const zone = selectedZone.value
  await deleteZone(zone, {
    onConfirm: () => selectZone(null),
  })
}
</script>

<style scoped>
.list-container {
  position: absolute;
  left: 80px;
  top: 20px;
  z-index: 9999;
}
</style>
