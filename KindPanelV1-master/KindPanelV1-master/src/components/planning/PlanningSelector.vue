<template>
    <q-btn-dropdown v-if="planning" no-caps flat 
        :label="selectedPlanning ? planName(selectedPlanning) : 'Planificación'"
    >
        <q-list :style="`max-height:${activatedPlanning?'calc(65vh - 60px)':'calc(65vh - 262px)'}`" class="scroll">
            <q-item v-for="plan of planning" :key="plan.id"
                clickable v-close-popup @click="selectPlanning(plan)"
                v-show="!plan.disabled"
            >
                <q-item-section avatar>
                    <q-avatar v-if="selectedPlanning && plan.id===selectedPlanning.id" icon="check" />
                </q-item-section>
                <q-item-section>
                    <q-item-label>{{planName(plan)}}</q-item-label>
                    <q-item-label caption>{{isActivated(plan) ? 'Activado' : 'Desactivado'}}</q-item-label>
                </q-item-section>
            </q-item>
        </q-list>
        <q-list>
            <div v-if="!activatedPlanning">
                <EmptyListFace>
                    Parece ser que no tienes ninguna planificación activa.<br/>
                    Ve a <strong>Gestionar planificaciones</strong> para activar una.
                </EmptyListFace>
            </div>
            <q-separator />
            <!-- MANAGE PLANNING -->
            <q-item clickable v-close-popup to="/planning">
                <q-item-section avatar>
                    <q-avatar icon="o_settings_suggest" />
                </q-item-section>
                <q-item-section>
                    <q-item-label>Gestionar planificaciones</q-item-label>
                </q-item-section>
            </q-item>
        </q-list>
    </q-btn-dropdown>
</template>

<script>
import EmptyListFace from 'src/components/includes/EmptyListFace'
import { usePlanning } from 'src/context'

export default {
    components: {EmptyListFace},
    setup() {
        const {
            planning,
            selectPlanning,
            selectedPlanning,
            activatedPlanning,
        } = usePlanning()

        const isActivated = plan => {
            return activatedPlanning.value && 
            plan.id === activatedPlanning.value.id
        }
        
        const planName = plan => plan.name || `Planificaión ${plan.id}`

        return {
            planName,
            planning,
            selectedPlanning,
            activatedPlanning,
            selectPlanning,
            isActivated,
        }
    },
}
</script>

<style scoped>
</style>