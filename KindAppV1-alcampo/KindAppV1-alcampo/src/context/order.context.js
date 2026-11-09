import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'
import { useAddresses, useSales, useProducts, useVisits, useInvoices } from 'src/context'

const orders = ref(store.get('orders', []))
const selectedOrder = ref(null)
const showOrderDetailsModal = ref(false)

export const useOrders = () => {
  const { showInvoicePreview } = useInvoices()

  const formatter = order => {
    const { visits, getLastOrderVisitById } = useVisits()
    const lastVisit = computed(() => visits.value && getLastOrderVisitById(order.id))
    return {
      ...order,
      hasVisit: computed(() => !!lastVisit.value),
      hasDelivered: computed(() => lastVisit.value?.visited),
    }
  }

  const options = ref({
    entityName: 'orders',
    entityNameSingular: 'order',
    entityUrl: 'order/',
    selectedEntity: selectedOrder,
    formatter,
  })

  const sortedOrders = computed(() => {
    const firstOrder = orders.value.find(o => o.isFirstOrder)
    const result = []

    let currentOrder = firstOrder
    while(currentOrder) {
      result.push(currentOrder)
      currentOrder = currentOrder.nextOrder ? orders.value.find(o => o.id === currentOrder.nextOrder) : null
    }

    return result.concat(orders.value.filter(o => !result.includes(o))).map(o => formatter(o))
  })

  const getOrdersByAddressId = addressId => addressId ? orders.value.filter(o => o.customerAddress.id === addressId).map(o => formatter(o)) : []
  const convertOrderToCurrentSale = (order, openModal=true) => {
    // const { getAddressById } = useAddresses()
    const { getProductById } = useProducts()
    const { currentSale, showAddSaleModal } = useSales()
    const { customer, description } = order.customerAddress // getAddressById(order.customerAddress)
    const totalToPay = order.details.reduce((sum, d) => sum + d.quantity * d.unitPrice, 0)
    // SET CURRENT SALE PROPS
    currentSale.value = {
      order: order.id,
      orderClientId: order.clientId,
      paymentTerm: order.paymentTerm,
      // INVOICE DETAILS
      invoiceNumber: order.invoiceNumber || '',
      // CUSTOMER
      customer: customer.id,
      customerFiscalName: customer.fiscalName || `${customer.firstName ? customer.firstName + " " : ""}${customer.lastName}`,
      customerDocument: customer.document,
      customerPhone: customer.mobilePrimary,
      customerAddress: description,
      // PRICE LIST
      priceList: null,
      // SALE CONDITION AND PAYMENTS
      saleCondition: order.saleCondition, // Contado, Crédito
      payments: order.paymentType ? [{
        name: order.paymentType,
        amount: totalToPay,
      }] : [],
      // PRODUCTS
      details: []
    }

    // SET CURRENT SALE PRODUCTS
    for (const detail of order.details) {
      getProductById(detail.product).addQuantity(detail.quantity, { unitPrice: detail.unitPrice })
    }

    if (openModal) showAddSaleModal.value = true
  }
  const convertOrderToInvoice = (order) => {
    convertOrderToCurrentSale(order, false)
    showInvoicePreview.value = true
  }

  return {
    sortedOrders,
    showOrderDetailsModal,
    convertOrderToCurrentSale,
    convertOrderToInvoice,
    getOrdersByAddressId,
    ...useGenericEntityList(orders, options.value),
  }
}
