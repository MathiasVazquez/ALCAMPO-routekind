<template>
  <q-list>
    <slot name="initList" />
    <q-item v-for="mobile of mobiles" :key="mobile.id"
      clickable v-close-popup @click="preventSelection?$emit('select', mobile):selectMobile(mobile)"
    >
      <q-item-section avatar v-if="!hideCheck">
        <q-avatar><q-icon v-if="mobile.id === selectedMobile.id" name="check"/></q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label>{{mobile.name}}</q-item-label>
      </q-item-section>
    </q-item>
    <slot name="endList" />
  </q-list>
</template>

<script>
import { ref } from 'vue'
import { useMobiles } from 'src/context'

export default {
	name: 'MainLayout',
  props: ['preventSelection', 'hideCheck'],
  emits: ['select'],
	setup () {
		const { selectMobile, mobiles, selectedMobile } = useMobiles()
		const expandedMenu = ref(false)

		return {
			mobiles,
			expandedMenu,
			selectedMobile,
			selectMobile,
		}
	}
}
</script>

