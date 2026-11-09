<template>
    <q-scroll-area 
        class="full-height"
        style="margin-left:50px"
    >
        <PlanningList />
    </q-scroll-area>
</template>

<script>
import PlanningList from 'src/components/planning/PlanningList'

export default {
    components: {PlanningList},
    setup() {
        
    },
}
</script>