<template>
    <q-scroll-area 
        class="full-height"
        style="margin-left:50px"
    >
        <MobileList/>
    </q-scroll-area>
</template>

<script>
import MobileList from 'src/components/mobile/MobileList'

export default {
    components: {MobileList},
    setup() {
        
    },
}
</script>

<style scoped>
.mobile-list-scroll-area {

}
</style>