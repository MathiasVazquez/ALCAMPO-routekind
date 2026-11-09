<template>
  <router-view />
  <TopMessage />
  <ConfirmModal />
  <!--<SelectDateModal />-->
</template>
<script>
import { defineComponent, watch } from 'vue'
import { loadAllFromServer, useSession } from 'src/context'
import { useLocation } from 'src/helpers'
import { useRouter } from 'vue-router'
import TopMessage from 'src/components/includes/TopMessage'
import ConfirmModal from 'src/components/includes/ConfirmModal'
import SelectDateModal from 'src/components/includes/SelectDateModal'

export default defineComponent({
  name: 'App',
  components: {TopMessage, ConfirmModal, SelectDateModal},
  setup() {
    const { startWatchLocation } = useLocation()
    const { isLogged } = useSession()
    const router = useRouter()

    const onCreate = () => {
      if (isLogged.value) {
        loadAllFromServer()
        startWatchLocation()
      }
      else router.replace('/login')
    }
    onCreate()
    watch(isLogged, onCreate)
  },
})
</script>
