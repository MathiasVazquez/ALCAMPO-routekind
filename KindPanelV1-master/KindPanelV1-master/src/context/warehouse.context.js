import { ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const warehouses = ref(store.get('warehouses', []))

export const useWarehouses = () => {
    const options = ref({
        entityName: 'warehouses',
        entityNameSingular: 'warehouse',
        entityUrl: 'warehouse/',
    })
    return useGenericEntityList(warehouses, options.value)
}