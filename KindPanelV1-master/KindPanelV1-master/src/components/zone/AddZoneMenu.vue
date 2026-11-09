<template>
  <q-card class="container" style="width:280px">
    <div class="container-side-bar bg-primary"></div>
    <q-card-section class="q-gutter-y-md">
      <q-btn-dropdown flat no-caps class="full-width bg-grey-2" align="left" auto-close>
        <template #label>
          <div class="column full-width q-py-sm">
            <div class="text-caption row q-mb-xs">Asignar zona a</div>
            <div class="row" style="margin-top:-6px">{{selectedMobile?.name}}</div>
          </div>
        </template>
        <q-list>
          <q-item clickable
            v-for="mobile of mobiles" :key="mobile.id"
            v-show="mobile.id !== selectedMobile.id && mobile.isActive"
            @click="selectedMobile=mobile"
          >
            <q-item-section>
              {{mobile.name}}
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <div>
        <q-input v-model="newRouteName" outlined placeholder="Nombre de la nueva zona" @keypress.enter="handleCreateZone" autofocus />
        <div class="text-caption text-grey-8 q-px-xs q-mt-sm">Presione Enter para crear</div>
      </div>
      <div class="row justify-end">
        <q-btn color="primary" @click="handleCreateZone" v-close-popup>Crear</q-btn>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { ref } from 'vue'
import { useMobiles, useZones, usePlanning } from 'src/context'

export default {
  setup() {
    const { addZone } = useZones()
    const { mobiles } = useMobiles()
    const { selectedPlanning } = usePlanning()
    const newRouteName = ref("")
    const selectedMobile = ref(mobiles.value.find(m => m.isActive))

    const handleCreateZone = async () => {
      if (!selectedMobile.value) {}
      else await addZone({
        mobile: selectedMobile.value.id,
        planning: selectedPlanning.value.id,
        name: newRouteName.value
      })
    }

    return {
      mobiles,
      newRouteName,
      selectedMobile,
      handleCreateZone,
    }
  },
}
</script>

<style scoped>
.container {
  position: relative;
}
.container-side-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 6px;
  height: 100%;
}
</style>
