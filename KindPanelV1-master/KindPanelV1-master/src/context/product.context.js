import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'

const products = ref(store.get('products', []))
const selectedProduct = ref(null)

export const useProducts = () => {

  const options = ref({
    entityName: 'products',
    entityNameSingular: 'product',
    entityUrl: 'product/',
    selectedEntity: selectedProduct,
  })

  return useGenericEntityList(products, options.value)
}
