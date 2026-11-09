<template>
  <q-item
    clickable
    v-ripple
    @click="selectAddress(address, false)"
    :class="{ 'bg-grey-3': address.id === selectedAddress.id }"
  >
    <q-item-section avatar>
      <GenericEntityAvatar :alias="address?.customer?.fullName" size="28px" />
    </q-item-section>
    <q-item-section>
      <q-item-label
        class="text-subtitle2 column q-gutter-x-sm"
        style="margin-bottom: -2px"
      >
        <!-- VISIT -->
        <div v-if="address?.task?.type === 'rrequired'" class="q-mb-xs">
          <q-badge color="primary" label="Visita requerida" />
        </div>
        <!-- Customer name -->
        <div>{{ address?.customer?.fullName }}</div>
      </q-item-label>
      <q-item-label
        v-if="address.description"
        class="text-weight-light text-grey-8 text-body2"
      >
        {{ address.description }}
      </q-item-label>
      <q-item-label>
        <div class="row items-center q-gutter-x-sm">
          <!-- Coords -->
          <div v-if="hasCoords && distanceLabel" class="flex items-center">
            <q-icon color="grey-7" name="turn_right" />
            <div class="text-weight-light text-grey-8 text-caption">
              {{ distanceLabel }}
            </div>
          </div>
          <q-badge v-if="!hasCoords" color="red">Sin coordenadas</q-badge>
          <!-- ORDERS -->
          <div
            v-if="pendingOrders.length > 0"
            class="flex items-center q-gutter-x-xs"
          >
            <q-icon color="grey-7" name="o_inventory_2" />
            <div class="text-weight-light text-grey-8 text-caption">
              {{ pendingOrders.length }}
              {{
                pendingOrders.length === 1
                  ? "pedido pendiente"
                  : "pedidos pendientes"
              }}
            </div>
          </div>
        </div>
      </q-item-label>
    </q-item-section>
    <q-item-section
      side
      top
      v-if="address.hasVisit.value && address.visitLater.value"
      class="row"
    >
      <div class="bg-secondary q-px-xs rounded-borders text-caption text-white">
        Visitar más tarde
      </div>
    </q-item-section>
    <q-item-section side top v-else-if="address.hasVisit.value" class="row">
      <div class="bg-green q-px-xs rounded-borders text-caption text-white">
        Visitado
      </div>
    </q-item-section>
  </q-item>
  <q-separator />
</template>

<script>
import { computed } from "vue"
import { useAddresses, useOrders, useVisits } from "src/context"
import { useMapDistance } from "src/helpers"
import GenericEntityAvatar from "src/components/includes/GenericEntityAvatar"

export default {
  props: ["address", "selectedClass"],
  components: { GenericEntityAvatar },
  setup(props) {
    const { selectAddress, selectedAddress } = useAddresses()
    const { distanceToCurrentPosition } = useMapDistance()
    const { getOrdersByAddressId } = useOrders()
    const { getVisitsByAddressId } = useVisits()

    const hasCoords = computed(() => !!props.address.lat && !!props.address.lng)
    const distanceLabel = computed(
      () => distanceToCurrentPosition(props.address)?.label
    )
    const addressOrders = computed(() => getOrdersByAddressId(props.address.id))

    const pendingOrders = computed(() =>
      addressOrders.value.filter((o) => !o.hasDelivered.value)
    )

    return {
      hasCoords,
      pendingOrders,
      distanceLabel,
      addressOrders,
      selectAddress,
      selectedAddress,
    }
  },
}
</script>
