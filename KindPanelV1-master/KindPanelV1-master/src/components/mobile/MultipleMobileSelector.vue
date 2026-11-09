<template>
  <div class="text-grey-8 text-caption">Móviles seleccionados</div>
  <q-select
    multiple
    use-chips
    borderless
    stack-label
    class="full-width"
    v-model="selectedMobileList"
    :options="options"
  >
    <template v-slot:selected-item="scope" class="q-mt-md">
      <q-chip removable
        @remove="scope.removeAtIndex(scope.index)"
        :tabindex="scope.tabindex"
        color="grey-2"
        text-color="grey-9"
        class="q-mx-sm"
      >
        {{ scope.opt.label }}
      </q-chip>
    </template>
  </q-select>
</template>

<script>
import { computed, ref } from 'vue'
import { useMobiles } from 'src/context'

export default {
  setup() {
    const { mobiles, selectedMobileList } = useMobiles()

    const options = computed(() => mobiles.value.map(m => { return { label: m.name, value: m.id } }))

    return {
      options,
      selectedMobileList,
    }
  }
}
</script>