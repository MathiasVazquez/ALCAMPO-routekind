<template>
  <div class="content" :style="`bottom:${displacement}px;height:${height}px`">
    <div><slot name="top" /></div>
    <div class="container full-height scroll">
      <!-- HEADER -->
      <div ref="contentHeader" class="content-header column" v-touch-pan.prevent.mouse="handlePan">
        <div class="flex flex-center"><div class="content-header-bar" /></div>
        <slot name="header" />
      </div>
      <!-- BODY -->
      <div class="content-body scroll" :style="`height:calc(${height}px - ${headerHeight}px - 50px)`">
        <slot name="body" />
      </div>
      <q-separator />
    </div>
  </div>
</template>

<script>
import { ref, toRefs, watch, computed, nextTick } from 'vue'

export default {
  components: {},
  props: {
    height: {type: Number, default: 400},
    minHeight: {type: Number, default: 100},
    modelValue: {type: Boolean, default: false},
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const { height, minHeight, modelValue } = toRefs(props)

    const contentHeader = ref(null)
    const headerHeight = ref(0)
    const flex = ref(20)

    watch([contentHeader, modelValue], async () => {
      await nextTick()
      headerHeight.value = contentHeader.value.offsetHeight
    })

    const closedPosition = computed(_ => minHeight.value + flex.value - height.value)
    const displacement = ref(modelValue.value ? 0 : closedPosition.value)

    const closeDrawer = () => displacement.value = closedPosition.value
    const openDrawer = () => displacement.value = 0

    const handlePan = ({ evt, ...newInfo }) => {
      const next = displacement.value - newInfo.delta.y
      if (-next < height.value - minHeight.value)
        displacement.value = Math.min(next, 0)

      if (newInfo.isFirst) { }
      else if (newInfo.isFinal) {
        const mg = minHeight.value + flex.value
        const mid = (height.value - mg) / 2
        if (-displacement.value > mid) {
          // CLOSED
          closeDrawer()
          emit('update:modelValue', false)
        }
        else {
          // OPENED
          openDrawer()
          emit('update:modelValue', true)
        }
      }
    }

    watch(modelValue, () => {
      if (modelValue.value) openDrawer()
      else closeDrawer()
    })

    return {
      height,
      minHeight,
      headerHeight,
      displacement,
      contentHeader,
      handlePan,
    }
  },
}
</script>

<style scoped>
.content {
  position: absolute;
  bottom: 0;
  width: 100%;
  overflow: hidden;
  z-index: 1000;
}
.container {
  z-index: 1000;
  border-top: 1px solid #ccc;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  box-shadow: 0 0 10px 5px #0002;
  background-color: #fff;
}
.content-header {
  width: 100%;
  padding: 10px 0;
  overflow: hidden;
}
.content-header-bar {
  width: 50px;
  height: 7px;
  border-radius: 5px;
  background-color: #aaa;
}
.content-body {
  overflow: auto;
}
</style>
