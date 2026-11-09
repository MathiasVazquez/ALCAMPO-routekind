<template>
  <div class="full-width">
    <!-- Searcher -->
    <q-input
      dense
      outlined
      autofocus
      v-model="search"
      type="text"
      label="Buscar clientes"
      class="full-width"
    />
    <!-- Options? -->
    <div>
      <div class="text-caption text-grey-7 q-ma-sm">
        <span v-if="search.length < 3"> Escribe al menos 3 carácteres </span>
        <span v-else>
          {{ customerAddressesSearchResult.length }}
          {{
            customerAddressesSearchResult.length === 1
              ? "cliente encontrado"
              : "clientes encontrados"
          }}
        </span>
      </div>
    </div>

    <!-- Result list -->
    <AddressList
      v-if="customerAddressesSearchResult.length > 0"
      :addresses="customerAddressesSearchResult"
      :dense="true"
      @click="$emit('click', $event)"
    >
      <template #side="{ address }">
        <q-btn flat dense round icon="more_vert">
          <q-menu>
            <q-list style="min-width: 100px">
              <q-item clickable @click="focusAddress(address)">
                <q-item-section avatar>
                  <q-avatar icon="location_searching" />
                </q-item-section>
                <q-item-section>Enfocar</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
      </template>
    </AddressList>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useCustomerAddresses, useUI } from "src/context"
import AddressList from "../address/AddressList.vue"

const search = ref("")

defineEmits(["click"])
const props = defineProps(["omitIds"])

const { centerMap } = useUI()
const { customerAddresses } = useCustomerAddresses()
const customerAddressesSearchResult = computed(() => {
  if (!search.value || search.value.length < 3) return []
  return customerAddresses.value.filter(
    (a) =>
      !(props.omitIds || []).includes(a.id) &&
      a.customer?.fullName?.toLowerCase().includes(search.value.toLowerCase())
  )
})

function focusAddress(address) {
  const { lat, lng } = address
  centerMap({ lat, lng, zoom: 19 })
}
</script>
