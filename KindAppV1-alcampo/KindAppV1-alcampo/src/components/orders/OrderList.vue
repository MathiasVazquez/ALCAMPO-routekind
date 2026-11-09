<template>
  <q-toolbar class="bg-white q-px-lg column" style="align-items: start">
    <div class="items-baseline row q-gutter-x-sm no-wrap">
      <!-- <div class="text-h5 text-weight-light">Tienes</div> -->
      <div class="text-h4 text-weight-bold">{{ sortedOrders.length }}</div>
      <div class="text-h5 text-weight-light">pedidos asignados</div>
    </div>
    <div class="full-width q-mt-sm" v-if="finishedOrders.length > 0">
      <div class="row items-center">
        <div class="text-caption text-grey-8">
          {{ finishedOrders.length }} de {{ sortedOrders.length }} pedidos
          entregados
        </div>
        <q-space />
        <div class="text-caption text-grey-8">
          {{ Math.round(listProgress * 100) }}%
        </div>
      </div>
      <q-linear-progress
        rounded
        size="10px"
        :value="listProgress"
        color="primary"
      />
    </div>
  </q-toolbar>

  <q-list>
    <q-scroll-area
      ref="scrollAreaRef"
      class="q-mt-md"
      style="height: calc(100vh - 210px)"
      @scroll="onListScroll"
    >
      <q-item class="q-px-lg q-pb-md q-pt-none q-ma-none">
        <q-item-section>
          <div
            class="row items-center q-gutter-x-sm no-wrap"
            v-if="finishedOrders.length > 0"
          >
            <q-input
              outlined
              dense
              v-model="search"
              placeholder="Buscar pedido"
              style="flex-grow: 1"
            >
              <template #prepend
                ><q-icon name="search" color="grey-7"
              /></template>
            </q-input>
            <!-- <q-btn flat style="height:40px;border:1px solid #bbb" icon="sync" />
            <q-btn flat style="height:40px;border:1px solid #bbb" icon="o_filter_alt" /> -->
          </div>
        </q-item-section>
      </q-item>

      <q-separator />
      <OrderItem
        v-for="(order, index) of sortedOrders"
        :key="order.id"
        :order="order"
        :index="index"
      />

      <div style="padding-bottom: 60px" />

      <q-page-sticky
        v-if="showGoToTopBtn"
        position="bottom-right"
        style="z-index: 100"
        :offset="[18, -40]"
      >
        <q-btn
          round
          icon="keyboard_arrow_up"
          color="primary"
          @click="setScrollPosition(0)"
        />
      </q-page-sticky>
    </q-scroll-area>
  </q-list>
</template>

<script>
import { ref, computed } from "vue"
import { useOrders } from "src/context"
import OrderItem from "./OrderItem"

export default {
  components: { OrderItem },
  setup() {
    const search = ref("")
    const scrollAreaRef = ref(null)
    const showGoToTopBtn = ref(false)
    const { sortedOrders } = useOrders()

    const finishedOrders = computed(() =>
      sortedOrders.value.filter((o) => o.hasDelivered.value)
    )
    const listProgress = computed(
      () => finishedOrders.value.length / sortedOrders.value.length
    )

    const onListScroll = (event) =>
      (showGoToTopBtn.value = event.verticalPosition > 100)
    const setScrollPosition = (position) =>
      scrollAreaRef.value.setScrollPosition("vertical", position, 200)

    return {
      search,
      sortedOrders,
      listProgress,
      scrollAreaRef,
      showGoToTopBtn,
      finishedOrders,
      setScrollPosition,
      onListScroll,
    }
  },
}
</script>
