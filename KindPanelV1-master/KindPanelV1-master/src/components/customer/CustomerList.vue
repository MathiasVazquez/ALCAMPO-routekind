<template>
    <AddCustomerToZoneModal v-model="showAddCustomerModal" />
    <UpdateCustomerZoneFrecuency v-model="showUpdateRouteFrecuency" :direction="updateDirection" />

    <q-list class="text-black">
        <!-- IN POLYGON CUSTOMERS -->
        <q-item class="q-pa-none column">
            <q-item-section>
                <q-item-label header overline class="bg-grey-2">
                    <div class="row justify-between items-center">
                        <div>CLIENTES ({{customersDirection.length}})</div>
                        <div class="row">
                            <q-btn flat rounded dense no-caps icon="add"
                                 @click="showAddCustomerModal=true"
                            >
                                <q-tooltip>Agregar cliente a la ruta</q-tooltip>
                            </q-btn>
                        </div>
                    </div>
                </q-item-label>
            </q-item-section>
        </q-item>
        <q-separator/>

        <EmptyListFace
            v-if="customersDirection.length === 0"
            @click="showAddCustomerModal=true"
            label="Agregar cliente"
        >
            <div>Parece que no hay ningún cliente en esta ruta</div>
            <q-item-label caption class="q-mt-sm">
                Los clientes se agregarán automáticamente a medida que crees figuras,
                también puedes presionar en [Agregar cliente] para agregar un cliente
                a la ruta que no se encuentre dentro de ninguna figura
            </q-item-label>

        </EmptyListFace>
        <CustomerItem
            v-for="direction of customersDirection"
            :key="direction.id"
            :direction="direction"
            :customer="direction.customer"
            :style="direction.isInactive ? 'background-color:#ffe1e1' : ''"
        >
            <div class="row">
                <div v-if="direction.isInactive"
                    class="bg-red q-px-xs text-white text-caption rounded-borders q-mt-sm"
                >
                    Deshabilitado
                </div>
            </div>
            <div v-if="direction.extra" class="column">
                <div class="row">
                    <div class="q-px-sm q-mt-sm bg-primary text-white rounded-borders text-caption">Adicional</div>
                </div>
                <div class="row">
                    <div class="q-pl-xs q-mt-xs rounded-borders row no-wrap items-center" style="border:1px solid #888">
                        <div class="text-caption" style="line-height:1.2" :class="{'q-pr-xs q-py-xs': !direction.onlyOnce}">
                            {{direction.onlyOnce ? `Solo ${directionWeekDay(direction)} ${formatedDate(direction.date)}` : routeDays ? `Todos los ${routeDays}` : 'Ningún día seleccionado'}}
                        </div>
                        <q-btn v-if="direction.onlyOnce" flat round dense
                            color="grey-8" icon="edit" size="9px" class="q-ml-xs"
                            @click="editExtraDirectionDate(direction)" />
                        <!--<q-icon v-if="direction.onlyOnce" class="q-ml-sm" style="margin-top:1px" color="grey-7" name="o_info" />
                        <q-tooltip v-if="direction.onlyOnce">Luego se deshabilitará automáticamente</q-tooltip>-->
                    </div>
                </div>
            </div>
            <template v-slot:side>
                <ItemOptionsBtn :options="customerOptions(direction)" />
            </template>
        </CustomerItem>

    </q-list>
</template>

<script>
import { ref, computed } from 'vue';
import CustomerItem from './CustomerItem'
import EmptyListFace from 'src/components/includes/EmptyListFace'
import AddCustomerToZoneModal from 'src/components/zone/AddCustomerToZoneModal'
import UpdateCustomerZoneFrecuency from 'src/components/zone/UpdateCustomerZoneFrecuency'
import { useZones, useConfirmModal, useSelectDate } from 'src/context'
import ItemOptionsBtn from 'src/components/includes/ItemOptionsBtn'
import { weekDays } from 'src/utils/statics'

