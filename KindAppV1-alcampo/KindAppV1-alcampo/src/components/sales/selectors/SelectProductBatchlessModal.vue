<template>
  <q-dialog v-model="showDetails">
    <q-card>
      <q-card-section>
        <div class="row items-center justify-between">
          <div class="text-h6 text-grey-9">{{selectedProduct.productName}}</div>
        </div>
      </q-card-section>

      <q-separator />

      <q-card-section style="max-height: 50vh" class="scroll column no-wrap">
        <div class="row justify-between items-center">
          <div v-if="selectedProduct.trackInventory" class="column q-mr-md">
            <div class="text-caption">Cantidad disponible</div>
            <div class="text-h6" style="margin-top:-8px">{{selectedProduct.totalQuantityAvaible.value}}</div>
          </div>
          <div v-else class="column q-mr-md">
            <div class="text-caption">Seleccionar cantidad</div>
          </div>
          <div class="row items-center justify-end q-mx-sm q-my-xs">
            <q-btn round outline dense icon="remove" @click="selectedProduct.addQuantity(-1)" />
            <q-item-label class="q-pa-md">{{selectedProduct.totalQuantityAdded.value}}</q-item-label>
            <q-btn round outline dense icon="add" @click="selectedProduct.addQuantity(1)" />
          </div>
        </div>
      </q-card-section>

      <!-- COMPOSED ITEM INFO -->
      <q-separator v-if="selectedProduct.isComposed" />
      <q-card-section v-if="selectedProduct.isComposed">
        <div class="text-caption text-grey-8 q-mb-xsq">Cada unidad de este producto incluye</div>
        <div v-for="item of selectedProduct.items" :key="item.id" class="column">
          <div>x{{item.unitQuantity}} {{getProductById(item.product).productName}}</div>
        </div>
      </q-card-section>

      <!-- ADVANCE SETTINGS -->
      <q-separator v-if="showAdvancedSettings" />
      <q-slide-transition>
        <div v-if="showAdvancedSettings">
          <q-card-section>
            <div><strong>Advanced settings on!</strong></div>
            <div class="text-caption text-grey-8">Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore tenetur quaerat beatae. Error vel quas rem harum. Porro temporibus soluta quam velit accusantium ex excepturi culpa. Praesentium repudiandae ipsa labore!</div>
          </q-card-section>
        </div>
      </q-slide-transition>

      <!-- BOTTOM OPTIONS -->
      <q-separator />
      <q-card-actions>
        <div class="row items-center full-width">
          <!-- <q-btn round flat icon="o_tune" :class="showAdvancedSettings ? 'bg-primary text-white' : 'text-grey-8'"
            @click="showAdvancedSettings=!showAdvancedSettings"
          /> -->
          <q-btn v-if="selectedProduct.totalQuantityAdded.value>0"
            flat round color="red-7" icon="o_delete"
            @click="selectedProduct.removeAllQuantity"
          />
          <q-space />
          <q-btn flat label="Finalizar" color="primary" v-close-popup />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, toRefs, computed, watch } from 'vue'
import { formatMoney } from 'src/helpers'
import { useProducts } from 'src/context'
// import { useCurrentOrderProductDetails, useProducts } from 'src/context'
// import CurrentOrderProductItemBatches from '../CurrentOrderProductItemBatches'

export default {
  // components: {CurrentOrderProductItemBatches},
  setup() {
    const { selectedProduct, selectProduct, getProductById } = useProducts()

    const productPriced = computed(() => !!selectedProduct.value.listPrice.value || !!selectedProduct.value.currentSalePrice.value)
    const canSelectedProduct = computed(() =>
      !!selectedProduct.value &&
      !!productPriced.value &&
      (
        selectedProduct.value.totalQuantity.value > 0 ||
        !selectedProduct.value.trackInventory
      )
    )
    const showAdvancedSettings = ref(false)

    const showDetails = computed({
      get: () => canSelectedProduct.value,
      set: value => { if (!value) selectProduct(null) }
    })

    // const {
    //   totalQuantityAvaible,
    //   coProductQuantity,
    //   hasStockInCurrentOrder,
    //   removeProductFromCurrentOrder,
    // } = useCurrentOrderProductDetails(product.value)

    // const { getProductById } = useProducts()

    const handeRemoveProduct = () => {}

    return {
      showDetails,
      selectedProduct,
      showAdvancedSettings,
      // product,
      // totalQuantityAvaible,
      // hasStockInCurrentOrder,
      // handeRemoveProduct,
      // coProductQuantity,
      // formatMoney,
      getProductById,
    }
  },
}
</script>
