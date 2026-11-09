<template>
  <div>
    <q-item style="border-bottom: 1px solid #ddd">
      <!-- TOPBAR -->
      <q-item-section class="q-my-xs">
        <div class="row justify-between items-center no-wrap">
          <div class="text-caption text-grey-8">
            Detalles de {{ selectedZone.alias }}
          </div>
          <q-btn flat dense round icon="close" @click="selectZone(null)" />
        </div>
      </q-item-section>
    </q-item>
    <!-- TABS -->
    <q-tabs
      v-model="detailsTab"
      class="text-grey bg-grey-2"
      active-color="primary"
      indicator-color="primary"
      align="justify"
      narrow-indicator
      dense
    >
      <q-tab name="polygons" label="Figuras" />
      <q-tab name="customers" label="Clientes" />
    </q-tabs>

    <q-separator />

    <q-tab-panels v-model="detailsTab" animated>
      <q-tab-panel name="polygons" class="q-pa-none q-ma-none">
        <PolygonList />
      </q-tab-panel>

      <q-tab-panel name="customers" class="q-pa-none q-ma-none">
        <ZoneAddressList />
      </q-tab-panel>
    </q-tab-panels>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useZones } from "src/context";
import PolygonList from "src/components/polygon/PolygonList";
import ZoneAddressList from "src/components/zone/ZoneAddressList";

const { selectedZone, selectZone } = useZones();
const detailsTab = ref("polygons");

// watch(detailsTab, () => {
//   if (detailsTab.value === 'customers')
//     selectedZone.
// })
</script>
