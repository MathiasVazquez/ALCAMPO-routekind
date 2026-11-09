import { useRouter } from "vue-router"
import { useUI } from "./ui.context"
import { useSales } from "./sale.context"
import { useVisits } from "./visit.context"
import { useOrders } from "./order.context"
import { useBatches } from "./batch.context"
import { useInvoices } from "./invoice.context"
import { useProducts } from "./product.context"
import { useLocation } from "./location.context"
import { useSettings } from "./settings.context"
import { useAddresses } from "./address.context"
import { usePriceLists } from "./priceList.context"
import { usePaymentTypes } from "./paymentType.context"
import { useConfirmModal } from "./confirmModal.context"
import { useSession, authHeader } from "./session.context"
import {
  mustCloseSession,
  validateResponse,
} from "src/context/generics/listEntity.generic"

const USE_DEV = false

export const BASE_URL = USE_DEV
  ? "http://localhost:8000/api/appapi/"
  : "https://kind-server1.probusinesspy.xyz/api/appapi/"
//: "https://kind-server-3.probusinesspy.xyz/api/appapi/"
// "https://test3.probusinesspy.xyz/api/v1/appapi/"

const getFromServerEntities = () => [
  useAddresses,
  useOrders,
  usePriceLists,
  useProducts,
  useBatches,
  useInvoices,
  usePaymentTypes,
  useVisits,
]

const clearAllMemory = () =>
  getFromServerEntities().forEach(
    (useEntity) => (useEntity().manager.entityList.value = [])
  )

const loadAllFromServer = async (profile = true) => {
  const { loadProfile } = useSession()

  if (profile) {
    const profileResult = await loadProfile()
    if (!validateResponse(profileResult.error)) return
  }

  const loadEntity = (useEntity) =>
    new Promise(async (resolve, reject) => {
      const { data, error } = await useEntity().manager.loadEntity()
      if (error) reject(error)
      else resolve(data)
    })

  return await Promise.all(getFromServerEntities().map(loadEntity))
}

export {
  loadAllFromServer,
  useConfirmModal,
  usePaymentTypes,
  clearAllMemory,
  usePriceLists,
  useAddresses,
  useLocation,
  useSettings,
  useProducts,
  useInvoices,
  useBatches,
  useSession,
  useOrders,
  useVisits,
  useSales,
  useUI,
  authHeader,
  mustCloseSession,
}
