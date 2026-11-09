<template>
  <q-dialog v-if="selectedOrder" v-model="showOrderDetailsModal" :persistent="sending">
    <q-card container class="bg-white flex flex-center" style="min-width:300px">

      <q-btn v-if="!sending" round flat @click="showOrderDetailsModal=false"
        color="grey-8" icon="arrow_back" class="absolute-top-left q-ma-md" style="z-index:100"
      />

      <q-card-section class="column flex-center q-gutter-y-sm full-width">
        <q-avatar round color="primary" text-color="white" icon="room_service" />
        <div v-if="selectedOrder.invoiceNumber" class="column text-h6 text-center">
          <div>Pedido con factura número</div>
          <div>{{selectedOrder.invoiceNumber}}</div>
        </div>
        <div v-else class="text-h6 text-center">Detalles del pedido</div>
        <div class="q-py-sm rounded-borders full-width" style="font-family:Monospace">
          <div>Cliente: {{selectedAddress.customer.fullName || 'OCASIONAL'}}</div>
          <div>CI/RUC: {{selectedAddress.customer.document || ''}}</div>
          <div>Condición de venta: {{selectedOrder.saleCondition || ''}}</div>
          <div>Forma de pago: {{selectedOrder.paymentType || ''}}</div>
          <div class="q-mt-md text-weight-bold">DETALLE</div>
          <div v-for="detail of selectedOrder.details.map(d => { return { ...d, product: getProductById(d.product) } })" :key="detail.id"
            class="row items-center justify-between q-mb-xs"
          >
            <div>{{detail.quantity}}x {{detail.product.productName}}</div>
            <div>{{formatMoney(detail.quantity * detail.unitPrice)}} Gs.</div>
          </div>
          <div class="q-mt-md text-weight-bold">TOTALES</div>
          <div class="row items-center justify-between">
            <div>Total</div>
            <div>{{formatMoney(totalToPay)}} Gs.</div>
          </div>
          <div class="row items-center justify-between">
            <div>Pagado</div>
            <div>{{formatMoney(selectedOrder.totalPayed || 0)}} Gs.</div>
          </div>
          <div class="row items-center justify-between text-weight-bold" style="font-size:18px">
            <div>A cobrar</div>
            <div>{{formatMoney(totalToPay - (selectedOrder.totalPayed || 0))}} Gs.</div>
          </div>
          <div></div>
        </div>
      </q-card-section>

      <q-card-section v-if="unavaibleProducts.length > 0">
        <div class="column flex-center">
          <!-- <div class="bg-red text-white q-pa-sm rounded-borders q-mb-sm">No hay stock suficiente</div> -->
          <div v-for="unavaibleProduct of unavaibleProducts" :key="unavaibleProducts.id"
            class="text-red-10"
          >
            Sin stock suficiente de <strong>{{unavaibleProduct.productName}}</strong> ({{unavaibleProduct.totalQuantity.value}}/{{unavaibleProduct.requiredQty}})
          </div>
        </div>
      </q-card-section>

      <q-card-section v-else-if="!selectedOrder.hasDelivered.value" class="column flex-center q-gutter-y-md">
        <q-btn v-if="selectedOrder.invoiceNumber" rounded color="primary"
          :label="sending ? 'Confirmando...' : 'Confirmar entrega'"
          @click="handleConfirDelivery"
        />
        <q-btn v-if="!sending" :flat="!!selectedOrder.invoiceNumber" rounded :no-caps="!!selectedOrder.invoiceNumber"
          :color="selectedOrder.invoiceNumber ? 'grey-9' : 'primary'" :label="selectedOrder.invoiceNumber ? 'Emitir otra factura' : 'Emitir factura'"
          @click="handleEmitInvoice"
        />
        <!--<q-btn v-if="!sending && !selectedOrder.invoiceNumber" flat rounded no-caps
          color="grey-9" label="Marcar como entregado"
          @click="handleConfirDelivery"
        />-->
      </q-card-section>
      <!-- <q-card-section v-else class="flex flex-center q-gutter-y-md">
        <q-btn flat rounded no-caps v color="grey-9" label="Emitir otra factura"
          @click="handleEmitInvoice"
        />
      </q-card-section> -->

      <!--<q-card-actions class="full-width">
        <q-btn flat @click="showOrderDetailsModal=false" color="grey-8" label="Cancelar" />
        <q-space />
        <q-btn flat color="primary" label="Confirmar" />
      </q-card-actions>-->
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, computed } from 'vue'
import { formatMoney } from 'src/helpers'
import { useOrders, useVisits, useAddresses, useProducts } from 'src/context'

export default {
  setup() {
    const { showOrderDetailsModal, convertOrderToInvoice, selectedOrder } = useOrders()
    const { getProductById } = useProducts()
    const { addresses } = useAddresses()
    const { addVisit } = useVisits()

    const sending = ref(false)
    const selectedAddress = computed(() => selectedOrder.value.customerAddress)
    const totalToPay = computed(() => selectedOrder.value.details.reduce((sum, d) => sum + d.quantity * d.unitPrice, 0))

    const unavaibleProducts = computed(() => {
      const result = []
      for (const detail of selectedOrder.value.details) {
        const product = getProductById(detail.product)
        if (!product.trackInventory) continue
        if (detail.quantity > product.totalQuantity.value) {
          result.push({ ...product, requiredQty: detail.quantity })
        }
      }
      return result
    })

    const handleConfirDelivery = async () => {
      if (sending.value) return
      sending.value = true
      const { error } = await addVisit({
        customerAddress: selectedAddress.value.id,
        visited: true,
        order: selectedOrder.value.id,
        invoiceNumber: selectedOrder.value.invoiceNumber,
      })
      sending.value = false
      if (!error) showOrderDetailsModal.value = false
    }

    const handleEmitInvoice = () => {
      convertOrderToInvoice(selectedOrder.value)
      showOrderDetailsModal.value = false
    }

    return {
      sending,
      totalToPay,
      formatMoney,
      selectedOrder,
      getProductById,
      selectedAddress,
      unavaibleProducts,
      handleEmitInvoice,
      handleConfirDelivery,
      showOrderDetailsModal,
    }
  },
}
</script>
