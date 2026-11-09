<template>
  <div class="text-overline q-px-xs">Información del cliente</div>
  <!-- CUSTOMER RUC -->
  <q-input borderless :readonly="readonly" label="RUC" class="q-my-sm q-px-md bg-grey-3 rounded-borders" autofocus
    :model-value="currentSale.customerDocument"
    @update:model-value="currentSale = { ...currentSale, customerDocument: $event }"
  />
  <!-- CUSTOMER FISCAL NAME -->
  <q-input borderless :readonly="readonly" label="RAZÓN SOCIAL" class="q-my-sm q-px-md bg-grey-3 rounded-borders"
    :model-value="currentSale.customerFiscalName"
    @update:model-value="currentSale = { ...currentSale, customerFiscalName: $event }"
  />
  <!-- CUSTOMER PHONE NUMBER -->
  <q-input borderless label="TEFÉFONO / CELULAR" class="q-my-sm q-px-md bg-grey-3 rounded-borders"
    :model-value="currentSale.customerPhone"
    @update:model-value="currentSale = { ...currentSale, customerPhone: $event }"
  />
  <!-- CUSTOMER LOCATION -->
  <q-input borderless label="DIRECCIÓN" class="q-my-sm q-px-md bg-grey-3 rounded-borders"
    :model-value="currentSale.customerAddress"
    @update:model-value="currentSale = { ...currentSale, customerAddress: $event }"
  />
  <!-- CLEAR -->
  <div class="row justify-end">
    <q-btn no-caps dense flat @click="clearCustomerInfo" style="text-decoration:underline">Borrar todos los campos</q-btn>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useSales } from 'src/context'

export default {
  setup() {
    const { currentSale } = useSales()
    const readonly = ref(!!currentSale.value.customerDocument && !!currentSale.value.customerFiscalName)

    const clearCustomerInfo = _ => {
      // if (currentSale.value.order) return
      readonly.value = false
      currentSale.value = {
        ...currentSale.value,
        customer: null,
        customerDocument: '',
        customerFiscalName: '',
        customerPhone: '',
        customerAddress: '',
      }
    }

    return {
      readonly,
      currentSale,
      clearCustomerInfo,
    }
  },
}
</script>
