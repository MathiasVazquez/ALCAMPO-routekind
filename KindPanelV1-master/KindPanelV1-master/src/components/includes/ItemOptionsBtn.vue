<template>
    <q-btn flat :round="!label" dense no-caps size="11px" 
        :icon="icon || 'more_vert'" :label="label"
        :class="{'q-pr-xs': label}"
    >
        <q-tooltip v-if="!hideTooltip">{{tooltip || 'Más opciones'}}</q-tooltip>
        <q-menu auto-close>
            <q-list>
                <q-item clickable
                    v-for="option of options" 
                    :key="option.text" 
                    @click="option.onClick"
                    v-show="!option.hidden"
                >
                    <q-item-section v-if="option.icon" avatar><q-avatar :icon="option.icon" /></q-item-section>
                    <q-item-section><q-item-label>{{option.text}}</q-item-label></q-item-section>
                </q-item>
            </q-list>
        </q-menu>
    </q-btn>
</template>

<script>
import { toRefs } from 'vue';

export default {
    props: ['options', 'label', 'icon', 'tooltip', 'hide-tooltip'],
    setup(props) {
        const { options, label, icon, tooltip, hideTooltip } = toRefs(props)
        return { label, options, icon, tooltip, hideTooltip }
    },
}
</script>