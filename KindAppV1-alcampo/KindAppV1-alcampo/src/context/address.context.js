import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { useVisits } from 'src/context'
import { useGenericEntityList } from './generics/listEntity.generic'

const addresses = ref(store.get('addresses', []))
const selectedAddress = ref(null)

export const useAddresses = () => {
  const options = ref({
    entityName: 'addresses',
    entityNameSingular: 'address',
    entityUrl: 'customer/address/',
    selectedEntity: selectedAddress,
    formatter: address => {
      if (!address) return null
      const { visits, getLastAddressVisitById } = useVisits()
      const visit = computed(() => getLastAddressVisitById(address.id, visits.value))
      return {
        ...address,
        hasVisit: computed(() => !!visit.value),
        showInMap: computed(() => !visit.value || (!visit.value.visted && visit.value.visitLater)),
        visitLater: computed(() => !!visit.value && !visit.value.visited && visit.value.visitLater),
        customer: {
          ...address.customer,
          // fiscalName: address.customer ? address.customer.fiscalName || `${address.customer.firstName ? address.customer.firstName + ' ' : ''}${address.customer.lastName}` : '',
          fullName: `${address.customer?.firstName ? address.customer.firstName + ' ' : ''}${address.customer?.lastName || ''}` || 'Sin nombre'
        }
      }
    }
  })
  return useGenericEntityList(addresses, options.value)
}
