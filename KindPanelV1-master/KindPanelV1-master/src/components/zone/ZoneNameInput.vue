<template>
    <ItemNameInput
        :focus="focus"
        @update:focus="$emit('update:focus', $event)"

        :updateHandler="updateZone"

        :currentItem="currentItem"
        :selectedItem="selectedZone"

        alias="Ruta"
    />
</template>

<script>
import { computed, toRefs } from 'vue'
import ItemNameInput from 'src/components/includes/ItemNameInput'
import { useZones } from 'src/context'

export default {
    components: {ItemNameInput},
    props: ['focus', 'currentItem'],
    emits: ['update:focus'],
    setup(props) {
        const { focus, currentItem } = toRefs(props)
        const { updateZone, selectedZone } = useZones()

        return {
            focus,
            currentItem,
            selectedZone,
            updateZone,
        }
    },
}
</script>

<style scoped>

</style>
