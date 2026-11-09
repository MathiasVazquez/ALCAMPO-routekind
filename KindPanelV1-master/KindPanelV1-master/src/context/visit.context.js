import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'
import { useMobiles, useSettings } from 'src/context'
import { sameDate, formatFromDatePicker } from 'src/helpers'

const visits = ref(store.get('visits', []))
const selectedVisit = ref(null)

export const useVisits = () => {
  const { orderDateFilter } = useSettings()
  const { selectedMobileList, getMobileById } = useMobiles()

  const options = ref({
    entityName: 'visits',
    entityNameSingular: 'visit',
    entityUrl: 'visit/',
    selectedEntity: selectedVisit,
    deselectOnSelfSelection: true,
    canDeselectEntity: true,
    formatter: visit => {
      const confirmed = computed(() => visits.value && visit.visited)
      const skiped = computed(() => visits.value && !confirmed.value && !visit.visitLater)
      const visible = computed(() =>
        selectedMobileList.value.some(m => m.value === visit.mobile) &&
        sameDate(visit.checkDate, orderDateFilter.value)
      )
      const color = computed(() => confirmed.value ? 'green' : skiped.value ? 'red' : visit.visitLater ? 'purple' : 'black')
      const stateLabel = computed(() => confirmed.value ? 'Concretado' : skiped.value ? 'No concretado' : visit.visitLater ? 'Volver más tarde' : 'Indefinido')
      return {
        ...visit,
        color,
        skiped,
        visible,
        confirmed,
        stateLabel,
      }
    }
  })

  const manager = useGenericEntityList(visits, options.value)

  const sortVisits = visits => visits.sort((v1, v2) => {
    const v1Date = new Date(v1.checkDate)
    const v2Date = new Date(v2.checkDate)
    return v1Date < v2Date ? 1 : v1Date > v2Date ? -1 : 0
  })

  const visitsGroupByMobile = computed(() => {
    const result = {}
    manager.visits.value
      .filter(v => v.visible.value)
      .forEach(v => {
        const mobile = getMobileById(v.mobile)
        const viist = { ...v, mobile }
        if (!result[v.mobile]) result[v.mobile] = [viist]
        else result[v.mobile].push(viist)
      })
    // Sort order group elements
    const sortedResilt = {}
    for (const group in result)
      sortedResilt[group] = sortVisits(result[group])
    return sortedResilt
  })

  const getVisitsByAddressId = (id, list) => (list || manager.visits.value).filter(v => `${v.customerAddress}` === `${id}`)
  const getVisitsByOrderId = (id, list) => (list || manager.visits.value).filter(v => `${v.order}` === `${id}`)
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
    sortVisits,
    getLastOrderVisitById,
    getLastAddressVisitById,
    visitsGroupByMobile,
    ...manager,
  }
}
