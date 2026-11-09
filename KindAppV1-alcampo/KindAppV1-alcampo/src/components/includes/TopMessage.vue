<template>
  <transition 
    enter-active-class="animated bounce"
    leave-active-class="animated bounceOut"
  >
    <div v-if="topMessage"
      class="absolute-bottom row justify-center"
      style="z-index:99999"
      :style="`bottom:${topMessage.bottom}px`"
    >
      <div class="q-pa-sm q-mx-md rounded-borders text-white text-body1 row justify-between items-center no-wrap"
        style="max-width:360px" :class="topMessage.bgColor"
      >
        <div><strong>{{topMessage.text}}</strong></div>
        <q-btn flat round icon="close" @click="closeMessage" />
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useUI } from 'src/context'

export default {
  setup() {
    const { topMessage, closeMessage } = useUI()

    return {
      topMessage,
      closeMessage,
    }
  },
}
</script>