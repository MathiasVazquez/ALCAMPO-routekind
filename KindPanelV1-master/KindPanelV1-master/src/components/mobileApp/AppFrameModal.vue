<template>
  <q-dialog v-model="showAppFrame">
    <q-card class="mobile-app-view">
      <iframe src="https://app.probusinesspy.xyz" frameborder="0" class="full-height"
        style="overflow:hidden;min-height:calc(90vh - 7px);min-width:400px" />
    </q-card>
  </q-dialog>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useUI } from 'src/context'

export default {
  setup(props) {
    const { showAppFrame } = useUI()
    watch(showAppFrame, () => console.log('2. showAppFrame'))

    return {
      showAppFrame,
    }
  },
}
</script>

<style scoped>
.mobile-app-view {
  min-width: 400px;
  max-width: 400px;
  min-height: 90vh;
  max-height: 90vh;
}
</style>
