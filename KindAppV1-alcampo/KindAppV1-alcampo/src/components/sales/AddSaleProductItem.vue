<template>
  <q-item class="q-pa-md q-mx-sm" clickable @click="showDetails">
    <q-item-section v-if="false" avatar class="q-pa-none q-ma-none" style="min-width:40px">
      <q-avatar round class="bg-grey-2 text-grey-8" size="28px">{{index || ''}}</q-avatar>
    </q-item-section>
    <q-item-section>
      <!-- HEADER -->
      <div class="row items-center justify-between no-wrap">
        <q-item-label><strong>{{product.productName}}</strong></q-item-label>
      </div>
      <!-- NO PRICE ERROR MESSAGE -->
      <div v-if="!productPriced" class="q-mt-sm">
        <q-badge
          color="red" style="font-size:14px" class="q-pa-sm text-weight-bold"
          label="No disponible en la lista de precios" />
      </div>
      <!-- NO STOCK ERROR MESSAGE -->
      <div v-else-if="!product.totalQuantity.value && product.trackInventory" class="q-mt-sm">
        <q-badge
          color="red" style="font-size:14px" class="q-pa-sm text-weight-bold"
          label="No hay stock disponible" />
      </div>
      <!-- CASE: PRODUCT ALREADY ADDED -->
      <div v-else-if="product.totalQuantityAdded.value > 0 && productPriced"
        class="row justify-between row items-center no-wrap text-subtitle2 text-grey-8 q-mt-sm"
      >
        <div class="row items-center">
          <div class="q-px-sm rounded-borders full-height q-mr-sm flex flex-center"
            style="border:1px solid #888;min-height:30px"
          >
            {{product.totalQuantityAdded.value}}
          </div>
          <div class="q-mr-sm">x</div>
          <div class="q-px-sm rounded-borders full-height q-mr-sm flex flex-center"
            style="border:1px solid #888;min-height:30px"
          >
            {{formatMoney(product.currentSalePrice.value || product.listPrice.value)}} c/u
          </div>
        </div>
        <!--<div class="q-mr-sm">=</div>-->
        <q-badge color="primary" style="font-size:15px" class="q-pa-sm"
          :label="`= ${formatMoney((product.currentSalePrice.value || product.listPrice.value) * product.totalQuantityAdded.value)} Gs.`"
        />
      </div>
      <!-- CASE: PRODUCT NOT ADDED -->
      <div v-else class="row items-center text-subtitle2 text-grey-8 q-mt-sm">
        <div v-if="product.trackInventory">{{product.totalQuantityAvaible.value}} {{product.totalQuantityAvaible.value===1?'disponible':'disponibles'}}</div>
        <q-space />
        <q-badge
          color="primary"
          class="q-pa-sm"
          style="font-size:15px"
          :label="`${formatMoney(product.listPrice.value)} Gs. c/u`"
        />
      </div>
    </q-item-section>
    <!-- REMOVE FROM LIST -->
    <!-- <q-item-section side v-if="!productIsAvaible && product.totalQuantityAdded.value">
      <q-btn flat round icon="o_delete" color="red" class="bg-grey-2" @click="handeRemoveProduct" />
    </q-item-section> -->
    <!-- PRODUCT BATCHES -->
    <!--<q-dialog v-model="showDetails">

      <CurrentOrderProductComposedItem v-if="product.isComposed" :product="product" />
      <CurrentOrderProductRegularItem v-else :product="product" />
      <CurrentOrderProductBatchless :product="product" />
    </q-dialog>-->
  </q-item>
  <q-separator></q-separator>
</template>

<script>
import { ref, toRefs, computed, watch } from 'vue'
import { formatMoney } from 'src/helpers'
import { useProducts } from 'src/context'
import SelectProductBatchlessModal from './selectors/SelectProductBatchlessModal'

export default {
  components: {SelectProductBatchlessModal},
  props: ['product', 'index'],
  setup(props) {
    const { product } = toRefs(props)
    const { selectProduct } = useProducts()

    const productPriced = computed(() => !!product.value.listPrice.value || !!product.value.currentSalePrice.value)
    const productIsAvaible = computed(() => productPriced.value && product.value.totalQuantity.value > 0)

    const handeRemoveProduct = e => {
      e.stopPropagation()
      product.value.removeAllQuantity()
    }

    const showDetails = () => {
      if (productIsAvaible.value || !product.value.trackInventory) {
        selectProduct(product.value)
      }
    }

    return {
      product,
      productPriced,
      productIsAvaible,
      handeRemoveProduct,
      showDetails,
      formatMoney,
    }
  },
}
</script>
