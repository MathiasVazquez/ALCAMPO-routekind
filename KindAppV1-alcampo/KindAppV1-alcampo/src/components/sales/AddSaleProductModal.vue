<template>
  <q-dialog
    :modelValue="modelValue"
    @update:modelValue="$emit('update:modelValue', $event)"
    position="bottom"
  >
    <q-card style="width:350px">
      <q-card-section class="no-wrap q-pa-sm column">
        <div class="row items-center no-wrap">
          <q-input v-model="search" borderless class="full-width bg-grey-3 q-px-md" label="Buscar producto...">
            <template v-slot:prepend>
              <q-btn flat round dense icon="arrow_back" class="q-mr-sm" @click="$emit('update:modelValue', false)" />
            </template>
            <template v-slot:append>
              <q-btn v-if="search" flat round icon="close" @click="search=''" />
            </template>
          </q-input>
        </div>
        <div class="q-px-sm q-pt-sm text-grey-8 text-subtitle2 text-right">
          {{filteredProducts.length}} {{filteredProducts.length===1?`producto ${search?'filtrado':'disponible'}`:`productos ${search?'filtrados':'disponibles'}`}}
        </div>

      </q-card-section>
      <q-separator />
      <q-card-section class="q-pa-none">
        <q-scroll-area style="height:60vh;">
          <q-list>
            <AddSaleProductItem v-for="(product, index) of filteredProducts" :key="product.id" :product="product" :index="index+1" />
          </q-list>
        </q-scroll-area>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { toRefs, ref, computed } from 'vue'
import { useProducts } from 'src/context'
// import { useProducts, useCurrentOrderProductDetails } from 'src/context'
import AddSaleProductItem from './AddSaleProductItem'

export default {
  components: {AddSaleProductItem},
  props: ['modelValue'],
  emits: ['update:modelValue'],
  setup() {
    const search = ref('')

    const { products } = useProducts()

    const filteredProducts = computed(() =>  products.value
        .filter(p => p.totalQuantityAdded.value === 0 && p.productName && p.productName.toLowerCase().includes(search.value.toLowerCase()))
      /*.reduce((result, p) => {
        const { totalQuantityAvaible } = useCurrentOrderProductDetails(p)
        return totalQuantityAvaible.value > 0 && p.price ? [p, ...result] : [...result, p]
      }, [])*/
    )

    return {
      search,
      filteredProducts
    }
  },
}
</script>
