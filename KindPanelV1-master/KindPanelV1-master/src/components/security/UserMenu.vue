<template>
  <div class="column q-gutter-y-md flex flex-center full-width q-py-md">
    <q-avatar icon="o_person" size="70px" class="bg-grey-2" />
    <div>@{{user.username}}</div>
    <div class="text-weight-bold text-h6">{{user.company.name}}</div>
    <q-item clickable @click="handleLogout" class="bg-red-8 rounded-borders text-white text-weight-bold">
      <q-item-section avatar>
        <q-avatar icon="logout" />
      </q-item-section>
      <q-item-section>
        CERRAR SESIÓN
      </q-item-section>
    </q-item>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useSession } from 'src/context'

export default {
  props: ['hideMapOptions'],
  setup() {
    const { logout, user } = useSession()
    const router = useRouter()

    const handleLogout = () => {
      logout()
      router.push({ name: 'Login' })
    }

    return {
      user,
      handleLogout,
    }
  },
}
</script>
