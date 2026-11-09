<template>
  <TopMessage />
    <ConfirmModal />
    <router-view />
</template>

<script>
import { watch } from 'vue'
import { useRouter } from 'vue-router'
import { useSession, useLocation, mustCloseSession } from 'src/context'
import TopMessage from 'src/components/includes/TopMessage'
import ConfirmModal from 'src/components/includes/ConfirmModal'

export default {
  components: {TopMessage, ConfirmModal},
  setup() {
    const { startWatchLocation } = useLocation()
    const { isLogged } = useSession()
    const router = useRouter()

    watch(mustCloseSession, () => {
      if (mustCloseSession.value) {
        router.replace({ name: 'Login' })
      }
    })

    const onCreate = () => {
      if (isLogged.value) startWatchLocation()
      else router.replace('/login')
    }
    onCreate()
    watch(isLogged, onCreate)
  },
}
</script>


