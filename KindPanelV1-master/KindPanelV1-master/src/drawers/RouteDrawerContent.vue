<template>
    <!-- MOBILE USER SETTINGS -->
    <!--<div
        class="absolute-top drawer-header column"
        style="margin-left:50px"
    >
        <SelectedMobileInfo />
        <q-space/>
        <q-separator/>
    </div>-->

    <!-- POLYGON LIST -->
    <q-scroll-area
        class="full-height"
        style="margin-left:50px"
    >
        <ZoneList/>
    </q-scroll-area>
</template>

<script>
import SelectedMobileInfo from 'src/components/mobileUser/SelectedMobileInfo'
import ZoneList from 'src/components/zone/ZoneList'

export default {
    components: {SelectedMobileInfo, ZoneList},
    setup() {

    },
}
</script>

<style scoped>
.polygon-list-scroll-area {
	height:calc(100% - 121px);
	margin-top:121px;
}
</style>
