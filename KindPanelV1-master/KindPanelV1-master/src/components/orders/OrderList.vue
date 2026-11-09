<template>
  <q-list class="text-black q-mt-sm">
    <!-- HEADER -->
    <q-item class="column q-mb-sm q-pb-md">
      <q-item-section class="q-mb-sm">
        <q-input dense outlined placeholder="Buscar pedido" />
      </q-item-section>
      <q-item-section style="margin: 0">
        <div class="row items-center no-wrap full-width">
          <!-- DATE FILTER SELECTOR -->
          <q-btn-dropdown
            no-caps
            flat
            align="left"
            style="border: 1px solid #bbb"
          >
            <template #label>
              <div class="row full-width text-weight-regular">
                {{ orderDateFilterLabel }}
              </div>
            </template>
            <q-date
              flat
              landscape
              today-btn
              v-model="orderDateFilter"
              :events="orderDates"
              :event-color="
                (d) =>
                  getOrdersByDate(d).some((o) => !o.assigned.value)
                    ? 'red'
                    : 'green'
              "
            >
              <q-badge v-if="unassignedOrders.length > 0" color="red"
                >Pedidos sin asignar</q-badge
              >
              <!-- <div>{{getOrdersByDate(orderDateFilter)}}</div> -->
            </q-date>
          </q-btn-dropdown>
          <q-space />
          <!-- SYNC ORDERS -->
          <SyncEntityBtn
            :entityManager="[ordersManager, visitsManager]"
            message="Sincronizar pedidos"
          />
        </div>
      </q-item-section>
      <q-item-section style="margin: 0"> </q-item-section>
    </q-item>

    <!-- ASSIGNED ORDER LIST -->
    <!-- <div v-if="Object.keys(ordersGroupByMobileWithUnassigned).length === 0">
      <q-item-label caption class="q-ma-md"> Sin pedidos </q-item-label>
    </div> -->
    <div
      v-for="(groupOrders, mobileId) of ordersGroupByMobileWithUnassigned"
      :key="mobileId"
    >
      <div class="row items-center q-ma-md" v-if="groupOrders.length > 0">
        <q-item-label caption class="q-mr-sm">{{
          mobileId === "-1" ? "SIN ASIGNAR" : getMobileById(mobileId)?.name
        }}</q-item-label>
        <q-badge
          color="grey-1"
          text-color="grey-8"
          style="border: 1px solid #ddd"
          rounded
          :label="`${groupOrders.length}`"
        />
      </div>

      <!-- ITEMS -->
      <draggable
        v-if="!updatingList"
        :list="groupOrders"
        item-key="id"
        @start="draging = true"
        @end="draging = false"
        @change="(e) => handleOnChange(e, groupOrders)"
        handle=".drag-handler"
      >
        <template #item="{ element, index }">
          <div>
            <GenericEntityItem
              alias="Pedido"
              :entity="element"
              :entityManager="ordersManager"
              :shortNameFilter="(_) => `${index + 1}`"
              selectedClass="bg-grey-3"
            >
              <template #upper>
                <q-item-label caption> N° {{ element.id }} </q-item-label>
              </template>

              <template #inavatar>
                <q-badge v-if="element.hasSorted" rounded color="green" floating
                  ><q-icon name="check"
                /></q-badge>
                <q-badge
                  v-else-if="element.mobile"
                  rounded
                  color="orange"
                  floating
                  ><q-icon name="warning"
                /></q-badge>
              </template>

              <!-- ORDER CUSTOMER NAME -->
              <template #label>
                <div class="column">
                  <div class="row q-gutter-x-xs">
                    <div>
                      <span class="text-grey-7">Para</span>
                      {{ element.customerAddress?.customer?.firstName || "" }}
                      {{ element.customerAddress?.customer?.lastName || "" }}
                    </div>
                    <!--<q-avatar v-if="element.hasSorted" round size="16px" color="green" text-color="white" icon="check"></q-avatar>
                      <q-avatar v-else-if="element.mobile" round size="16px" color="orange" text-color="white" icon="warning">
                        <q-tooltip>órden de entrega no asiganada</q-tooltip>
                      </q-avatar>-->
                  </div>
                  <div
                    v-if="element.customerAddress?.description"
                    class="text-caption text-grey-7"
                  >
                    {{ element.customerAddress?.description }}
                  </div>
                  <div class="row q-gutter-x-xs">
                    <div v-if="element.hasDelivered.value">
                      <q-badge color="green">Entregado</q-badge>
                    </div>
                    <div v-if="!element.mobile && element.autoAssignedToMobile">
                      <q-badge color="orange">Automático</q-badge>
                    </div>
                    <div
                      v-else-if="
                        !element.mobile && !element.autoAssignedToMobile
                      "
                    >
                      <q-badge color="red">Sin asignar</q-badge>
                    </div>
                  </div>
                </div>
              </template>

              <!-- ADDRESS DESCRIPTION -->
              <template #final>
                <q-item-section side>
                  <q-btn
                    v-if="element.hasSorted"
                    class="drag-handler"
                    flat
                    round
                    icon="drag_handle"
                  />
                  <q-btn
                    v-else-if="element.mobile || element.autoAssignedToMobile"
                    flat
                    round
                    icon="add_link"
                    @click="addAsLastOrder(element, groupOrders)"
                  />
                </q-item-section>
              </template>

              <!-- UNION LINE -->
              <!--<template v-if="!draging" #pre="{color}">
                  <div v-if="element.nextOrder && index + 1 < groupOrders.length" class="bottom-union-line" :style="`border:2px dashed ${color}`" />
                </template>-->
            </GenericEntityItem>
          </div>
        </template>
      </draggable>
    </div>
  </q-list>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useMobiles, useOrders, useSettings, useVisits } from "src/context"
