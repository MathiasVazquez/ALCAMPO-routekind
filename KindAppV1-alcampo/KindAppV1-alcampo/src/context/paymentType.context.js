import { ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const paymentTypes = ref(store.get('paymentTypes', []))
const selectedPaymentType = ref(null)

export const usePaymentTypes = () => {
  const options = ref({
    entityName: 'paymentTypes',
    entityNameSingular: 'paymentType',
    entityUrl: 'payment/payment-type/',
    selectedEntity: selectedPaymentType,
  })
  return useGenericEntityList(paymentTypes, options.value)
}
