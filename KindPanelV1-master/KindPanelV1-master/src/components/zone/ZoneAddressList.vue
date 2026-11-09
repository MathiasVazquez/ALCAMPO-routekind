<template>
  <q-list class="text-black">
    <!-- HEADER -->
    <q-item class="column">
      <q-item-section class="q-my-sm" style="margin: 0">
        <div class="row items-center q-gutter-x-sm no-wrap full-width">
          <q-input
            dense
            outlined
            class="full-width"
            :placeholder="`Buscar clientes en ${selectedZone.alias}`"
            v-model="customerSearch"
          >
            <template #append>
              <q-btn
                v-if="customerSearch"
                flat
                round
                icon="close"
                @click="customerSearch = ''"
              />
            </template>
          </q-input>
          <q-btn
            flat
            dense
            icon="sync"
            class="q-px-sm"
            style="height: 40px; border: 1px solid #ccc"
            @click="updateAddresses"
          />
          <q-btn
            flat
            dense
            icon="add"
            class="q-px-sm"
            style="height: 40px; border: 1px solid #ccc"
          >
            <q-menu>
              <div class="q-pa-md">
                <AddressesSearcherMenu
                  :omit-ids="fullSelectedZoneAddresses.map((a) => a.id)"
                  @click="toggleIsAdditional($event.id)"
                />
              </div>
            </q-menu>
          </q-btn>
        </div>
      </q-item-section>
    </q-item>
    <!-- LIST OF POLYGONS -->
    <q-item-label caption class="q-ma-md text-grey-7">
      {{ fullSelectedZoneAddresses.length }}
      {{
        fullSelectedZoneAddresses.length === 1
          ? "CLIENTE SELECCIONADO"
          : "CLIENTES SELECCIONADOS"
      }}
    </q-item-label>
    <!-- ITEMS -->
    <AddressList :addresses="filteredSelectedZoneAddresses">
      <template #bottom-label="{ address }">
        <div v-if="isDeactived(address.id)">
          <q-badge color="red" text-color="white" label="Inactivo" />
        </div>
        <div v-else-if="isAdditional(address.id)">
          <q-badge color="green" text-color="white" label="Adicional" />
        </div>
      </template>

      <template #side="{ address, index }">
        <div class="row no-wrap">
          <!-- DISABLED CUSTOMER FROM ROUTE -->
          <q-btn
            flat
            dense
            round
            icon="more_vert"
            @click="
              (e) => {
                e.stopPropagation()
                e.preventDefault()
              }
            "
          >
            <q-menu auto-close>
              <q-list>
                <!-- MOVE UP -->
                <q-item>
                  <q-item-section class="row no-wrap">
                    <div class="row no-wrap">
                      <q-btn
                        v-if="
                          index > 0 &&
                          filteredSelectedZoneAddresses.length ===
                            fullSelectedZoneAddresses.length
                        "
                        @click="moveItemPosition(index, -1)"
                        flat
                        dense
                        round
                        icon="o_move_up"
                      >
                        <q-tooltip>Mover arriba</q-tooltip>
                      </q-btn>
                      <q-btn
                        v-if="
                          fullSelectedZoneAddresses.length - 1 > index &&
                          filteredSelectedZoneAddresses.length ===
                            fullSelectedZoneAddresses.length
                        "
                        @click="moveItemPosition(index, 1)"
                        flat
                        dense
                        round
                        icon="o_move_down"
                      >
                        <q-tooltip>Mover abajo</q-tooltip>
                      </q-btn>

                      <q-separator spaced inset vertical />

                      <q-btn
                        v-if="index > 0"
                        @click="moveItemPosition(index, -index)"
                        flat
                        dense
                        round
                        icon="keyboard_double_arrow_up"
                      >
                        <q-tooltip>Mover al principio</q-tooltip>
                      </q-btn>
                      <q-btn
                        v-if="fullSelectedZoneAddresses.length - 1 > index"
                        @click="
                          moveItemPosition(
                            index,
                            fullSelectedZoneAddresses.length - index
                          )
                        "
                        flat
                        dense
                        round
                        icon="keyboard_double_arrow_down"
                      >
                        <q-tooltip>Mover al final</q-tooltip>
                      </q-btn>
                    </div>
                  </q-item-section>
                </q-item>

                <q-separator />

                <!-- ACTIVATE / DEACTIVATE -->
                <q-item clickable @click="toggleIsDeactivated(entity.id)">
                  <q-item-section avatar>
                    <q-avatar
                      :icon="
                        isDeactived(address.id) ? 'toggle_on' : 'o_toggle_off'
                      "
                    />
                  </q-item-section>
                  <q-item-section>
                    {{ isDeactived(address.id) ? "Activar" : "Inactivar" }}
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </template>
    </AddressList>
  </q-list>
