import { ref, computed } from 'vue'
import { formatMoney } from 'src/helpers'
import {
  formatWords,
  getSpaces,
  getSeparator,
  getBetween,
  ESC_ALIGN_CENTER,
  ESC_ALIGN_LEFT
} from "src/helpers/printer.helper"
import {
  useProducts,
  useSession,
  useSales,
  useOrders
} from 'src/context'

export const footerLine = ref("")

export const linesToPrint = computed(() => {
  const { orders } = useOrders()
  const { products } = useProducts()
  const { currentSale } = useSales()
  const { invoiceConfig, company } = useSession()

  // debugger
  const saleOrder = orders.value.find((order) => order.id === currentSale.value.order || order.clientId === currentSale.value.orderClientId)
  const paymentTerm = currentSale.value.paymentTerm || saleOrder?.paymentTerm
  const purchaseOrderNumber =
  saleOrder?.purchaseOrderNumber ??
  saleOrder?.purchase_order_number ??
  ''
  const newLine = (line, align) => formatWords(line).map(line => {return { text: line, align: align || ESC_ALIGN_LEFT }})

  // const date = new Date();
  // const currentDate = `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`

  // let totalIva5 = 0
  // let totalIva10 = 0
  let total0 = 0
  let total5 = 0
  let total10 = 0
  const currentSaleProducts = products.value.filter(p => p.totalQuantityAdded.value > 0)

  const productListLines = currentSaleProducts.reduce((result, product) => {
    const productPrice = product.currentSalePrice.value === undefined ? product.listPrice.value : product.currentSalePrice.value
    const productTotalNum = productPrice * product.totalQuantityAdded.value
    const productTotal = formatMoney(`${productTotalNum}`)
    const detailsPrice = formatMoney(`${productPrice}`)
    const priceSpace = getSpaces(19 - detailsPrice.length - productTotal.length)
    const price_total = detailsPrice + priceSpace + productTotal
    const iva_qty = `${product.taxPercentage}%  ${product.totalQuantityAdded.value}${getSpaces(6 - (product.totalQuantityAdded.value + "").length)}`
    const lineResult = result.concat([...newLine(product.productName), ...newLine(`${iva_qty}${price_total}`)])
    if (product.taxPercentage === 10) total10 += productTotalNum
    else if (product.taxPercentage === 5) total5 += productTotalNum
    else total0 += productTotalNum
    return lineResult
  }, [])

  const totalIva5 = parseInt(total5 / 21)
  const totalIva10 = parseInt(total10 / 11)

  const paymentLines = currentSale.value.payments.reduce((result, payment) => {
    const r = result.concat(newLine(getBetween(payment.name, formatMoney(payment.amount))))
    // console.log('result:', r)
    return r
  }, [])

  const formatDate = date => {
    const _d = new Date(date)
    return `${_d.getDate()}/${_d.getMonth()+1}/${_d.getFullYear()}`
  }

  const isCredit = currentSale.value.saleCondition !== "Contado"

  // debugger
  return [
    ...newLine(company.value.name, ESC_ALIGN_CENTER),
    ...newLine(`RUC: ${company.value.fiscalNumber}`, ESC_ALIGN_CENTER),
    ...newLine(`${company.value.address}`, ESC_ALIGN_CENTER),
    ...newLine(`${company.value.city} - ${company.value.country}`, ESC_ALIGN_CENTER),
    ...newLine(`Tel: ${company.value.phone}`, ESC_ALIGN_CENTER),
    ...newLine(`Timbrado Nro ${invoiceConfig.value.stamped}`, ESC_ALIGN_CENTER),
    ...newLine(`Valido Desde ${formatDate(invoiceConfig.value.startDate)}`, ESC_ALIGN_CENTER),
    ...newLine(`Valido Hasta ${formatDate(invoiceConfig.value.dueDate)}`, ESC_ALIGN_CENTER),

    ...newLine(getSeparator()),

    ...newLine(`Fact. Nro.: ${currentSale.value.invoiceNumber.value}`),
    ...(saleOrder ? newLine(`Nro remisión: ${saleOrder.orderNumber}`) : []),
    ...(purchaseOrderNumber
  ? newLine(`Orden Compra: ${purchaseOrderNumber}`)
  : []),
    ...newLine(`Cond. Venta: ${paymentTerm || currentSale.value.saleCondition}`),
    ...newLine(`Fecha: ${formatDate(new Date())}`),
    ...newLine(`Cliente: ${currentSale.value.customerDocument ? currentSale.value.customerFiscalName : "OCASIONAL"}`),
    ...newLine(`RUC: ${currentSale.value.customerDocument || "44444401-7"}`),
    ...(currentSale.value.customerAddress ? newLine("Direccion: " + currentSale.value.customerAddress) : []),
    ...(currentSale.value.customerPhone ? newLine("Telef: " + currentSale.value.customerPhone) : []),

    ...newLine(getSeparator()),
    ...newLine("Imp. Cant. P. Unit.      Total"),
    ...newLine(getSeparator()),
    ...productListLines,

    ...(isCredit ? [] : newLine(getSeparator('--'))),
    ...(isCredit ? [] : newLine("MEDIOS DE COBRO", ESC_ALIGN_CENTER)),
    ...(isCredit ? [] : newLine("Tipo   Nro    Banco    Importe")),
    ...(isCredit ? [] : paymentLines),

    ...newLine(getSeparator('--')),
    ...newLine(getBetween('TOTAL GENERAL', formatMoney(currentSale.value.totalToPay.value))),
    ...newLine(getBetween('TOTAL A PAGAR', formatMoney(currentSale.value.totalToPay.value))),

    ...newLine(getSeparator('--')),
    ...newLine(getBetween('TOTAL EXCENTAS', '0')),
    ...newLine(getBetween('TOTAL GRABADAS 10%', formatMoney(total10))),
    ...newLine(getBetween('TOTAL GRABADAS 5%', formatMoney(total5))),

    ...newLine(getSeparator('--')),
    ...newLine('LIQUIDACION IVA'),
    ...newLine(getBetween('Total IVA 10%', formatMoney(totalIva10))),
    ...newLine(getBetween('TOTAL IVA 5%', formatMoney(totalIva5))),
    ...newLine(getBetween('Total IVA', formatMoney(totalIva10 + totalIva5))),

    ...newLine(getSeparator('--')),
    ...newLine('*** GRACIAS POR SU COMPRA ***', ESC_ALIGN_CENTER),
    ...(footerLine.value ? newLine(footerLine.value) : []),
  ]
})
