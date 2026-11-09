<template>
  <q-list>
    <q-item-label class="q-mb-md q-mx-md" caption>{{title || `Pedidos (${selectedAddressOrders.length})`}}</q-item-label>

    <div class="q-px-md">
      <AddressOrderItem v-for="order of selectedAddressOrders" :key="order.id" :order="order" @click="openOrder" />

      <q-item v-if="selectedAddressOrders.length === 0" class="basic-item basic-item-outline" style="margin-top:16px">
        <q-item-section>
          <q-item-label class="text-grey-6">No hay pedidos pendientes</q-item-label>
        </q-item-section>
      </q-item>
    </div>
  </q-list>
</template>

<script>
import { ref, computed, nextTick } from 'vue'
import { useOrders, useAddresses, useSales, useProducts } from 'src/context'
import { formatMoney } from 'src/helpers'
import AddressOrderItem from 'src/components/orders/AddressOrderItem'

export default {
  components: {AddressOrderItem},
  props: ['address', 'title'],
  setup(props) {
    const { getOrdersByAddressId, ordersManager, selectOrder, showOrderDetailsModal } = useOrders()
    const { getProductById } = useProducts()
    const selectedAddress = computed(() => props.address)
    const selectedAddressOrders = computed(() => getOrdersByAddressId(selectedAddress.value?.id).filter(o => !o.hasDelivered.value))

    const openOrder = order => {
      selectOrder(order)
      showOrderDetailsModal.value = true
    }

    return {
      openOrder,
      formatMoney,
      ordersManager,
      getProductById,
      selectedAddress,
      selectedAddressOrders,
    }
  },
}
</script>
