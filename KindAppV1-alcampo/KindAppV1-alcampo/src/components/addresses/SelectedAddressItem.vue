<template>
  <!-- DISTANCE -->

  <q-item v-if="address">
    <q-item-section>
      <q-item-label caption>Distancia</q-item-label>
      <div class="row q-gutter-x-xs items-baseline">
        <div class="text-h4 text-weight-bold text-grey-9">
          {{ distance ? distance[distance.unit] : "---" }}
        </div>
        <div class="text-body1">{{ distance?.unit || "Km" }}</div>
      </div>
    </q-item-section>
    <!--<q-item-section side>
      <q-btn round flat icon="o_edit" class="bg-grey-3" size="18px" />
    </q-item-section>-->
  </q-item>

  <!-- CUSTOMER AND ADDRESS INFO -->

  <q-item v-if="address" class="q-pt-none">
    <q-item-section>
      <div class="row q-gutter-x-sm no-wrap">
        <div class="column">
          <GenericEntityAvatar
            :alias="customer.fullName"
            :entity="address"
            size="25px"
          />
          <div class="flex flex-center relative-position" style="flex-grow: 1">
            <div class="address-side-line"></div>
            <q-icon name="fiber_manual_record" size="16px" color="grey-9" />
          </div>
        </div>
        <div class="column" style="margin-top: 6px">
          <div
            v-if="address.task && !address.hasVisit.value"
            class="row q-mb-xs"
          >
            <q-badge color="primary" label="Visita requerida" />
          </div>
          <div class="text-weight-bold">{{ customer.fullName }}</div>
          <q-item-label :lines="open ? 0 : 2">
            <div class="q-mt-sm">
              {{ address.description || "Sin dirección" }}
            </div>
          </q-item-label>
        </div>
      </div>
    </q-item-section>
  </q-item>
</template>

<script>
import { computed, ref } from "vue"
import { useAddresses, useOrders } from "src/context"
import { useMapDistance } from "src/helpers"
import GenericEntityAvatar from "src/components/includes/GenericEntityAvatar"

export default {
  props: ["open"],
  components: { GenericEntityAvatar },
  setup() {
    const { getOrdersByAddressId, getOrderById } = useOrders()
    const { selectedAddress, getAddressById } = useAddresses()
    const { distanceToCurrentPosition } = useMapDistance()

    const distance = computed(() =>
      distanceToCurrentPosition(selectedAddress.value)
    )
    const customer = computed(() => selectedAddress.value?.customer)
    const selectedAddressOrders = computed(() =>
      getOrdersByAddressId(selectedAddress.value?.id)
    )
    const nextAddressOrders = computed(() => {
      const nextOrderId = selectedAddressOrders.value[0]?.nextOrder
      if (!nextOrderId) return null

      const nextAddress = getOrderById(nextOrderId).customerAddress
      if (!nextAddress) return null

      return nextAddress //getAddressById(nextAddress)
    })

    return {
      distance,
      customer,
      nextAddressOrders,
      address: selectedAddress,
    }
  },
}
</script>

<style scoped>
.address-side-line {
  width: 1px;
  height: 50%;
  background-color: transparent;
  position: absolute;
  border: 1px dashed #444;
  top: 0;
}
</style>
