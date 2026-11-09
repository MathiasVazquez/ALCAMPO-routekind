<template>
  <AddVisitModal />
  <AddSaleModalTabs />
  <InvoicePreviewTabModal />
  <OrderDetails />

  <q-layout view="lHh Lpr lFf">
    <q-drawer v-model="showLeftDrawer" show-if-above bordered :width="$q.screen.width">
      <LeftDrawerTabs />
    </q-drawer>

    <q-page-container class="container">
      <router-view />
    </q-page-container>

    <q-footer class="bg-white">
      <q-toolbar>
        <div class="row items-center q-gutter-x-xs full-width">
          <q-btn rounded unelevated icon="add_circle_outline" color="primary" class="row" style="flex-grow:1"
            @click="handleAddSale"
          >
            <div class="q-mx-sm" style="margin-top:1px">Nueva venta</div>
          </q-btn>
          <q-btn @click="handleAddVisit" rounded unelevated color="grey-4" text-color="grey-9">
            <div class="row items-center q-gutter-x-xs">
              <!--<q-icon name="rule" />-->
              <div style="transform:translateY(1px)">Terminar visita</div>
            </div>
          </q-btn>
        </div>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<script>
import { useUI } from 'src/context'
import { useVisits, useSales, useAddresses, useConfirmModal } from 'src/context'
import LeftDrawerTabs from 'src/components/drawers/LeftDrawerTabs'
import AddVisitModal from 'src/components/visits/AddVisitModal'
import AddSaleModalTabs from 'src/components/sales/AddSaleModalTabs'
import InvoicePreviewTabModal from 'src/components/invoices/InvoicePreviewTabModal'
import OrderDetails from 'src/components/orders/OrderDetails'

export default {
  components: {LeftDrawerTabs, AddVisitModal, AddSaleModalTabs, InvoicePreviewTabModal, OrderDetails},
  setup() {
    const { showAddSaleModal, currentSale } = useSales()
    const { showAddVisitModal, getVisitsByAddressId } = useVisits()
    const { selectedAddress } = useAddresses()
    const { showLeftDrawer } = useUI()
    const { showConfirmModal } = useConfirmModal()

    const handleAddSale = () => {
      currentSale.value.clear()
      showAddSaleModal.value = true
    }
    const handleAddVisit = () => {
      const selectedAddressHasVisits = getVisitsByAddressId(selectedAddress.value?.id).length > 0
      if (selectedAddressHasVisits) {
        showConfirmModal({
          text: "Ya ha realizado una visita a esta dirección. ¿Está seguro de que quiere registrar otra?",
          icon: 'o_warning',
          color: 'primary',
          onConfirm: () => showAddVisitModal.value = true
        })
      }
      else showAddVisitModal.value = true
    }

    return {
      handleAddVisit,
      showLeftDrawer,
      showAddSaleModal,
      showAddVisitModal,
      handleAddSale,
    }
  },
}
</script>

<style scoped>
.container {
  position: relative;
  height: 100vh;
  overflow: hidden;
}
</style>