export default {
    components: {EmptyListFace, CustomerItem, AddCustomerToZoneModal, ItemOptionsBtn, UpdateCustomerZoneFrecuency},
    setup() {
        const showAddCustomerModal = ref(false)
        const showUpdateRouteFrecuency = ref(false)
        const updateDirection = ref(null)
        const {
            getRouteDays,
            selectedRoute,
            selectedRouteDirections,
            updateRouteExtraDirection,
            removeCustomerDirectionFromRoute,
            setRouteDirectionInactive,
        } = useZones()
        const { showDateSelector } = useSelectDate()
        const { showConfirmModal } = useConfirmModal()

        const customersDirection = computed(() => []
            .concat(selectedRoute.value.extraDirections.map(e => {
                return {
                    ...e.direction,
                    onlyOnce: e.onlyOnce,
                    date: e.date,
                    extra: true,
                    isInactive: selectedRoute.value.disabledDirections.includes(e.direction.id)
                }
            })
            .concat(selectedRouteDirections.value.map(d => {
                return {
                    ...d,
                    isInactive: selectedRoute.value.disabledDirections.includes(d.id)
                }
            }))))

        const routeDays = computed(() => {
            const days = getRouteDays(selectedRoute.value)
            return days && days.length ? days.map(d => d.name).reduce((result, d) => `${result}${result?', '+d:d}`, '') : null
        })

        const formatedDate = date => {
            if (!date) return ''
            const d = new Date(date)
            return `${d.getDate()}/${d.getMonth()+1}/${d.getFullYear()}`
        }
        const directionWeekDay = direction => direction && direction.date ?
            weekDays.find(d => d.weekday === new Date(direction.date).getDay()).name : ''
        const newDateWeekday = direction => new Date(direction.date).getDay()

        const editExtraDirectionDate = direction => showDateSelector(
            new Date(direction.date),
            date => updateRouteExtraDirection(direction, { date })
        )

        const customerOptions = direction => {
            return [{
                text: direction.isInactive ? 'Habilitar' : 'Deshabilitar',
                icon: direction.isInactive ? 'o_visibility' : 'o_visibility_off',
                // hidden: true,
                onClick: () => setRouteDirectionInactive(direction, !direction.isInactive),
            }, {
                text: 'Enfocar en el mapa',
                hidden: true,
                icon: 'o_pin_drop',
                onClick: () => {}
            }, /*{
                text: 'Mostrar siempre',
                icon: 'date_range',
                hidden: !direction.extra || !direction.onlyOnce,
                onClick: () => {
                    updateRouteExtraDirection(direction, {
                        date: null,
                        onlyOnce: false
                    }
                )},
            },*/ {
                text: 'Modificar frecuencia',
                icon: 'o_date_range',
                hidden: true,
                onClick: () => {
                    updateDirection.value = direction
                    showUpdateRouteFrecuency.value = true
                },
            }, /*{
                text: 'Mostrar por única vez',
                icon: 'o_today',
                hidden: !direction.extra || direction.onlyOnce,
                onClick: () => showDateSelector(
                    direction.date ? new Date(direction.date) : new Date(),
                    date => updateRouteExtraDirection(direction, { date, onlyOnce: true })
                ),
            },*/ {
                text: 'Remover de la ruta',
                icon: 'o_delete',
                hidden: !direction.extra,
                onClick: () => {
                    showConfirmModal({
                        text: '¿Estás seguro/a de que quieres remover este cliente de la ruta?',
                        color: 'red',
                        errorMessage: 'No fue posible realizar la operación, por favor vuelva a intentarlo',
                        async onConfirm() { await removeCustomerDirectionFromRoute(direction) }
                    })
                }
            }]
        }

        return {
            routeDays,
            updateDirection,
            selectedRoute,
            customersDirection,
            showAddCustomerModal,
            showUpdateRouteFrecuency,
            removeCustomerDirectionFromRoute,
            editExtraDirectionDate,
            directionWeekDay,
            customerOptions,
            newDateWeekday,
            formatedDate,
        }
    },
}
</script>
