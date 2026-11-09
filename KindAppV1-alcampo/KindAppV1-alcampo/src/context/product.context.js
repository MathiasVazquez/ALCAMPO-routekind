import { computed, ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'
import { useBatches, useSales, usePriceLists } from 'src/context'

const products = ref(store.get('products', []))
const selectedProduct = ref(null)

export const useProducts = () => {

  const options = ref({
    entityName: 'products',
    entityNameSingular: 'product',
    entityUrl: 'product/',
    selectedEntity: selectedProduct,
    canDeselectEntity: true,
    formatter: product => {
      const { currentSale } = useSales()
      const { getBatchesByProductId } = useBatches()
      const { selectedPriceList } = usePriceLists()

      const productBatches = computed(() => getBatchesByProductId(product.id))
      const totalQuantity = computed(() => productBatches.value.reduce((sum, b) => sum + parseInt(b.quantity), 0))
      const totalQuantityAdded = computed(() => currentSale.value.details.filter(b => b.product === product.id)?.reduce((sum, b) => sum + b.quantity, 0) || 0)
      const totalQuantityAvaible = computed(() => totalQuantity.value - totalQuantityAdded.value)
      const listPrice = computed(() => selectedPriceList.value.details.find(d => d.product === product.id)?.unitPrice)
      const currentSalePrice = computed(() => currentSale.value.details.find(b => b.product === product.id)?.unitPrice)
      const addQuantityFromBatch = (deltaQuantity, batch, { unitPrice } = {}) => {
        const batchInCurrentSale = currentSale.value.details.find(d => d.batch === batch.id)
        const nextQuantity = Math.max(0, !!batchInCurrentSale ? batchInCurrentSale.quantity + deltaQuantity : deltaQuantity)
        currentSale.value = {
          ...currentSale.value,
          details:
            nextQuantity === 0 ? currentSale.value.details.filter(d => d.batch !== batch.id) :
            !!batchInCurrentSale ? currentSale.value.details.map(d => d.batch === batch.id ? { ...d, quantity: nextQuantity } : d) :
            [...currentSale.value.details, { batch: batch.id, product: batch.product || product.id, quantity: nextQuantity, unitPrice }]
        }
      }
      const addQuantityToProduct = (deltaQuantity, { unitPrice } = {}) => {
        const detail = currentSale.value.details.find(d => d.product === product.id)
        const nextQuantity = Math.max(0, (detail?.quantity || 0) + deltaQuantity)
        currentSale.value = {
          ...currentSale.value,
          details:
            nextQuantity === 0 ? currentSale.value.details.filter(d => d.product !== product.id) :
            !!detail ? currentSale.value.details.map(d => d.product === product.id ? { ...d, quantity: nextQuantity } : d) :
            [...currentSale.value.details, { batch: undefined, product: product.id, quantity: nextQuantity, unitPrice }]
        }
      }
      const addQuantity = (deltaQuantity, options) => {
        if (!product.trackInventory) return addQuantityToProduct(deltaQuantity, options)
        for (let index = 0; index < Math.abs(deltaQuantity); index++) {
          const batch = productBatches.value.find(b => deltaQuantity > 0 ? b.avaibleQuantity.value > 0 : b.avaibleQuantity.value < b.quantity)
          if (!batch) return
          addQuantityFromBatch(deltaQuantity > 0 ? 1 : -1, batch, options)
        }
      }
      const removeAllQuantity = () => {
        const batchesInCurrentSale = currentSale.value.details.filter(d => d.product === product.id).map(d => d.batch)
        currentSale.value = {
          ...currentSale.value,
          details: currentSale.value.details.filter(b => !batchesInCurrentSale.includes(b.batch))
        }
      }
      return {
        ...product,
        listPrice,
        totalQuantity,
        currentSalePrice,
        totalQuantityAdded,
        totalQuantityAvaible,
        isComposed: product.items?.length > 0,
        removeAllQuantity,
        addQuantity,
      }
    }
  })

  return useGenericEntityList(products, options.value)
}
