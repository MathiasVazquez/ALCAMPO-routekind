<template>
    <div class="row justify-between q-pa-sm">
        <!-- DROPDOWN OPTIONS -->
        <div class="flex flex-center row">
            <q-btn-dropdown v-if="routes" flat :label="currentRouteName" align="left">
                <q-list>
                    <q-item v-for="route of routes" :key="route.id"
                        clickable v-close-popup @click="selectZone(route)"
                    >
                        <q-item-section avatar>
                            <q-avatar><q-icon v-if="selectedZone && route.id === selectedZone.id" name="check"/></q-avatar>
                        </q-item-section>
                        <q-item-section>
                            <q-item-label>{{route.name || `Ruta ${route.id}`}}</q-item-label>
                        </q-item-section>
                    </q-item>
                </q-list>
            </q-btn-dropdown>
        </div>
        <!-- FILTER BY DAYS -->
        <div class="flex flex-center">
            <q-btn flat round dense no-caps icon="o_filter_alt">
                <q-menu>
                    <q-list>
                        <q-item clickable @click="toggleAllSelected" class="bg-grey-2">
                            <q-item-section avatar>
                                <q-avatar><q-icon :name="allDaysSelected ? 'o_check_box' : 'check_box_outline_blank'"/></q-avatar>
                            </q-item-section>
                            <q-item-section>
                                Todos
                            </q-item-section>
                        </q-item>
                        <q-separator/>
                        <q-item v-for="day of days" :key="day.code"
                            clickable
                            @click="day.selected=!day.selected"
                            v-show="!day.holiday"
                        >
                            <q-item-section avatar>
                                <q-avatar><q-icon :name="day.selected ? 'o_check_box' : 'check_box_outline_blank'"/></q-avatar>
                            </q-item-section>
                            <q-item-section>
                                <q-item-label>{{day.name}}</q-item-label>
                            </q-item-section>
                        </q-item>
                    </q-list>
                </q-menu>
            </q-btn>
        </div>
    </div>
</template>

<script>
import { computed, ref } from 'vue'
import { weekDays } from 'src/utils/statics'
import { useZones } from 'src/context'

export default {
    setup() {
        const { selectZone, selectedZone, routes } = useZones()

        const currentRouteName = computed(_ => selectedZone.value ? selectedZone.value.name || `Ruta ${selectedZone.value.id}` : 'Seleccionar...')

        const days = ref(weekDays.map(d => { return { ...d, selected: true } }))
        const allDaysSelected = computed(_ => days.value.every(d => d.selected === true))
        const toggleAllSelected = _ => {
            const selected = allDaysSelected.value
            days.value.forEach(d => d.selected = !selected)
        }

        return {
            days,
            routes,
            selectZone,
            selectedZone,
            allDaysSelected,
            currentRouteName,
            toggleAllSelected,
        }
    },
}
</script>
