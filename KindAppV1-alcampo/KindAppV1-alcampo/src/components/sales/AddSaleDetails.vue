<template>
  <div class="full-height column no-wrap">
    <q-card-section class="column" style="padding-bottom:100px">
      <div class="row justify-between items-center text-overline q-px-xs">Condición de venta</div>

      <!-- SALE CONDITION -->

      <q-btn-dropdown align="left" flat class="q-pa-md q-my-sm bg-grey-3" auto-close>
        <template v-slot:label>
          <div class="text-left full-width column">
            <div class="text-left">{{(currentSale.saleCondition || 'SELECCIONAR').toUpperCase()}}</div>
          </div>
        </template>
        <q-list>
          <div v-for="condition of saleConditions" :key="condition">
            <q-item clickable @click="currentSale.saleCondition=condition" class="q-pa-md" >
              <q-item-section>{{condition}}</q-item-section>
            </q-item>
            <q-separator />
          </div>
        </q-list>
      </q-btn-dropdown>

      <!-- PAYMENTS LIST -->

      <div v-for="(payment, paymentIndex) of currentSale.payments" :key="payment.name" class="full-width">
        <div class="row justify-between items-center text-overline q-px-xs q-mt-sm">Forma de pago {{paymentIndex + 1}}</div>
        <div class="row items-center no-wrap">
          <q-btn-dropdown align="left" flat class="q-py-md q-px-md q-my-sm bg-grey-3 full-width" auto-close>
            <template v-slot:label>
              <div class="row items-center justify-between no-wrap full-width">
                <div class="text-left full-width column">
                  <div class="text-left">{{(payment.name || 'SELECCIONAR').toUpperCase()}}</div>
                </div>
                <!--<div class="column items-end rounded-borders q-px-sm q-py-xs">
                  {{formatMoney(payment.amount)}} Gs.
                </div>-->
              </div>
            </template>
            <q-list>
              <div v-for="paymentType of avaiblePaymentTypes" :key="paymentType.name">
                <q-item clickable @click="currentSale.updatePayment(paymentIndex, { ...paymentType })" class="q-pa-md" >
                  <q-item-section>{{paymentType.name}}</q-item-section>
                </q-item>
                <q-separator />
              </div>
            </q-list>
          </q-btn-dropdown>
          <!-- REMOVE PAYMENT -->
          <q-btn v-if="currentSale.payments.length > 1"
            outline icon="o_delete" class="q-py-md q-ml-sm" color="red"
            @click="currentSale.removePayment(paymentIndex)"
          />
        </div>

        <!-- PAYMENT AMOUNT -->
        <q-input type="number"
          :model-value="payment.amount"
          @update:model-value="currentSale.updatePayment(paymentIndex, { amount: $event })"
          borderless :label="`Importe de la forma de pago ${paymentIndex + 1} (Gs.)`"
          class="q-px-md rounded-borders q-mb-sm" style="border:1px solid #ccc"
        >
          <template #append>
            <q-btn unelevated dense round icon="price_check" color="grey-4" text-color="grey-8"
              @click="currentSale.updatePayment(paymentIndex, { amount: parseFloat(payment.amount || 0) + currentSale.totalNotPayed.value })"
            />
          </template>
        </q-input>

        <!-- PAYMENT CARD DETAILS -->

        <q-input v-if="payment.needsCode" borderless
          :model-value="payment.cardNumber"
          @update:model-value="currentSale.updatePayment(paymentIndex, { cardNumber: $event })"
          :label="`Número de boleta de la forma de pago ${paymentIndex + 1}`"
          class="q-px-sm rounded-borders" style="border:1px solid #ccc"
        />

        <!-- PAYMENT BANK NAME -->

        <q-input v-if="payment.needsBank" borderless
          :model-value="payment.bankName || ''"
          @update:model-value="currentSale.updatePayment(paymentIndex, { bankName: $event })"
          :label="`Nombre del bank para la forma de pago ${paymentIndex + 1}`"
          class="q-px-sm q-mt-sm rounded-borders" style="border:1px solid #ccc"
        />

      </div>

      <!-- ADD PAYMENT -->

      <q-btn no-caps outline icon="add" align="left" color="primary"
        class="q-pa-md q-my-sm" label="Agregar forma de pago"
        v-if="avaiblePaymentTypes.length > 0"
        @click="currentSale.addPayment({ ...avaiblePaymentTypes[0], amount: 0 })"
      />

      <!-- INVOICE DOCUMENT SELECTOR -->

      <div v-if="false" class="row justify-between items-center text-overline q-px-xs q-mt-sm">RUC para la factura</div>
      <q-btn-dropdown v-if="false" align="left" flat class="q-pa-md q-my-sm bg-grey-3" auto-close>
          <template v-slot:label>
            <div class="text-left full-width column">
              <div class="text-left">{{(`${customerDocumentFrom.name} (${customerDocumentFrom.document})` || 'SELECCIONAR').toUpperCase()}}</div>
            </div>
          </template>
          <q-list>
            <div v-for="documentType of DOCUMENT_TYPES" :key="documentType.code" v-show="documentType.show">
              <q-item clickable @click="customerDocumentFrom=documentType" class="q-pa-md" >
                <q-item-section>{{`${documentType.name} (${documentType.document})`}}</q-item-section>
              </q-item>
              <q-separator />
            </div>
          </q-list>
      </q-btn-dropdown>
    </q-card-section>

    <!-- FOOTER - TOTAL, PREVIEW -->
    <q-space />
    <q-card-section class="footer-section">
      <div class="row justify-between items-center">
        <div class="column">
          <div class="text-caption">TOTAL</div>
          <div class="row items-end" style="margin-top:-6px">
            <div class="text-h6">Gs {{formatMoney(currentSale.totalPayed.value)}}</div>
            <div style="margin-bottom:3px">/{{formatMoney(currentSale.totalToPay.value)}}</div>
          </div>
        </div>
        <div>
          <q-btn rounded unelevated
            label="Vista previa"
            class="bg-primary text-white"
            :class="{'bg-grey-4 text-grey-8': !currentSale.isValidSale.value}"
            @click="showInvoicePreview=!!currentSale.isValidSale.value"
          />
        </div>
      </div>
    </q-card-section>
  </div>

