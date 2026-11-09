<template>
  <q-card class="bg-white column no-wrap shadow-0">
    <q-card-section
      class="column no-wrap items-center full-width text-weight-bold scroll"
      style="height:calc(100vh - 106px)"
    >
      <div class="column bg-grey-3 q-pa-md" style="margin-bottom:60px">
        <div v-for="(line, index) of linesToPrint" :key="index" class="full-width"
          style="font-family:monospace;margin-button:-20px;max-width:280px;overflow:hidden"
          :class="{'text-center': line.align === ESC_ALIGN_CENTER}"
        >
          <pre style="margin:0;word-break:break-word">{{line.text}}</pre>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { ESC_ALIGN_CENTER } from "src/helpers/printer.helper"
import { computed, toRefs, ref } from 'vue'
import { linesToPrint } from 'src/helpers'
import { useSales } from 'src/context'

export default {
  props: ['name'],
  setup(props) {
    const { name } = toRefs(props)
    const { currentSale } = useSales()

    const sending = ref(false)
    const printing = ref(false)
    const printers = ref(null)
    const printersFormated = computed(() => printers.value ? JSON.stringify(printers.value) : '')

    return {
      currentSale,
      name,
      sending,
      printing,
      linesToPrint,
      printersFormated,
      ESC_ALIGN_CENTER,
    }
  },
}
</script>

<style scoped>
.print-button {
  position: absolute;
  z-index: 1000;
  bottom: 0;
  margin: 20px 0;
  left: 50%;
  transform: translateX(-50%);
}
.header-container {
  position: absolute;
  top: 0;
}
</style>
