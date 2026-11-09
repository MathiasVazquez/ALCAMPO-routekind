<template>
    <q-scroll-area 
        class="full-height"
        style="margin-left:50px"
    >
        <UserList/>
    </q-scroll-area>
</template>

<script>
import UserList from 'src/components/security/UserList'

export default {
    nqme: 'SecurityDrawerContent',
    components: {UserList},
    setup() {
        
    },
}
</script>