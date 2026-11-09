<template>
  <div v-if="selectedPlanning" class="page-container">
    <!-- USER -->
    <div class="text-overline text-weight-regular text-grey-6">PLANIFICACIÓN</div>
    <div class="row items-center q-gutter-x-md">
      <div class="text-h4 text-weight-light">{{planningName}}</div>
      <q-badge color="green" v-if="selectedPlanning.isActive">Activo</q-badge>
      <q-badge color="red" v-else>Inactivo</q-badge>
      <q-space />
      <q-btn no-caps unelevated color="grey-3" text-color="grey-8">
        <div class="row items-center q-gutter-x-sm">
          <q-icon name="o_edit" size="20px" />
          <div>Editar</div>
        </div>
      </q-btn>
      <q-btn no-caps unelevated color="grey-3" text-color="grey-8" icon="more_horiz">
        <q-menu auto-close>
          <q-list>
            <q-item v-if="!selectedPlanning.isActive" clickable @click="activatePlanning" class="text-grey-9">
              <q-item-section avatar>
                <q-avatar icon="done" />
              </q-item-section>
              <q-item-section>
                Activar
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { usePlanning } from 'src/context'
import EmptyListFace from 'src/components/includes/EmptyListFace'
import UserSelector from 'src/components/security/UserSelector'
import MobileSelector from 'src/components/mobile/MobileSelector'
import CreateUserModal from 'src/components/mobileUser/CreateUserModal'
import MobileSelectorForUser from 'src/components/mobile/MobileSelectorForUser'

export default {
  components: {EmptyListFace, CreateUserModal, UserSelector, MobileSelector, MobileSelectorForUser},
  setup() {
    const { planning, selectedPlanning, updatePlanning, setPlanning } = usePlanning()
    const planningName = computed(() => selectedPlanning.value.name || `Planificación ${selectedPlanning.value.id}`)

    const activatePlanning = async () => {
      const { error } = await updatePlanning({ id: selectedPlanning.value.id, isActive: true })
      if (!error) setPlanning(planning.value.map(p => p.id == selectedPlanning.value.id ? p : { ...p, isActive: false }))
    }

    return {
      planningName,
      selectedPlanning,
      activatePlanning,
    }
  },
}
</script>