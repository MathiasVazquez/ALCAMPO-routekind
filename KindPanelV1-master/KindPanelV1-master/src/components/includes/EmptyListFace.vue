<template>
  <!--q-pa-md flex flex-center column q-gutter-y-md bg-grey-3 q-ma-sm-->
  <div
    class="flex flex-center page-section-item column q-gutter-y-md bg-grey-3 text-grey-8 page-section-item"
  >
    <!--<div v-for="face of faces" :key="face" class="text-h4">{{face}}</div>-->
    <!-- <div class="text-h4">{{getRandomFace()}}</div> -->
    <q-icon size="42px" color="grey-6" name="o_live_help" />
    <div class="text-center" style="max-width: 200px"><slot /></div>
    <q-btn v-if="label" color="primary" @click="$emit('click', $event)">
      {{ label }}
    </q-btn>
    <slot name="footer" />
  </div>
</template>

<script>
import { getRandomFace, faces } from "src/utils/statics";
import { toRefs } from "vue";

export default {
  props: ["label"],
  emits: ["click"],
  setup(props) {
    const { label } = toRefs(props);

    return {
      faces,
      label,
      getRandomFace,
    };
  },
};
</script>
