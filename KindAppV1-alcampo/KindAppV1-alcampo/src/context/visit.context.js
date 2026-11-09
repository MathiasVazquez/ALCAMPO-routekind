import { ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'
import { useLocation } from './location.context'

const visits = ref(store.get('visits', []))
const selectedVisit = ref(null)
const showAddVisitModal = ref(false)

export const useVisits = () => {
  const options = ref({
    entityName: 'visits',
    entityNameSingular: 'visit',
    entityUrl: 'visit/',
    selectedEntity: selectedVisit,
    canDeselectEntity: true,
    // localOnly: true,
    requestFormatter: visit => {
      const { currentPosition } = useLocation()
      return {
        ...visit,
        checkDate: visit.checkDate || new Date().toISOString(),
        lat: visit.lat || currentPosition.value?.lat || '',
        lng: visit.lng || currentPosition.value?.lng || '',
      }
    }
  })

  const getVisitsByAddressId = (id, list) => (list || visits.value).filter(v => `${v.customerAddress}` === `${id}`)
  const getVisitsByOrderId = (id, list) => (list || visits.value).filter(v => `${v.order}` === `${id}`)
  const getLastOrderVisitById = (id, list) => {
    const orderVisits = getVisitsByOrderId(id, list)
    if (orderVisits.length === 0) return null
    else if (orderVisits.length === 1) return orderVisits[0]
    else return orderVisits.reduce((result, v) => new Date(result.checkDate) > new Date(v.checkDate) ? result : v, orderVisits[0])
  }
  const getLastAddressVisitById = (id, list) => {
    const addressVisits = getVisitsByAddressId(id, list)
    if (addressVisits.length === 0) return null
    else if (addressVisits.length === 1) return addressVisits[0]
    else return addressVisits.reduce((result, v) => new Date(result.checkDate) > new Date(v.checkDate) ? result : v, addressVisits[0])
  }

  return {
    ...useGenericEntityList(visits, options.value),
    getLastAddressVisitById,
    getLastOrderVisitById,
    getVisitsByAddressId,
    getVisitsByOrderId,
    showAddVisitModal,
  }
}
