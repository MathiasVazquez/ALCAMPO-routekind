<template>
  <div>
    <div class="border-grey border-round acenter gshadow bg-grey-2" :style="`width:${bw}px;height:${bh}px`">
      <div class="border-grey border-round acenter bg-white" :style="`width:${bw*0.92}px;height:${bh*0.8}px;margin-bottom:${bh*0.1}px`">
        <q-icon name="verified_user" style="position:absolute;color:#ccca;margin-right:2px;margin-top:2px" :size="`${bw*0.34}px`"/>
        <q-icon name="verified_user" style="position:absolute" :size="`${bw*0.3}px`" color="primary"/>
      </div>
    </div>
    <div class="row justify-center">
      <div class="border-h-grey bg-grey-2" :style="`height:${bw*0.05}px;width:${bh*0.25}px`"></div>
    </div>
    <div class="row justify-center">
      <div class="border-grey border-round gshadow bg-grey-2" :style="`height:${bw*0.05}px;width:${bh*0.33}px;`"></div>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, toRefs, computed } from 'vue'

export default defineComponent({
  name: 'LoginImg',
  props: ['scale'],
  setup(props) {
    const { scale } = toRefs(props);
    const bw_1 = ref(220.0);
    const bh_1 = ref(160.0);
    const bw = computed(() => bw_1.value * scale.value);
    const bh = computed(() => bh_1.value * scale.value);

    return { bw, bh }
  },
})
</script>

<style scoped>
.border-grey, .border-h-grey {
  border-right: 3px solid #888;
  border-left: 3px solid #888;
}
.border-grey, .border-v-grey {
  border-top: 3px solid #888;
  border-bottom: 3px solid #888;
}
.border-round {
  border-radius: 5px;
}
.acenter {
  display: flex;
  justify-content: center;
  align-items: center;
}
.gshadow {
  box-shadow: -3px 0 2px 2px #ddd;
}
</style>
