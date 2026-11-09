import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const customers = ref(store.get('customers', []))
const selectedCustomer = ref(null)

export const useCustomers = () => {

  // const customersAddresses = computed(() => {
  //   const directions = []
  //   for (let customer of customers.value) {
  //     for (let direction of customer.directions) {
  //       try {
  //         directions.push({ ...direction, customer,
  //           lat: direction.lat ? parseFloat(direction.lat) : null,
  //           lng: direction.lng ? parseFloat(direction.lng) : null
  //         })
  //       }
  //       catch (error) {}
  //     }
  //     // directions.push({ customer, description: "", lat: null, lng: null })
  //   }
  //   return directions
  // })

  const options = ref({
    entityName: 'customers',
    entityNameSingular: 'customer',
    entityUrl: 'customer/',
    selectedEntity: selectedCustomer,
    canDeselectEntity: true,
    formatter: customer => customer ? { ...customer, fullName: `${customer.firstName || ''} ${customer.lastName || ''}`, } : null
  })

  return {
    ...useGenericEntityList(customers, options.value)
  }
}
