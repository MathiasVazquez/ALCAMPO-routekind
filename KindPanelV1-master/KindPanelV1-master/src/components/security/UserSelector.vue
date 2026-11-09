<template>
    <q-list v-if="avaibleUsers.length > 0">
        <q-item v-for="user of avaibleUsers" :key="user.id"
            clickable class="q-pa-md column"
            @click="handleAssignUser(user)"
        >
            <q-item-section>
                <q-item-label>{{user.name}} {{user.lastName}}</q-item-label>
                <q-item-label caption>{{user.username}}</q-item-label>
            </q-item-section>
        </q-item>
    </q-list>
    <q-item v-else style="max-width:300px" class="bg-grey-2">
        <q-item-section>
            <q-item-label>No quedan usuarios disponibles para asignar</q-item-label>
            <q-item-label caption>Al parecer, todos los usuarios ya están asignados, pero siempre puedes crear un nuevo usuario.</q-item-label>
        </q-item-section>
    </q-item>
</template>

<script>
import { computed, ref } from 'vue';
import EmptyListFace from 'src/components/includes/EmptyListFace'
import CreateUserModal from 'src/components/mobileUser/CreateUserModal'
import { useMobiles, useUsers } from 'src/context'

export default {
    components: {EmptyListFace, CreateUserModal},
    setup() {
        const showCreateUserModal = ref(false)
        const { mobiles, selectedMobile, updateMobile } = useMobiles()

        const { users, getUserById } = useUsers()

        const user = computed(() => getUserById(selectedMobile.value?.user))
        const avaibleUsers = computed(() => users.value.filter(u => u.isMobileUser && !mobiles.value.some(m => m.user == u.id)))

        const handleAssignUser = async user => await updateMobile({ id: selectedMobile.value.id, user: user?.id || null })

        return {
            user,
            users,
            avaibleUsers,
            selectedMobile,
            showCreateUserModal,
            handleAssignUser,
        }
    },
}
</script>