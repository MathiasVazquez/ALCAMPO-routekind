<template>
  <GenericEntityItem
    :entity="order"
    :entityManager="ordersManager"
    :alias="selectedAddress.description || selectedAddress.customer.fullName"
    :outline="true"
    :unselectable="true"
    :selectedClass="['bg-grey-3']"
    @click="$emit('click', order)"
  >
    <template #label>
      <q-item-section>
        <div v-for="detail of order.details" :key="detail.id" class="row items-center justify-between no-wrap">
          <div>{{detail.quantity}}x <strong>{{getProductById(detail.product).productName}}</strong></div>
          <div>{{formatMoney(detail.unitPrice)}} Gs. c/u</div>
        </div>

        <div v-if="order.invoiceNumber" class="q-mt-xs row items-center q-gutter-x-xs text-caption">
          <q-icon name="o_receipt_long" />
          <div>{{order.invoiceNumber}}</div>
        </div>
      </q-item-section>
      <slot name="append" />
    </template>
  </GenericEntityItem>
</template>

<script>
import { useOrders, useAddresses, useProducts } from 'src/context'
import { formatMoney } from 'src/helpers'
import GenericEntityItem from 'src/components/includes/GenericEntityItem'

export default {
  components: {GenericEntityItem},
  props: ['order'],
  emits: ['click'],
  setup() {
    const { ordersManager } = useOrders()
    const { selectedAddress } = useAddresses()
    const { getProductById } = useProducts()

    return {
      ordersManager,
      selectedAddress,
      getProductById,
      formatMoney,
    }
  },
}
</script>
