<template>
    <ItemNameInput         
        :focus="focus"
        @update:focus="$emit('update:focus', $event)"

        :updateHandler="updatePolygon"

        :currentItem="currentItem"
        :selectedItem="selectedPolygon"

        alias="Figura"
    />
</template>

<script>
import { computed, toRefs } from 'vue'
import ItemNameInput from 'src/components/includes/ItemNameInput'
import { usePolygons } from 'src/context'

export default {
    components: {ItemNameInput},
    props: ['focus', 'currentItem'],
    emits: ['update:focus'],
    setup(props) {
        const { focus, currentItem } = toRefs(props)
        const { updatePolygon, selectedPolygon } = usePolygons()

        return {
            focus,
            currentItem,
            selectedPolygon,
            updatePolygon,
        }
    },
}
</script>

<style scoped>

</style>