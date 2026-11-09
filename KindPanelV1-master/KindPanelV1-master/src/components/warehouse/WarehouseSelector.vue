<template>
    <q-list v-if="avaibleWarehouses.length > 0">
        <q-item v-for="warehouse of avaibleWarehouses" :key="warehouse.id"
            clickable class="q-pa-md column"
            @click="handleAssignWarehouse(warehouse)"
        >
            <q-item-section>
                <q-item-label>{{warehouse.name}}</q-item-label>
                <q-item-label caption>{{warehouse.clientCode}}</q-item-label>
            </q-item-section>
        </q-item>
    </q-list>
    <q-item v-else style="max-width:300px" class="bg-grey-2">
        <q-item-section>
            <q-item-label>No quedan almacenes disponibles para asignar</q-item-label>
            <q-item-label class="q-mt-sm" caption>Al parecer, todos los almacenes ya están asignados, pero siempre puedes crear un nuevo almacén.</q-item-label>
        </q-item-section>
    </q-item>
</template>

<script>
import { computed, ref } from 'vue'
import EmptyListFace from 'src/components/includes/EmptyListFace'
import { useMobiles, useWarehouses } from 'src/context'

export default {
    components: { EmptyListFace },
    emits: ['select'],
    setup() {
        const showCreateUserModal = ref(false)
        const { mobiles, selectedMobile, updateMobile } = useMobiles()
        const { warehouses } = useWarehouses()
        const avaibleWarehouses = computed(() => warehouses.value.filter(w => !mobiles.value.some(m => m.warehouse == w.id)))

        const handleAssignWarehouse = async warehouse => {
            await updateMobile({ id: selectedMobile.value.id, warehouse: warehouse.id })
        }

        return {
            warehouses,
            selectedMobile,
            avaibleWarehouses,
            showCreateUserModal,
            handleAssignWarehouse
        }
    },
}
</script>