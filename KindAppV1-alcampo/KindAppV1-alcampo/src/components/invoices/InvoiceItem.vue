<template>
  <q-item clickable @click="selectInvoice(invoice)">
    <q-item-section v-if="false" avatar>
      <GenericEntityAvatar :alias="invoice.customerFiscalName || `CO`" size="28px" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="text-subtitle2 column q-gutter-y-xs" style="margin-bottom:-2px">
        <!-- NUMBER -->
        <div>{{invoice.invoiceNumber}}</div>
      </q-item-label>
      <!-- CUSTOMER NAME -->
      <q-item-label class="text-weight-light text-grey-8 text-body2">
        {{invoice.customerFiscalName || 'CLIENTE OCASIONAL'}}
      </q-item-label>

      <q-item-label>
        <div class="row items-center q-gutter-x-sm">
          <!-- DATE -->
          <div class="flex items-center">
            <q-icon color="grey-9" name="schedule" />
            <div class="text-weight-light text-grey-8 text-caption q-ml-xs">
              <span v-if="showDate">
                {{moment(invoice.date).fromNow()}}
              </span>
              <span v-else>
                {{moment(invoice.date).fromNow()}}
              </span>
            </div>
          </div>
          <!-- SALE CONDITION -->
          <div class="flex items-center">
            <q-icon color="grey-9" name="currency_exchange" />
            <div class="text-weight-light text-grey-8 text-caption q-ml-xs">{{invoice.saleCondition}}</div>
          </div>
        </div>
      </q-item-label>
    </q-item-section>

    <q-item-section side top>
      <div class="column items-end">
        <!-- CANCELLED -->
        <div v-if="invoice.cancelled" class="row items-center bg-red text-white q-px-xs rounded-borders text-caption">Anulado</div>
        <!-- INVOICE OPTIONS -->
        <q-btn v-else round flat icon="more_vert">
          <q-menu auto-close>
            <q-list separator>
              <q-item clickable @click="openInvoicePreview">
                <q-item-section avatar>
                  <q-avatar icon="o_receipt" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    Vista previa
                  </q-item-label>
                </q-item-section>
              </q-item>
              <q-item class="text-red" clickable @click="handleCancelInvoice">
                <q-item-section avatar>
                  <q-avatar icon="block" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    Anular factura
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-btn>
        <div class="q-mt-xs">TOTAL</div>
        <div class="q-ml-xs">Gs. {{formatMoney(invoiceTotal)}}</div>
      </div>
    </q-item-section>
  </q-item>
  <q-separator />
  <!--<InvoiceDetailsModal />-->
</template>

<script>
import { ref, computed } from 'vue'
import { formatMoney } from 'src/helpers'
import { useInvoices, useSales, useConfirmModal } from 'src/context'
import GenericEntityAvatar from 'src/components/includes/GenericEntityAvatar'
import InvoiceDetailsModal from './InvoiceDetailsModal'

import moment from 'moment'
import 'moment/locale/es'
moment.locale('es')

export default {
  props: ['invoice'],
  components: {GenericEntityAvatar, InvoiceDetailsModal},
  setup(props) {
    const { selectInvoice, selectedInvoice, showInvoicePreview, cancelInvoice } = useInvoices()
    const { currentSale } = useSales()
    const { showConfirmModal } = useConfirmModal()

    const invoiceTotal = computed(() => props.invoice.payments.reduce((sum, p) => sum + p.amount, 0))

    const showDate = ref(true)
    setInterval(() => { showDate.value = !showDate.value }, 60000)

    const openInvoicePreview = () => {
      currentSale.value = props.invoice
      showInvoicePreview.value = true
    }
    const handleCancelInvoice = () => {
      showConfirmModal({
        text: `¿Está seguro de que desea anular la factura con numeración ${props.invoice.invoiceNumber}?`,
        icon: 'block',
        color: 'red',
        onConfirm: async () => await cancelInvoice(props.invoice)
      })
    }

    return {
      moment,
      showDate,
      invoiceTotal,
      selectInvoice,
      selectedInvoice,
      handleCancelInvoice,
      openInvoicePreview,
      formatMoney,
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
