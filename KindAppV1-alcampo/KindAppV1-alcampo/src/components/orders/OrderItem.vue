<template>
  <q-item clickable v-ripple
    :class="{'bg-grey-3': isSelected}"
    @click="handleOrderClick"
  >
    <q-item-section avatar>
      <GenericEntityAvatar
        :shortNameFilter="() => `${index + 1}`"
        :alias="orderAddress.customer.fullName" size="28px" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="text-subtitle2" style="margin-bottom:-2px">
        {{`${orderAddress?.customer.firstName} ${orderAddress?.customer.lastName}` || 'SIN NOMBRE'}}
      </q-item-label>
      <q-item-label v-if="orderAddress?.description" class="text-weight-light text-grey-8 text-body2">
        {{orderAddress.description}}
      </q-item-label>
      <q-item-label>
        <div class="row items-center q-gutter-x-sm">
          <div v-if="hasCoords && distanceLabel" class="flex items-center">
            <q-icon color="grey-7" name="turn_right" />
            <div class="text-weight-light text-grey-8 text-caption">{{distanceLabel}}</div>
          </div>
          <q-badge v-if="!hasCoords" color="red">Sin coordenadas</q-badge>
          <!-- INVOICE NUMBER -->
          <div v-if="order.invoiceNumber" class="flex items-center">
            <q-icon color="grey-7 q-mr-xs" name="o_receipt_long" />
            <div class="text-weight-light text-grey-8 text-caption">{{order.invoiceNumber}}</div>
          </div>
          <!-- LAST VISIT TIME -->
          <div v-if="orderVisit" class="flex items-center">
            <q-icon color="grey-7 q-mr-xs" name="schedule" />
            <div class="text-weight-light text-grey-8 text-caption">{{moment(orderVisit.checkDate).fromNow()}}</div>
          </div>
        </div>
      </q-item-label>
    </q-item-section>

    <q-item-section side>
      <q-badge v-if="order.hasDelivered.value" rounded color="green" class="row items-center q-mb-xs">
        <q-icon name="done_all" />
        <div class="q-ml-xs">Entregado</div>
      </q-badge>
      <q-badge v-else rounded color="red" class="row items-center q-mb-xs">
        <div>Pendiente</div>
      </q-badge>
      <q-btn round flat dense icon="more_horiz" @click="handleShowDetails" />
    </q-item-section>
    <!-- UNION LINE -->
    <!--<template #pre="{color}">
      <div v-if="order.nextOrder" class="bottom-union-line" :style="`border:2px ${order.hasVisit.value ? 'solid' : 'dashed'} ${color}`" />
    </template>-->
  </q-item>
  <q-separator />
</template>

<script>
import { computed } from 'vue'
import { useMapDistance } from 'src/helpers'
import { useAddresses, useOrders, useVisits } from 'src/context'
import moment from 'moment'
import GenericEntityAvatar from 'src/components/includes/GenericEntityAvatar'

export default {
  props: ['order', 'index', 'selectedClass'],
  components: {GenericEntityAvatar},
  setup(props) {
    const { getAddressById, selectedAddress, selectAddress } = useAddresses()
    const { ordersManager, showOrderDetailsModal, selectOrder } = useOrders()
    const { getLastOrderVisitById } = useVisits()
    const { distanceToCurrentPosition } = useMapDistance()

    const orderAddress = computed(() => props.order.customerAddress /*getAddressById(props.order.customerAddress)*/)
    const isSelected = computed(() => orderAddress.value && orderAddress.value.id === selectedAddress.value?.id)

    const hasCoords = computed(() => !!orderAddress.value?.lat && !!orderAddress.value?.lng)
    const distanceLabel = computed(() => distanceToCurrentPosition(orderAddress.value)?.label)
    const orderVisit = computed(() => getLastOrderVisitById(props.order.id))

    const handleOrderClick = () => selectAddress(orderAddress.value)
    const handleShowDetails = () => {
      selectOrder(props.order)
      showOrderDetailsModal.value = true
    }

    return {
      moment,
      hasCoords,
      orderVisit,
      isSelected,
      orderAddress,
      distanceLabel,
      ordersManager,
      showOrderDetailsModal,
      getLastOrderVisitById,
      handleShowDetails,
      handleOrderClick,
    }
  },
}
</script>

<style scoped>
.bottom-union-line {
  position: absolute;
  width: 1px;
  z-index: 999;
  left: 51px;
  height: 36px;
  background-color: transparent;
  transform: translateY(48px);
  /*transform: translateY(47px);*/
}
</style>
