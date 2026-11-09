import { ref } from "vue"
import { store } from "src/store/local.store"
import { useGenericEntityList } from "./generics/listEntity.generic"
import {
  useSession,
  useVisits,
  useProducts,
  useSales,
  useAddresses,
  useOrders,
} from "src/context"
import { useLocation } from "./location.context"

const invoices = ref(store.get("invoices", []))
const selectedInvoice = ref(null)
const showInvoicePreview = ref(false)

export const useInvoices = () => {
  const options = ref({
    entityName: "invoices",
    entityNameSingular: "invoice",
    entityUrl: "invoice/",
    selectedEntity: selectedInvoice,
    canDeselectEntity: true,
    // localOnly: true,
    requestFormatter: (invoice) => {
      const { invoiceConfig, warehouse } = useSession()
      // const { getBatchById } = useBatches()
      const { getProductById } = useProducts()
      const { currentSale } = useSales()
      return {
        ...invoice,
        invoiceConfig: invoiceConfig.value.id,
        startDate: invoiceConfig.value.startDate || "",
        dueDate: invoiceConfig.value.dueDate || "",
        stamped: invoiceConfig.value.stamped || "",
        warehouseId: warehouse.value.id,
        invoiceNumber: currentSale.value.invoiceNumber.value,
        date: new Date().toISOString(),
        details: invoice.details.map((b) => {
          const product = getProductById(b.product)
          return {
            ...b,
            unitPrice:
              product.currentSalePrice.value === undefined ||
              product.currentSalePrice.value === null
                ? product.listPrice.value
                : product.currentSalePrice.value,
            // clientId: product.clientId,
          }
        }),
      }
    },
  })

  const invoiceManager = useGenericEntityList(invoices, options.value)

  const addInvoice = async (invoice) => {
    const { currentSale } = useSales()
    const { addVisit } = useVisits()
    const { selectedAddress } = useAddresses()
    const { currentPosition, positionError } = useLocation()
    // const { orders, setOrders } = useOrders()
    const { increaseInvoiceConfigActualNumber } = useSession()
    const existingInvoice = invoices.value.find(
      (i) => i.invoiceNumber === invoice.invoiceNumber
    )
    if (existingInvoice) return { data: existingInvoice }
    const invoiceResult = await invoiceManager.addInvoice(invoice)
    // On invoice created successfuly
    if (!invoiceResult.error) {
      currentSale.value.updateRealBatchesQuantity()
      increaseInvoiceConfigActualNumber()
      currentSale.value = invoiceResult.data
      // Add Visit
      const visitResult = await addVisit({
        customerAddress: selectedAddress.value.id,
        lat: currentPosition.value?.lat || "",
        lng: currentPosition.value?.lng || "",
        checkDate: new Date().toISOString(),
        visited: true,
        order: invoice.order,
        invoice: invoiceResult.data.id,
        invoiceNumber: currentSale.value.invoiceNumber.value,
      })
      // Update order
      // if (invoice.order && !visitResult.error) {
      //   setOrders(orders.value.map(o => o.id === invoice.order ? { ...o, visit: visitResult.data.id } : o))
      //   // const orderResult = await updateOrder({ id: invoice.order, deliveryDate: new Date().toISOString() })
      // }
    }
    return invoiceResult
  }
  const cancelInvoice = async (invoice) => {
    const { currentSale } = useSales()
    const { error } = await invoiceManager.updateInvoice({
      id: invoice.id,
      cancelled: true,
    })
    if (error) return
    currentSale.value.updateRealBatchesQuantity({ increase: true })
  }

  return {
    ...invoiceManager,
    showInvoicePreview,
    cancelInvoice,
    addInvoice,
  }
}
