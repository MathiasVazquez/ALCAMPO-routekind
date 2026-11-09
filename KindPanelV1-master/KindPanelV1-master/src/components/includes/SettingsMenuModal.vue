<template>
  <q-dialog v-model="showSettingsMenu">
    <q-card>
      <q-card-section class="row items-center q-pa-none">
        <EditableMapOptionsMenu />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script>
import { toRefs } from 'vue'
import { useSettings } from 'src/context'
import EditableMapOptionsMenu from 'src/components/map/EditableMapOptionsMenu'

export default {
  components: {EditableMapOptionsMenu},
  setup(props) {
    const { showSettingsMenu } = useSettings()

    return {
      showSettingsMenu
    }
  },
}
</script>
