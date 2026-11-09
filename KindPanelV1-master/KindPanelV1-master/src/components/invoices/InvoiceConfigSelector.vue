<template>
    <q-list v-if="avaibleInvoiceConfigs.length > 0">
        <q-item v-for="invoiceConfig of avaibleInvoiceConfigs" :key="invoiceConfig.id"
            clickable class="q-pa-md column"
            @click="handleAssignInvoiceConfig(invoiceConfig)"
        >
            <q-item-section>
                <q-item-label>{{invoiceConfig.name}}</q-item-label>
                <q-item-label caption>{{invoiceConfig.stamped}}</q-item-label>
                <q-item-label caption>{{invoiceConfig.serialNumber}}</q-item-label>
            </q-item-section>
        </q-item>
    </q-list>
    <q-item v-else style="max-width:300px" class="bg-grey-2">
        <q-item-section>
            <q-item-label>No quedan facturaciones disponibles para asignar</q-item-label>
            <q-item-label class="q-mt-sm" caption>Al parecer, todas las facturaciones ya están asignadas, pero siempre puedes crear una nueva facturación.</q-item-label>
        </q-item-section>
    </q-item>
</template>

<script>
import { computed, ref } from 'vue'
import EmptyListFace from 'src/components/includes/EmptyListFace'
import { useMobiles, useInvoiceConfigs } from 'src/context'

export default {
    components: { EmptyListFace },
    emits: ['select'],
    setup() {
        const { mobiles, selectedMobile, updateMobile } = useMobiles()
        const { invoiceConfigs } = useInvoiceConfigs()
        const avaibleInvoiceConfigs = computed(() => invoiceConfigs.value.filter(w => !mobiles.value.some(m => m.invoiceConfig == w.id)))

        const handleAssignInvoiceConfig = async invoiceConfig => {
            await updateMobile({ id: selectedMobile.value.id, invoiceConfig: invoiceConfig.id })
        }

        return {
            selectedMobile,
            avaibleInvoiceConfigs,
            handleAssignInvoiceConfig
        }
    },
}
</script>