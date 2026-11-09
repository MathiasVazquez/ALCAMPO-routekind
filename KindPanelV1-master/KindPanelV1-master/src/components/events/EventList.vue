<template>
  <!-- HEADER -->
  <q-item class="column q-mt-sm">
    <q-item-section class="q-mb-sm">
      <q-input dense outlined placeholder="Buscar evento" />
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
          <q-date flat landscape today-btn v-model="orderDateFilter" />
        </q-btn-dropdown>
        <q-space />
        <!-- SYNC ORDERS -->
        <SyncEntityBtn
          :entityManager="[ordersManager, visitsManager]"
          message="Sincronizar eventos"
        />
      </div>
    </q-item-section>
  </q-item>

  <!-- TIME LINE -->
  <div class="q-ml-md q-mr-sm q-mt-sm">
    <!-- <div class="row q-gutter-x-xs">
      <q-btn rounded :flat="selectedBar !== 'visits'" unelevated :color="selectedBar === 'visits' ? 'primary' : 'grey-7'" @click="selectedBar='visits'">Visitas</q-btn>
      <q-btn rounded :flat="selectedBar !== 'orders'" unelevated :color="selectedBar === 'orders' ? 'primary' : 'grey-7'" @click="selectedBar='orders'">Pedidos</q-btn>
      <q-btn rounded :flat="selectedBar !== 'invoices'" unelevated :color="selectedBar === 'invoices' ? 'primary' : 'grey-7'" @click="selectedBar='invoices'">Facturas</q-btn>
    </div> -->

    <q-timeline color="primary">
      <!-- <q-timeline-entry heading>
        Timeline heading
      </q-timeline-entry> -->

      <q-timeline-entry
        v-ripple
        v-for="(visit, index) of visits"
        :key="visit.id"
        class="q-px-sm q-pt-xs cursor-pointer rounded-borders"
        :class="
          selectedVisit && selectedVisit.id === visit.id ? 'bg-grey-3' : ''
        "
        @click="selectVisit(visit)"
        :color="visit.color.value"
      >
        <template #title>
          <div class="column">
            <div class="row q-gutter-x-sm">
              <span class="text-weight-regular text-grey-7">Visita a</span>
              <span class="text-weight-bold">
                {{
                  visit.customer?.fiscalName ||
                  visit.customer?.fullName ||
                  "---"
                }}
              </span>
            </div>
            <div class="row q-mt-xs">
              <q-badge :color="visit.color.value">
                {{ visit.stateLabel.value }}
              </q-badge>
              <!-- <q-badge v-if="!visit.visited && visit.visitLater" color="purple">Volver más tarde</q-badge>
              <q-badge v-else-if="visit.visited" color="green">Concretado</q-badge>
              <q-badge v-else color="red">No concretado</q-badge> -->
            </div>
          </div>
        </template>
        <template #subtitle>
          <div class="column">
            <div class="text-caption q-my-xs">#{{ visit.id }}</div>
            <div class="text-weight-bolder">
              {{ moment(visit.checkDate).calendar() }} POR
              {{ visit.mobile.name }}
            </div>
            <!-- DATE -->
            <!-- <div class="row q-gutter-x-sm items-center no-wrap">
              <q-icon name="schedule" class="text-black text-weight-bold" size="12px" />
              <div class="text-caption text-black text-weight-bold">{{moment(visit.checkDate).calendar()}}</div>
            </div> -->
          </div>
        </template>

        <div class="column q-gutter-y-sm">
          <!-- ORDER -->
          <div
            v-if="visit.order && visit.visited"
            class="row q-gutter-x-sm items-center no-wrap"
          >
            <q-avatar
              icon="check"
              color="green"
              text-color="white"
              size="14px"
            />
            <div class="text-caption text-grey-8">
              PEDIDO N° {{ visit.order.id }} ENTREGADO
            </div>
          </div>
          <!-- INVOICE -->
          <div
            v-if="visit.invoiceNumber || visit.order?.invoiceNumber"
            class="row q-gutter-x-sm items-center no-wrap"
          >
            <q-avatar
              icon="check"
              color="green"
              text-color="white"
              size="14px"
            />
            <div class="text-caption text-grey-8">
              FACTURA N°
              {{ visit.invoiceNumber || visit.order?.invoiceNumber }} ENTREGADA
            </div>
          </div>
          <!-- MESSAGE -->
          <div v-if="visit.message" class="row">
            <!-- <q-avatar icon="check" color="green" text-color="white" size="14px" /> -->
            <!-- <div class="text-overline text-grey-8">MENSAJE</div> -->
            <!-- <div class="text-weight-bold text-grey-9 text-caption q-mb-xs"><u>MENSAJE</u></div> -->
            <div
              class="text-caption text-grey-8 rounded-borders q-pa-sm bg-grey-1"
              style="border: 1px solid #ccc"
            >
              {{ visit.message }}
            </div>
          </div>
          <!--
            <div class="text-overline text-grey-8">DIRECCIÓN DE ENTREGA (LATLNG)</div>
          -->
        </div>
      </q-timeline-entry>
    </q-timeline>
  </div>
</template>

<script>
import { ref, computed } from "vue"
import {
  useVisits,
  useMobiles,
  useCustomerAddresses,
  useSettings,
  useOrders,
} from "src/context"
import SyncEntityBtn from "src/components/includes/SyncEntityBtn"

import moment from "moment"
import "moment/locale/es"
moment.locale("es")

export default {
  components: { SyncEntityBtn },
  setup() {
    const { visits, visitsManager, selectedVisit, selectVisit, sortVisits } =
      useVisits()
    const { getMobileById } = useMobiles()
    const { getCustomerAddressById } = useCustomerAddresses()
    const { getOrderById, ordersManager } = useOrders()
    const { orderDateFilter, orderDateFilterLabel } = useSettings()
    const selectedBar = ref("visits")

    const sortedVisits = computed(() => {
      const result = visits.value
        .filter((v) => v.visible.value)
        .map((v) => {
          const customerAddress = getCustomerAddressById(v.customerAddress)
          return {
            ...v,
            mobile: getMobileById(v.mobile),
            customerAddress,
            customer: customerAddress?.customer,
            order: v.order ? getOrderById(v.order) : null,
          }
        })
      return sortVisits(result)
    })

    return {
      moment,
      selectedBar,
      visitsManager,
      orderDateFilter,
      ordersManager,
      selectedVisit,
      selectVisit,
      visits: sortedVisits,
      getMobileById,
      orderDateFilterLabel,
    }
  },
}
</script>
