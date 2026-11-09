<template>
  <transition
    enter-active-class="animated fadeInUp"
    leave-active-class="animated bounceOut"
  >
    <div v-if="synced" style="width:50px" class="flex flex-center">
      <q-icon class="text-white bg-green full-height q-pa-xs" name="check" size="18px" style="border-radius:100px" />
    </div>
  </transition>

  <q-btn v-if="showButton" flat class="bg-grey-1 text-primary" @click="syncEntity" style="width:50px;border:1px solid #ccc">
    <q-spinner-pie v-if="syncing" size="20px" />
    <q-icon v-else name="sync" />
    <q-tooltip v-if="!syncing">{{message || 'Sincronizar'}}</q-tooltip>
  </q-btn>
</template>

<script>
import { ref, toRefs } from 'vue'
import { useSession } from 'src/context'
import { useRouter } from 'vue-router'

export default {
  props: ["entityManager", 'message'],
  setup(props) {
    const { entityManager } = toRefs(props)
    const { logout } = useSession()
    const router = useRouter()
    const showButton = ref(true)
    const syncing = ref(false)
    const synced = ref(false)

    const syncEntity = async () => {
      if (syncing.value) return
      syncing.value = true
      const managers = [].concat(entityManager.value)
      await Promise.all(managers.map(manager => new Promise(async (resolve, reject) => {
        const { data, error } = await manager.loadEntity()
        if (error) {
          if (error?.response?.status && [401, 403].includes(error.response.status)) {
            logout()
            router.replace({ name: 'Login' })
          }
          reject(error)
        }
        else resolve(data)
      })))

      showButton.value = false
      synced.value = true
      setTimeout(() => {
        synced.value = false
        setTimeout(() => showButton.value = true, 500)
      }, 2000)
      syncing.value = false
    }

    return {
      synced,
      syncing,
      showButton,
      syncEntity,
    }
  },
}
</script>
