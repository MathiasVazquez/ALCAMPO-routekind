<template>
  <q-dialog v-model="showModal" position="bottom" class="shadow-0" style="box-shadow:none">
    <div class="row items-center q-py-sm q-px-xs shadow-0 q-gutter-x-sm">
      <q-btn rounded dense icon="o_receipt_long" class="bg-white q-px-sm text-grey-9">Vista previa</q-btn>
      <q-btn rounded dense color="red" icon="block" class="q-px-sm">Anular factura</q-btn>
    </div>
    <q-card class="shadow-10">
      <q-card-section>
        {{selectedInvoice}}
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { computed } from 'vue'
import { useInvoices } from 'src/context'

export default {
  setup() {
    const { selectedInvoice, selectInvoice } = useInvoices()

    const showModal = computed({
      get: () => !!selectedInvoice.value,
      set: value => { if (!value) selectInvoice(null) },
    })

    return {
      showModal,
      selectedInvoice,
    }
  },
}
</script>
