import { ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const priceLists = ref(store.get('priceLists', []))
const selectedPriceList = ref(null)

export const usePriceLists = () => {
  const options = ref({
    entityName: 'priceLists',
    entityNameSingular: 'priceList',
    entityUrl: 'product/price-list/',
    selectedEntity: selectedPriceList
  })
  return useGenericEntityList(priceLists, options.value)
}