</template>

<script>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { formatMoney } from 'src/helpers'
import { useSales, usePaymentTypes, useInvoices } from 'src/context'

export default {
  setup() {
    const router = useRouter()
    const isOccasional = ref(false)
    const { showInvoicePreview } = useInvoices()
    const { currentSale } = useSales()
    const { paymentTypes } = usePaymentTypes()

    const saleConditions = ref(['Contado', 'Crédito'])

    const DOCUMENT_TYPES = ref([{
      code: 1,
      name: `Del cliente`,
      document: currentSale.value.customerDocument,
      show: !!currentSale.value.customerDocument
    }, {
      code: 2,
      name: "Genérico",
      document: "44444401-7",
      show: true
    }])
    const customerDocumentFrom = ref(DOCUMENT_TYPES.value[0].show ? DOCUMENT_TYPES.value[0] : DOCUMENT_TYPES.value[1])

    const avaiblePaymentTypes = computed(() => paymentTypes.value.filter(p => !currentSale.value.payments.some(c => c.name === p.name)))


    return {
      currentSale,
      isOccasional,
      paymentTypes,
      saleConditions,
      avaiblePaymentTypes,
      DOCUMENT_TYPES,
      customerDocumentFrom,

      showInvoicePreview,
      formatMoney,
    }
  },
}
</script>

<style scoped>
.footer-section {
  position: absolute;
  bottom: 0;
  width: 100%;
  border-top: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
  background-color: white;
}
</style>
