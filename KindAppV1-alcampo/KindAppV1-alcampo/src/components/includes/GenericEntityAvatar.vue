<template>
  <slot name="before" :color="entityColor" :shortName="entityShortName" />
  <q-avatar :size="size || '35px'" :style="`background-color:${entityColor}`" text-color="grey-1 text-weight-light">
    {{entityShortName}}
  </q-avatar>
</template>

<script>
import { toRefs, computed } from 'vue'
import { getRandomColor } from 'src/helpers'

export default {
  props: ['shortNameFilter', 'entity', 'alias', 'color', 'size'],
  emits: ['ready'],
  setup(props, { emit }) {
    const { entity, alias, color } = toRefs(props)

    const aliasedName = computed(() => alias.value ? `${alias.value}${entity.value ? ' ' + entity.value.id : '---'}` : entity.value?.name || '---')
    const entityShortName = computed(() => (props.shortNameFilter ? props.shortNameFilter(entity.value) : `${aliasedName.value[0]}${(aliasedName.value.split(" ")[1] || "")[0] || aliasedName.value[1]}`).toUpperCase())
    const entityColor = computed(() => color.value || getRandomColor((entity.value?.id || entity.value?.clientId || '') + (aliasedName.value || entity.value?.name || entityShortName.value)))

    emit('ready', { entityColor, entityShortName, aliasedName })

    return {
      entityColor,
      entityShortName,
    }
  },
}
</script>
