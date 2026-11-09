<template>
    <q-item clickable
        class="rounded-borders q-ma-xs q-pr-none q-pl-sm q-py-sm"
        style="border:1px solid #ddd"
    >
        <q-item-section>
            <q-item-label caption>
                {{customer.document}}
            </q-item-label>
            <q-item-label caption class="text-weight-bold">
                <strong>{{customer.firstName}} {{customer.lastName}}</strong>
            </q-item-label>
            <q-item-label caption>
                {{direction.description}}
            </q-item-label>
            <q-item-label caption v-if="hasCoords">
                ({{direction.lat}}, {{direction.lng}})
            </q-item-label>
            <q-item-label v-else class="row q-mb-xs">
                <div class="q-px-xs rounded-borders bg-red text-white text-caption">Sin coordenadas</div>
            </q-item-label>
            <slot />
        </q-item-section>
        <q-item-section side style="min-width:0;padding:0">
            <slot name="side" />
        </q-item-section>
    </q-item>
</template>

<script>
import { toRefs, ref, computed } from 'vue'

export default {
    props: ['customer', 'direction'],
    setup(props) {
        const { customer, direction } = toRefs(props)
        // const directionDisabled = ref(direction.value.disabled)
        const hasCoords = computed(() => direction.value && direction.value.lng && direction.value.lat)

        return {
            customer,
            direction,
            hasCoords,
        }
    },
}
</script>