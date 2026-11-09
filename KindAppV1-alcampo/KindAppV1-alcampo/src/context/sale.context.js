import { ref, computed } from "vue"
import { useSession, useProducts, useBatches } from "src/context"

const defaultCurrentSale = computed(() => {
  return {
    // INVOICE DETAILS
    invoiceNumber: "",
    // CUSTOMER
    customer: null,
    customerFiscalName: "",
    customerDocument: "",
    customerPhone: "",
    customerAddress: "",
    // PRICE LIST
    priceList: 1,
    // SALE CONDITION AND PAYMENTS
    saleCondition: "Contado", // Contado, Crédito
    paymentTerm: "",
    payments: [
      {
        name: "Efectivo",
        amount: 0,
      },
    ],
    // PRODUCT
    details: [
      /*{
      batch: 1,
      product: 1,
      quantity: 10,
      // unitPrice: 10000,
    }, {
      batch: 3,
      product: 2,
      quantity: 20,
      // unitPrice: 20000,
    }*/
    ],
  }
})

const showAddSaleModal = ref(false)
const currentSale = ref(defaultCurrentSale.value)

export const useSales = () => {
  const { invoiceConfig } = useSession()
  const { getProductById } = useProducts()
  const { unformatBatches, setBatches } = useBatches()

  const clearCurrentSale = () => (currentSale.value = defaultCurrentSale.value)

  const addPayment = (payment) => {
    currentSale.value = {
      ...currentSale.value,
      payments: [...currentSale.value.payments, payment],
    }
  }
  const updatePayment = (index, update) => {
    currentSale.value = {
      ...currentSale.value,
      payments: currentSale.value.payments.map((p, i) =>
        `${i}` === `${index}` ? { ...p, ...update } : p
      ),
    }
  }
  const removePayment = (index) => {
    currentSale.value = {
      ...currentSale.value,
      payments: currentSale.value.payments.filter(
        (_, i) => `${i}` !== `${index}`
      ),
    }
  }
  const updateRealBatchesQuantity = ({ increase } = { increase: false }) => {
    setBatches(
      [...unformatBatches.value].map((b) => {
        const detail = currentSale.value.details.find((d) => d.batch === b.id)
        return detail
          ? {
              ...b,
              quantity: b.quantity + detail.quantity * (increase ? 1 : -1),
            }
          : b
      })
    )
  }

  const totalPayed = computed(
    () =>
      currentSale.value.payments.reduce(
        (sum, p) => sum + parseFloat(p.amount),
        0
      ) || 0
  )
  const totalToPay = computed(
    () =>
      currentSale.value.details.reduce((sum, d) => {
        const product = getProductById(d.product)
        const price =
          product.currentSalePrice.value === undefined
            ? product.listPrice.value
            : product.currentSalePrice.value
        return sum + d.quantity * price
      }, 0) || 0
  )
  const totalNotPayed = computed(() => totalToPay.value - totalPayed.value)
  const isValidSale = computed(
    () => totalToPay.value > 0 && totalNotPayed.value === 0
  )
  const invoiceNumber = computed(
    () =>
      currentSale.value.invoiceNumber ||
      `${invoiceConfig.value.serialNumber}-${invoiceConfig.value.actualNumber
        .toString()
        .padStart(7, "0")}`
  )

  return {
    currentSale: computed({
      get: () => {
        return {
          ...currentSale.value,
          _currentSale: currentSale.value,
          totalPayed,
          totalToPay,
          isValidSale,
          totalNotPayed,
          invoiceNumber,
          updateRealBatchesQuantity,
          clear: clearCurrentSale,
          updatePayment,
          removePayment,
          addPayment,
        }
      },
      set: (value) => {
        const _value = { ...value }
        delete _value._currentSale
        delete _value.totalPayed
        delete _value.totalToPay
        delete _value.isValidSale
        delete _value.totalNotPayed
        if (typeof _value.invoiceNumber !== "string")
          delete _value.invoiceNumber
        delete _value.clear
        delete _value.updatePayment
        delete _value.removePayment
        delete _value.addPayment
        currentSale.value = _value
      },
    }),
    showAddSaleModal,
    defaultCurrentSale,
    clearCurrentSale,
  }
}
