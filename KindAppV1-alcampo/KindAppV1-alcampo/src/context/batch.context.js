import { computed, ref } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'
import { useSales } from './sale.context'

const batches = ref(store.get('batches', []))
const selectedBatch = ref(null)

export const useBatches = () => {

  const formatter = batch => {
    const { currentSale } = useSales()
    return {
      ...batch,
      avaibleQuantity: computed(() => {
        const addedQuantity = currentSale.value.details.find(d => d.batch === batch.id)?.quantity || 0
        return batch.quantity - addedQuantity
      })
    }
  }

  const options = ref({
    entityName: 'batches',
    entityNameSingular: 'batch',
    entityUrl: 'product/batch/',
    selectedEntity: selectedBatch,
    formatter,
  })
  return {
    ...useGenericEntityList(batches, options.value),
    getBatchesByProductId: productId => batches.value.filter(b => b.product === productId).map(b => formatter(b)),
  }
}
