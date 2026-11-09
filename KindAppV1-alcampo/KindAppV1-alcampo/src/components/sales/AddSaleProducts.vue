<template>

  <!-- PRICE LIST -->

  <q-card-section class="column">
    <div class="row justify-between items-center text-overline q-px-xs">Lista de precios</div>
    <q-btn-dropdown align="left" flat class="q-pa-md q-my-sm bg-grey-3" auto-close>
      <template v-slot:label>
        <div class="text-left full-width">
          {{(selectedPriceList?.name || 'Seleccionar').toUpperCase()}}
        </div>
      </template>
      <q-list>
        <div v-for="priceList of priceLists" :key="priceList.id" >
          <q-item clickable @click="selectPriceList(priceList)" class="q-pa-md">
            <q-item-section>
              {{priceList.name}}
            </q-item-section>
          </q-item>
          <q-separator />
        </div>
      </q-list>
    </q-btn-dropdown>
  </q-card-section>

  <!-- PRODUCTS DETAILS -->

  <q-card-section class="column q-pa-none">
    <div class="row justify-between items-center q-px-md q-mx-xs text-overline">Productos</div>
    <div class="q-pt-sm q-px-md">
      <div class="rounded-borders overflow-hidden">
        <q-btn flat @click="showSelectProductModal=true"
          class="full-width bg-grey-3 q-px-md q-py-md"
        >
          <div class="row justify-between items-center full-width">
            <div>Agregar producto</div>
            <q-icon name="add" />
          </div>
        </q-btn>
      </div>
    </div>
    <!-- LIST OF PRODUCTS -->
    <q-list v-if="addedProducts">
      <q-item>
        <q-item-section>
          <q-item-label caption>
            {{addedProducts.length}} {{addedProducts.length === 1 ? 'producto agregado' : 'prodcutos agregados'}} a la lista
          </q-item-label>
        </q-item-section>
      </q-item>
      <AddSaleProductItem v-for="(product, index) of addedProducts" :key="product.id" :product="product" :index="index+1" />
    </q-list>
    <div v-else class="q-ma-md q-pa-xs text-subtitle2">
      <div class="q-pa-sm bg-red text-white rounded-borders text-weight-bold">No hay productos en la lista</div>
    </div>

  </q-card-section>

  <SelectProductBatchlessModal />
  <AddSaleProductModal v-model="showSelectProductModal" />
</template>

<script>
// import CurrentOrderAddProductModal from './CurrentOrderAddProductModal'
// import CurrentOrderProductItem from './CurrentOrderProductItem'
// import { usePrices, useProducts, useCurrentOrderPriceList, useCurrentOrderProducts, useCurrentOrder } from 'src/context'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { usePriceLists, useProducts, useSales } from 'src/context'
import AddSaleProductItem from 'src/components/sales/AddSaleProductItem'
import AddSaleProductModal from 'src/components/sales/AddSaleProductModal'
import SelectProductBatchlessModal from './selectors/SelectProductBatchlessModal'


export default {
  // components: {CurrentOrderAddProductModal, CurrentOrderProductItem},
  components: {AddSaleProductModal, AddSaleProductItem, SelectProductBatchlessModal},
  setup() {
    const router = useRouter()
    // PRICE LIST
    const { priceLists, selectedPriceList, selectPriceList } = usePriceLists()
    // ADDED PRODUCTS
    const { currentSale } = useSales()
    const { getProductById, products } = useProducts()
    const addedProducts = computed(() => products.value.filter(p => p.totalQuantityAdded.value > 0) /*{
      return currentSale.value.details.map(p => {
        return { ...getProductById(p.product), ...p }
      })
    }*/)
    // const { currentOrderPrices } = useCurrentOrderPriceList()
    // const { currentOrder } = useCurrentOrder()
    // // PRODUCTS
    // const { products } = useProducts()
    const showSelectProductModal = ref(false)
    // const search = ref('')

    return {
      // products,
      currentSale,
      priceLists,
      addedProducts,
      selectPriceList,
      selectedPriceList,

      // search,
      showSelectProductModal,
    }
  }
}
</script>
