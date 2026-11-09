import { ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const invoiceConfigs = ref(store.get('invoiceConfigs', []))

export const useInvoiceConfigs = () => {
    const options = ref({
        entityName: 'invoiceConfigs',
        entityNameSingular: 'invoiceConfig',
        entityUrl: 'invoice/config/',
    })
    return useGenericEntityList(invoiceConfigs, options.value)
}