</template>

<script setup>
import { useZones, useCustomerAddresses } from "src/context"
import AddressList from "src/components/address/AddressList"
import { ref, computed, onMounted } from "vue"
import AddressesSearcherMenu from "../map/AddressesSearcherMenu.vue"

const {
  selectedZone,
  selectedZoneAddresses,
  updateSelectedZoneAddresses,
  setAddressIsActive,
  updateZone,
} = useZones()

const { customerAddresses } = useCustomerAddresses()

const updateAddresses = async () => updateSelectedZoneAddresses()

function sortZoneAddresses(elements, sortedIds) {
  // Crear un mapa para un acceso rápido a los elementos por su id
  const mapElements = new Map()
  elements.forEach((element) => mapElements.set(element.id, element))

  // Ordenar primero por los IDs en idsOrdenados
  const sortedElements = sortedIds.map((id) => mapElements.get(id))

  // Añadir elementos que no están en idsOrdenados al final, manteniendo el orden original
  elements.forEach((element) => {
    if (!sortedIds.includes(element.id)) {
      sortedElements.push(element)
    }
  })

  return sortedElements
}

const customerSearch = ref("")
const fullSelectedZoneAddresses = computed(() => {
  const additional = customerAddresses.value.filter(
    (address) =>
      selectedZone.value.additionalAddresses.includes(address.id) &&
      !selectedZoneAddresses.value.some((a) => a.id === address.id)
  )
  return [...selectedZoneAddresses.value, ...additional]
})
const filteredSelectedZoneAddresses = computed(() => {
  if (!customerSearch.value)
    return sortZoneAddresses(
      fullSelectedZoneAddresses.value,
      selectedZone.value.addressesSorting
    )

  const result = fullSelectedZoneAddresses.value.filter((address) => {
    const fullName = `${address.customer.fullName}`
    return fullName.toLowerCase().includes(customerSearch.value.toLowerCase())
    // const fullNameWords = `${a.customer.fullName}`.split(" ");
    // const searchWords = customerSearch.value.split(" ");

    // return fullNameWords.some(
    //   (nameWord) =>
    //     nameWord &&
    //     searchWords.some(
    //       (sWord) =>
    //         sWord && nameWord.toLowerCase().startsWith(sWord.toLowerCase())
    //     )
    // );
  })

  return sortZoneAddresses(result, selectedZone.value.addressesSorting)
})

const additionalAddresses = computed(
  () => selectedZone.value?.additionalAddresses || []
)

async function toggleIsAdditional(addressId) {
  await setAddressIsActive(selectedZone.value.id, addressId, {
    isActive: !isAdditional(addressId),
    remove: isAdditional(addressId),
  })
}

function isAdditional(addressId) {
  return additionalAddresses.value.includes(addressId)
}

const deactivatedAddresses = computed(
  () => selectedZone.value?.deactivatedAddresses || []
)

async function toggleIsDeactivated(addressId) {
  await setAddressIsActive(
    selectedZone.value.id,
    addressId,
    isAdditional(addressId)
      ? {
          isActive: false,
          remove: true,
        }
      : {
          isActive: isDeactived(addressId),
          remove: isDeactived(addressId),
        }
  )
}

function isDeactived(addressId) {
  return deactivatedAddresses.value.includes(addressId)
}

const currentAddressesSorting = computed(() =>
  fullSelectedZoneAddresses.value.map((address) => address.id)
)

function updateAddressesSorting(addressesSorting) {
  updateZone({
    id: selectedZone.value.id,
    addressesSorting,
  })
}

onMounted(
  () =>
    selectedZone.value.addressesSorting.length === 0 &&
    updateAddressesSorting(currentAddressesSorting.value)
)

function moveItemPosition(index, delta) {
  // const _currentAddresses = currentAddressesSorting.value
  const _currentAddresses = selectedZone.value.addressesSorting

  if (_currentAddresses.length === 0) return updateAddressesSorting()

  const nextAddressesSorting = [..._currentAddresses]
  if (index < 0 || index >= nextAddressesSorting.length) return
  const newPosition = Math.max(
    0,
    Math.min(nextAddressesSorting.length - 1, index + delta)
  )
  const element = nextAddressesSorting.splice(index, 1)[0]
  nextAddressesSorting.splice(newPosition, 0, element)
  updateAddressesSorting(nextAddressesSorting)
}
</script>

<style scoped>
.list-container {
  position: absolute;
  left: 80px;
  top: 20px;
  z-index: 9999;
}
</style>