import { formatToDatePicker } from "src/helpers"
import GenericEntityItem from "src/components/includes/GenericEntityItem"
import SyncEntityBtn from "src/components/includes/SyncEntityBtn"
import draggable from "vuedraggable"

const {
  allOrders,
  ordersManager,
  selectOrder,
  insertOrderAtIndex,
  unassignedOrders,
  ordersGroupByMobileWithUnassigned,
  getOrdersByDate,
} = useOrders()
const { visitsManager } = useVisits()
const { getMobileById } = useMobiles()
const { orderDateFilter, orderDateFilterLabel } = useSettings()

const draging = ref(false)
const handleOnChange = (e, groupOrders) => {
  const maxIndex = groupOrders.filter((o) => o.hasSorted).length
  insertOrderAtIndex(Math.min(maxIndex, e.moved.newIndex + 1), e.moved.element)
}
const addAsLastOrder = (order, groupOrders) => {
  const len = groupOrders.filter((o) => o.hasSorted).length
  const index = len === 0 ? 1 : len + 1
  insertOrderAtIndex(index, order)
}

// const customerAddress = order => order.customerAddress // getCustomerAddressById(order.customerAddress)
// const orderCustomer = (order) => order?.customerAddress?.customer // getCustomerById(customerAddress(order)?.customer)

const orderDates = computed(() =>
  allOrders.value.map((o) => formatToDatePicker(new Date(o.expiryDate)))
)
watch(orderDateFilterLabel, () => selectOrder(null))

const updatingList = ref(false)
/*watch(ordersGroupByMobileWithUnassigned, async () => {
  updatingList.value = true
  await nextTick()
  updatingList.value = false
})*/
</script>

<style scoped>
.list-container {
  position: absolute;
  left: 80px;
  top: 20px;
  z-index: 9999;
}
.bottom-union-line {
  position: absolute;
  width: 1px;
  z-index: 999;
  left: 40px;
  height: 37px;
  background-color: transparent;
  transform: translateY(47px);
  /*transform: translateY(-23px);*/
}
</style>
