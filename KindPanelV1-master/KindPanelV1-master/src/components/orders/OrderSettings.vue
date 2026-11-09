<template>
  <div>
    <q-item>
      <!-- TOPBAR -->
      <q-item-section class="q-my-xs">
        <div class="row justify-between items-center no-wrap">
          <div class="text-overline text-grey-8">Información del pedido</div>
          <q-btn flat dense round icon="close" @click="selectOrder(null)" />
        </div>
      </q-item-section>
    </q-item>
    <q-separator />

    <!-- MOBILE - AUTO ASSIGNED -->
    <div v-if="!selectedOrder.mobile && selectedOrder.autoAssignedToMobile">
      <GenericEntityItem
        alias="Pedido"
        :entity="getMobileById(selectedOrder.autoAssignedToMobile)"
        :unselectable="true"
      >
        <template #label>
          <q-item-section>
            <div class="text-caption text-grey-8">Asignado automáticamente a</div>
            <div>{{getMobileById(selectedOrder.autoAssignedToMobile)?.name}}</div>
          </q-item-section>
        </template>

        <q-item-section v-if="!selectedOrder.hasSorted" side>
          <MobileSelector :preventSelection="true" @select="assignMobile" :hideCheck="true" :round="true">
            <template #initList>
              <q-item>
                <q-item-section>
                  <q-item-label caption>Asignar al móvil</q-item-label>
                </q-item-section>
              </q-item>
            </template>
          </MobileSelector>
        </q-item-section>
      </GenericEntityItem>
    </div>

    <!-- MOBILE - MANUAL ASSIGNED -->
    <GenericEntityItem
      v-if="selectedOrder.mobile"
      :entity="getMobileById(selectedOrder.mobile)"
      :unselectable="true"
    >
      <template #label>
        <q-item-section>
          <div class="text-caption text-grey-8">Asignado al móvil</div>
          <div>{{getMobileById(selectedOrder.mobile)?.name}}</div>
        </q-item-section>
      </template>

      <q-menu>
        <MobileSelector :preventSelection="true" @select="assignMobile" :hideCheck="true">
          <template #initList>
            <q-item>
              <q-item-section>
                <q-item-label caption>Asignar al móvil</q-item-label>
              </q-item-section>
            </q-item>
          </template>
          <template #endList>
            <q-separator />
            <q-item clickable @click="assignMobile(null)">
              <q-item-section class="text-red">
                <strong>Remover asignación</strong>
              </q-item-section>
            </q-item>
          </template>
        </MobileSelector>
      </q-menu>

      <q-item-section side>
        <q-icon name="o_edit" color="grey-8" />
      </q-item-section>
    </GenericEntityItem>

    <!-- MOBILE - MANUAL ASSIGNMENT -->
    <div class="q-pa-md" v-if="!selectedOrder.mobile && !selectedOrder.autoAssignedToMobile">
      <MobileSelector :preventSelection="true" @select="assignMobile" :outline="false" :hideCheck="true">
        <template #label>
          <div class="row items-center q-gutter-x-xs full-width q-py-xs">
            <q-icon name="add" size="10px" />
            <div>Asignar móvil</div>
          </div>
        </template>
      </MobileSelector>
    </div>

    <!-- DELIVERY SORT INDEX -->

    <!-- MANUAL ASSIGNED -->
    <GenericEntityItem
      v-if="selectedOrder.mobile || selectedOrder.autoAssignedToMobile"
      alias=""
      :shortNameFilter="e => `${selectedOrderPosition}°`"
      :unselectable="true"
    >
      <template #label>
        <q-item-section>
          <div class="text-caption text-grey-8">
            <div v-if="selectedOrder.hasSorted">Órden de entrega asignado en la posición {{selectedOrderPosition}}</div>
            <div v-else>Órden de entrega sin asignar</div>
          </div>
        </q-item-section>
      </template>

      <q-item-section side>
        <q-icon name="o_edit" color="grey-8" />
      </q-item-section>

      <q-menu>
        <q-list>
          <q-item>
            <q-item-section>
              <q-item-label caption>Asignar posición</q-item-label>
            </q-item-section>
          </q-item>
          <q-item v-for="(order, index) of sortedMobileOrders.filter(o => o.hasSorted).concat(selectedOrder.hasSorted ? [] : {id: null})"
            clickable :key="index" @click="insertOrderAtIndex(index + 1)"
            v-show="order.id !== selectedOrder.id"
          >
            <q-item-section>Asignar como {{index + 1}}°</q-item-section>
          </q-item>
          <q-separator />
          <q-item v-if="selectedOrder.hasSorted" clickable @click="insertOrderAtIndex(null)">
            <q-item-section class="text-red"><strong>Desasignar</strong></q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </GenericEntityItem>

    <q-item v-if="!selectedOrder.hasSorted && sortedMobileOrders"
      class="q-px-sm q-mx-md" style="margin-top:-16px"
    >
      <q-item-section>
        <div class="row">
          <q-btn flat no-caps
            class="text-weight-regular q-pr-sm"
            style="padding-left:2px"
            @click="insertOrderAtIndex(sortedMobileOrders.length + 1)"
          >
            <div class="row items-center q-gutter-x-sm">
              <q-icon name="add_link" />
              <div>Asignar como {{sortedMobileOrders.length + 1}}°</div>
            </div>
          </q-btn>
        </div>
      </q-item-section>
    </q-item>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useOrders, useMobiles } from 'src/context'
import GenericEntityItem from 'src/components/includes/GenericEntityItem'
import MobileSelector from 'src/components/mobile/MobileSelector'

export default {
  components: {GenericEntityItem, MobileSelector},
  setup() {
    const { orders, selectedOrder, selectOrder, updateOrder, ordersGroupByMobileWithUnassigned, ordersGroupByMobile, insertOrderAtIndex } = useOrders()
    const { getMobileById, selectedMobileList } = useMobiles()
    const detailsTab = ref('assignment')
    const showSaveSortIndex = ref(false)
    const selectedOrderMobile = computed(() => selectedOrder.value.mobile || selectedOrder.value.autoAssignedToMobile)
    const selectedOrderAddresess = computed(() => ordersGroupByMobileWithUnassigned.value[selectedOrderMobile.value])
    const assignedSortIndexOrders = computed(() => orders.value.filter(o => o.hasSorted))
    const sortedMobileOrders = computed(() => ordersGroupByMobile.value[selectedOrderMobile.value]?.filter(o => o.hasSorted))
    const selectedOrderPosition = computed(() => {
      let index = 1
      for (const order of sortedMobileOrders.value)
        if (order.id === selectedOrder.value.id) break
        else index++
      return index
    })

    const assignMobile = async mobile => await updateOrder({ id: selectedOrder.value.id, mobile: mobile?.id || null })

    return {
      detailsTab,
      selectOrder,
      selectedOrder,
      showSaveSortIndex,
      selectedMobileList,
      sortedMobileOrders,
      selectedOrderPosition,
      selectedOrderAddresess,
      assignedSortIndexOrders,
      insertOrderAtIndex,
      getMobileById,
      assignMobile,
    }
  },
}
</script>
