<template>
  <q-list class="text-black">

    <!-- HEADER -->
    <q-item class="q-pa-none column">
      <q-item-section class="q-px-md" style="min-height:50px">
        <q-item-label header overline class="q-pa-none">
          <div class="row justify-between items-center">
            <div>PLANIFICACIONES</div>
            <div class="row no-wrap items-center">
              <q-btn flat rounded dense no-caps icon="add" 
                @click="addPlanning()" class="q-ma-none"
              >
                <q-tooltip>Nueva planificación</q-tooltip>
              </q-btn>
            </div>
          </div>
        </q-item-label>
      </q-item-section>
    </q-item>

    <GenericEntityItem
      v-for="plan of planning" :key="plan.id"
      alias="Planificación"
      :entity="plan"
      :entityManager="planningManager"
      :shortNameFilter="shortNameFilter"
      :showLabelName="false"
      unselectedClass="bg-grey-3"
      :slice="true"
    >
      <template #after="{ entity }">
        <div>
          <q-badge color="green" v-if="entity.isActive">Activo</q-badge>
          <!--<q-badge color="red" v-else>Inactivo</q-badge>-->
        </div>
      </template>
    </GenericEntityItem>
  </q-list>
</template>

<script>
import { usePlanning } from 'src/context'
import GenericEntityItem from 'src/components/includes/GenericEntityItem'

export default {
  components: {GenericEntityItem},
  setup() {
    const { planning, addPlanning, planningManager, selectedPlanning } = usePlanning()
    const shortNameFilter = plan => {
      const name = plan.name || `Planificación ${plan.id}`
      return `${name[0]}${(name.split(" ")[1] || {})[0] || name[1]}`
    }

    return {
      planning,
      addPlanning,
      planningManager,
      selectedPlanning,
      shortNameFilter,
    }
  },
}
</script>