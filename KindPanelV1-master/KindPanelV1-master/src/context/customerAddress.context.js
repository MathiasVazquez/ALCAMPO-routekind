import { ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const addresses = ref(store.get('addresses', []))
const selectedAddress = ref(null)

export const useCustomerAddresses = () => {
  const options = ref({
    entityName: 'customerAddresses',
    entityNameSingular: 'customerAddress',
    entityUrl: 'customer/address/',
    selectedEntity: selectedAddress,
  })
  return useGenericEntityList(addresses, options.value)
}