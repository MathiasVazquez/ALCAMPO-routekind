<template>
    <q-dialog :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)"
        transition-show="rotate" transition-hide="rotate" persistent
    >
        <q-card>
            <q-card-section>
                <div class="row justify-between items-center no-wrap">
                    <div class="text-body1 text-grey-8">
                        ({{direction.id}}) Modificar freciencia de visita del cliente <strong>{{direction.customer.firstName}} {{direction.customer.lastName}}</strong> en la zona <strong>{{selectedZone.name || `Ruta ${selectedZone.id}`}}</strong>
                    </div>
                    <q-btn flat round icon="close" @click="$emit('update:modelValue', false)" />
                </div>
            </q-card-section>

            <q-separator />

            <!-- SELECTOR -->
            <q-card-section style="max-height:65vh;max-width:100%" class="scroll">
                <q-btn-dropdown no-caps outline auto-close class="full-width">
                    <q-list v-for="frecuency of frecuencyOptions" :key="frecuency.id">
                        <q-item clickable @click="selectedFrecuency=frecuency">
                            <q-item-section>
                                <div class="column full-width">
                                    <div class="row text-body1 text-weight-bold">{{frecuency.name}}</div>
                                    <div class="row text-caption" style="max-width:500px">{{frecuency.description}}</div>
                                </div>
                            </q-item-section>
                        </q-item>
                    </q-list>
                    <template #label>
                        <div class="column full-width" style="max-width:500px">
                            <div class="row text-body1 text-weight-bold">{{selectedFrecuency.name}}</div>
                        </div>
                    </template>
                </q-btn-dropdown>

                <div class="text-caption q-pa-sm">
                    {{selectedFrecuency.description}}
                </div>

                <!-- CASES -->

                <div v-if="selectedFrecuency.id === 1" class="row">
                    <ZoneDaysList :route="selectedZone" :canRemove="false" />
                </div>
                <div v-else-if="selectedFrecuency.id === 2">
                    <q-input outlined v-model="selectedFrecuency.data.date" type="date" label="Seleccionar día" />
                </div>
                <div v-else-if="selectedFrecuency.id === 3">
                    <q-select
                        label="Ingrese el día y presione Enter"
                        outlined
                        v-model="selectedFrecuency.data.monthDays"
                        use-input
                        use-chips
                        multiple
                        hide-dropdown-icon
                        input-debounce="0"
                        new-value-mode="add-unique"
                        style="width: 250px"
                        class="full-width"
                    />
                    <div class="q-mt-xs text-caption q-px-xs">
                        Obs: Para seleccionar el último día del mes, ingrese '-1', para seleccionar el penultimo día del mes, ingrese '-2', y así sucesivamente
                    </div>
                </div>
                <div v-else-if="selectedFrecuency.id === 4" class="q-gutter-y-xs">
                    <q-input outlined v-model="selectedFrecuency.data.startDate" type="date" label="Fecha de inicio" />
                    <div v-for="(week, index) of selectedFrecuency.data.weekDays" :key="index" class="row items-center">
                        <q-select
                            class="row"
                            style="flex-grow:1"
                            outlined
                            multiple
                            use-chips
                            stack-label
                            v-model="selectedFrecuency.data.weekDays[index]"
                            :options="selectedFrecuency.options"
                            :label="`Semana ${index+1}`"
                        />
                        <q-btn v-if="selectedFrecuency.data.weekDays.length > 2" flat round icon="close"
                            @click="selectedFrecuency.data.weekDays.splice(index, 1)"
                        >
                            <q-tooltip>Remover semana {{index + 1}}</q-tooltip>
                        </q-btn>
                    </div>
                    <div class="row full-width justify-end">
                        <q-btn outline no-caps class="row items-end" icon="add"
                            @click="selectedFrecuency.data.weekDays = [...selectedFrecuency.data.weekDays, []]"
                        >
                            Agregar otra semana
                        </q-btn>
                    </div>
                </div>
            </q-card-section>

            <!-- FOOTER -->
            <q-separator />
            <q-card-actions align="right">
                <!--<q-btn flat no-caps>Cancelar</q-btn>-->
                <q-btn unelevated no-caps color="primary" @click="saveFrequency">Guardar</q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { ref, toRefs, computed, watch, onMounted } from 'vue'
import { useZones } from 'src/context'
import { formatToDatePicker } from 'src/helpers'
import CustomerItem from 'src/components/customer/CustomerItem'
import ItemOptionsBtn from 'src/components/includes/ItemOptionsBtn'
import ZoneDaysList from 'src/components/zone/ZoneDaysList'
import { weekDays } from 'src/utils/statics'


export default {
    name: 'AddCustomerToRouteModal',
    components: {CustomerItem, ItemOptionsBtn, ZoneDaysList},
    props: ['modelValue', 'direction'],
    emits: ['update:modelValue'],
    setup(props, { emit }) {
        const { modelValue, direction } = toRefs(props)
        const { selectedZone, addRouteCustomerFrequency, getRouteCustomerFrequency } = useZones()

        const frecuencyOptions = ref([{
            id: 1,
            name: 'Frecuencia normal',
            description: 'Los días de la semana definidos por la zona.',
        }, {
            id: 2,
            name: 'Un día específico',
            description: 'Solo un día en específico que se considerará una única vez.',
            data: {
                date: formatToDatePicker(new Date()),
            }
        }, {
            id: 3,
            name: 'Distribución mensual',
            description: 'Uno o varios días específicos del mes. Por ejemplo, el 8 y el 24 de cada mes.',
            data: {
                monthDays: [],
            }
        }, {
            id: 4,
            name: 'Distribución semanal en el mes',
            description: 'Uno o varios días específicos de las semanas del mes. Por ejemplo, el lunes de la primera semana y el jueves de la tercera semana.',
            options: weekDays.map(w => w.name),
            data: {
                startDate: formatToDatePicker(new Date()),
                weekDays: [[], []],
            }
        }])

        const selectedFrecuency = ref(frecuencyOptions.value[0]) // TODO: SET THE CURRENT ROUTE FRECUENCY AS DEFAULT
        const setSelectedFrequency = () => {
            if (!direction.value) return
            const frequency = getRouteCustomerFrequency(direction.value)
            if (frequency) {
                const result = frecuencyOptions.value.find(f => `${f.id}` == `${frequency.frequencyType}`)
                selectedFrecuency.value = {
                    ...result,
                    data: JSON.parse(frequency.frequencyData)
                }
            }
        }

        const saveFrequency = async () => {
            const { error } = await addRouteCustomerFrequency(direction.value, selectedFrecuency.value.id, selectedFrecuency.value.data)
            if (error) {

            }
            else {
                emit('update:modelValue', false)
            }
        }

        watch(direction, setSelectedFrequency)
        onMounted(setSelectedFrequency)

        return {
            direction,
            modelValue,
            selectedZone,
            frecuencyOptions,
            selectedFrecuency,
            setSelectedFrequency,
            saveFrequency,
        }
    },
}
</script>
