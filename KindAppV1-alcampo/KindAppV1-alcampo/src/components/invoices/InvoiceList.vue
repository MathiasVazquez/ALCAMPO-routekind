<template>
  <q-toolbar class="bg-white q-px-lg column" style="align-items: start">
    <div class="items-baseline row q-gutter-x-sm no-wrap">
      <div class="text-h5 text-weight-light"></div>
      <div class="text-h4 text-weight-bold">{{ invoices.length }}</div>
      <div class="text-h5 text-weight-light">
        {{ invoices.length === 1 ? "factura emitida" : "facturas emitidas" }}
      </div>
    </div>
  </q-toolbar>

  <q-list>
    <q-scroll-area
      ref="scrollAreaRef"
      class="q-mt-md"
      style="height: calc(100vh - 182px)"
      @scroll="onListScroll"
    >
      <q-item class="q-px-lg q-pb-md q-pt-none q-ma-none">
        <q-item-section>
          <div class="row items-center q-gutter-x-sm no-wrap">
            <q-input
              v-if="invoices.length > 0"
              outlined
              dense
              v-model="search"
              placeholder="Buscar factura"
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
      <InvoiceItem
        v-for="invoice of invoices"
        :key="invoice.id"
        :invoice="invoice"
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
import { useInvoices } from "src/context"
import InvoiceItem from "./InvoiceItem"

export default {
  components: { InvoiceItem },
  setup() {
    const search = ref("")
    const scrollAreaRef = ref(null)
    const showGoToTopBtn = ref(false)
    const { invoices } = useInvoices()

    const sortedInvoices = computed(() =>
      invoices.value.sort((i1, i2) =>
        new Date(i1.date) < new Date(i2.date)
          ? 1
          : new Date(i1.date) > new Date(i2.date)
          ? -1
          : 0
      )
    )

    const onListScroll = (event) =>
      (showGoToTopBtn.value = event.verticalPosition > 100)
    const setScrollPosition = (position) =>
      scrollAreaRef.value.setScrollPosition("vertical", position, 200)

    return {
      search,
      invoices: sortedInvoices,
      scrollAreaRef,
      showGoToTopBtn,
      setScrollPosition,
      onListScroll,
    }
  },
}
</script>
