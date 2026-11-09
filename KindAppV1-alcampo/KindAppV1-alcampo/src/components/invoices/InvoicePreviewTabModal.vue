<template>
  <q-dialog v-model="showInvoicePreview" :maximized="true">
    <q-layout>
      <q-header>
        <q-toolbar class="bg-white row items-center">
          <div class="row items-center q-gutter-x-sm">
            <q-btn
              flat
              round
              color="grey-8"
              icon="arrow_back"
              @click="showInvoicePreview = false"
            />
          </div>
        </q-toolbar>
      </q-header>

      <q-page-container>
        <q-page>
          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="Original" class="q-pa-none">
              <InvoicePaperPreview name="Original" />
            </q-tab-panel>

            <q-tab-panel name="Duplicado" class="q-pa-none">
              <InvoicePaperPreview name="Duplicado" />
            </q-tab-panel>
          </q-tab-panels>

          <q-page-sticky position="bottom-right" :offset="[18, 18]">
            <q-btn v-if="sending" rounded no-caps color="primary">
              <div class="q-mr-sm q-px-xs" style="font-size: 16px">
                Enviando
              </div>
              <q-spinner />
            </q-btn>
            <q-btn v-else-if="printing" rounded no-caps color="primary">
              <div class="q-mr-sm q-px-xs" style="font-size: 16px">
                Imprimiendo
              </div>
              <q-spinner />
            </q-btn>
            <q-btn
              v-else
              rounded
              no-caps
              icon-right="print"
              color="primary"
              @click="handleSendCurrentSale"
            >
              <div class="q-mr-sm q-px-xs" style="font-size: 16px">
                Imprimir {{ tab.toLowerCase() }}
              </div>
            </q-btn>
          </q-page-sticky>
        </q-page>
      </q-page-container>

      <q-footer>
        <q-toolbar class="bg-white">
          <q-tabs
            dense
            no-caps
            narrow-indicator
            v-model="tab"
            align="justify"
            class="text-grey full-width"
            active-color="primary"
            indicator-color="primary"
          >
            <q-tab name="Original" label="Original" icon="o_receipt" />
            <q-tab name="Duplicado" label="Duplicado" icon="o_content_copy" />
            <!--<q-tab name="summary" label="Resumen" icon="o_summarize" />-->
          </q-tabs>
        </q-toolbar>
      </q-footer>
    </q-layout>
  </q-dialog>
</template>

<script>
import { ref, watch } from "vue"
import {
  connectPrinter,
  disconnectPrinter,
  ESC_ALIGN_LEFT,
  printSingleRow,
  listPrinters,
} from "src/helpers/printer.helper"
import InvoicePaperPreview from "./InvoicePaperPreview"
import { linesToPrint, footerLine } from "src/helpers"
import { useInvoices, useSales, useUI } from "src/context"

export default {
  components: { InvoicePaperPreview },
  setup() {
    const tab = ref("Original")
    const sending = ref(false)
    const printing = ref(false)

    const { addInvoice, showInvoicePreview } = useInvoices()
    const { showAddSaleModal, currentSale } = useSales()
    const { showErrorMessage } = useUI()

    footerLine.value = tab.value
    watch(tab, () => (footerLine.value = tab.value))

    const printInvoice = async () => {
      try {
        const printer = await connectPrinter()
        for (let line of linesToPrint.value)
          await printSingleRow(line.text, line.align || ESC_ALIGN_LEFT)
        await disconnectPrinter(printer)
        await new Promise((resolve) => setTimeout(() => resolve(), 2000))
      } catch (error) {
        // showErrorMessage(JSON.stringfy(error))
        showErrorMessage(
          `No fue posible imprimir la factura: ${JSON.stringify(error)}`
        )
        return { error }
      }
    }

    const handleSendCurrentSale = async () => {
      if (printing.value || sending.value) return
      // Send to server and save
      sending.value = true
      const { error } = await addInvoice(currentSale.value._currentSale)
      sending.value = false
      // On success send
      if (!error) {
        showAddSaleModal.value = false
        // if (!sendResult.reprint) showSuccessMessage({ text: "La factura fue registrada correctamente" })
        // Print invoice
        printing.value = true
        try {
          await printInvoice()
        } catch (error) {}
        printing.value = false
      }
    }

    // onMounted(async () => printers.value = await listPrinters())

    return {
      tab,
      sending,
      printing,
      showInvoicePreview,
      handleSendCurrentSale,
    }
  },
}
</script>
