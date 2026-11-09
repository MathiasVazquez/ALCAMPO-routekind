<template>
  <slot name="pre" :entity="entity" :selected="isSelected" :color="entityColor" />
  <q-item v-ripple clickable @click="selectEntity(entity)" class="basic-item"
    :class="[
      isSelected ? ['basic-item-selected', selectedClass]: unselectedClass,
      {'basic-item-outline': outline}
    ]"
    :style="isSelected ?
      (typeof selectedStyle === 'function' ? selectedStyle({color: entityColor}) : ( selectedStyle|| '')) :
      (typeof unselectedStyle === 'function' ? unselectedStyle({color: entityColor}) : ( unselectedStyle|| ''))"
  >
    <q-item-section avatar class="q-pa-none" style="min-width:45px">
      <GenericEntityAvatar :shortNameFilter="shortNameFilter" :entity="entity" :alias="alias" :color="entityColor">
        <template #before="{color}">
          <div v-if="isSelected" class="side-bar" :style="`background-color:${color}`"></div>
        </template>
      </GenericEntityAvatar>
    </q-item-section>
    <q-item-section>
      <slot name="upper" :entity="entity" :selected="isSelected" />
      <q-item-label title class="row q-gutter-x-sm items-center">
        <slot name="before" :entity="entity" :selected="isSelected" />
        <slot name="label" :entity="entity" :selected="isSelected">
          <div class="text-grey-7">
            {{alias}}
          </div>
        </slot>
      </q-item-label>
      <slot name="under" :entity="entity" :selected="isSelected" />
    </q-item-section>
    <slot name="final" :entity="entity" :selected="isSelected" />
  </q-item>
</template>

<script>
import { toRefs, ref, computed } from 'vue'
import { getRandomColor } from 'src/helpers'
import GenericEntityAvatar from './GenericEntityAvatar'

export default {
  props: ['entity', 'virtualSelected', 'unselectable', 'entityManager', 'alias', 'color', 'shortNameFilter', 'selectedStyle', 'unselectedStyle', 'selectedClass', 'unselectedClass', 'outline', 'cancelSelect'],
  emits: ['click'],
  components: {GenericEntityAvatar},
  setup(props, { emit }) {
    const { entity, unselectable, entityManager, alias, cancelSelect } = toRefs(props)
    const nameInputFocused = ref(false)

    const isSelected = computed(() => (selectedEntity.value && entity.value.id === selectedEntity.value.id) || props.virtualSelected)
    const selectedEntity = computed(() => !unselectable.value && entityManager.value.selectedEntity.value)
    const entityColor = computed(() => props.color || getRandomColor((entity.value?.id || entity.value?.clientId || '') + (alias.value || entity.value?.name)))

    const selectEntity = () => {
      emit('click', entity)
      if (unselectable.value) return
      if (cancelSelect.value && selectedEntity.value?.id === entity.value.id)
        entityManager.value.selectEntity(null)
      else entityManager.value.selectEntity(entity.value)
    }

    return {
      alias,
      entity,
      isSelected,
      entityColor,
      selectEntity,
      entityManager,
      selectedEntity,
      nameInputFocused,
    }
  },
}
</script>

<style scoped>
.side-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background-color: red;
  z-index: 10;
}
</style>
