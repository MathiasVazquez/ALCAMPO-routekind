import { useCustomerAddresses } from "./customerAddress.context"
import { useInvoiceConfigs } from "./invoiceConfig.context"
import { useConfirmModal } from "./confirmModal.context"
import { usePolygonPins } from "./polygonPin.context"
import { useSelectDate } from "./selectDate.context"
import { useWarehouses } from "./warehouse.context"
import { useCustomers } from "./customer.context"
import { useSettings } from "./settings.context"
import { usePlanning } from "./planning.context"
import { usePolygons } from "./polygon.context"
import { useMobiles } from "./mobile.context"
import { useOrders } from "./order.context"
import { useZones } from "./zone.context"
import { useVisits } from "./visit.context"
import { useUsers } from "./user.context"
import { useUI } from "./ui.context"
import { useProducts } from "./product.context"
import { useSession, authHeader } from "./session.context"
import { useRouter } from "vue-router"

const USE_DEV = false

export const BASE_URL = USE_DEV
  ? "http://127.0.0.1:8000/api/panelapi/"
  : "https://kind-server-3.probusinesspy.xyz/api/panelapi/"
// : "https://kind-server1.probusinesspy.xyz/api/panelapi/"
// : "https://zeus4.probusinesspy.xyz/api/panelapi/"
export const replaceArrElementByProp = (arr, elem, prop = "id") =>
  arr.map((a) => (a && elem && a[prop] === elem[prop] ? elem : a))
export const removeArrElementByProp = (arr, elem, prop = "id") =>
  arr.filter((a) => a && elem && a[prop] !== elem[prop])

const loadAllFromServer = async () => {
  const { logout } = useSession()
  const router = useRouter()

  return await Promise.all(
    [
      useCustomerAddresses,
      useUsers,
      useOrders,
      usePolygonPins,
      usePolygons,
      useZones,
      useVisits,
      useMobiles,
      usePlanning,
      useProducts,
      useWarehouses,
      useInvoiceConfigs,
    ].map(
      (useEntity) =>
        new Promise(async (resolve, reject) => {
          const { data, error } = await useEntity().manager.loadEntity()
          if (error) {
            if ([401, 403].includes(error.response.status)) {
              logout()
              router.replace({ name: "Login" })
            }
            reject(error)
          } else resolve(data)
        })
    )
  )
}

export const formatPolygonsJson = (_polygons) => {
  const { getPolygonPinById } = usePolygonPins()

  const polygons = (_polygons || []).filter((p) => p.isActive)

  return {
    type: "FeatureCollection",
    features: polygons.map((poly) => {
      return {
        type: "Feature",
        geometry: {
          type: "Polygon",
          coordinates: [
            poly
              ? poly.polygonPins.value.map((p) => {
                  return [p.lng, p.lat]
                })
              : [],
          ],
        },
        properties: poly,
      }
    }),
  }
}

export {
  loadAllFromServer,
  useCustomerAddresses,
  useInvoiceConfigs,
  useConfirmModal,
  usePolygonPins,
  useSelectDate,
  useWarehouses,
  useCustomers,
  useSettings,
  usePlanning,
  usePolygons,
  useProducts,
  useSession,
  useMobiles,
  useZones,
  useOrders,
  useVisits,
  useUsers,
  useUI,
  authHeader,
}
