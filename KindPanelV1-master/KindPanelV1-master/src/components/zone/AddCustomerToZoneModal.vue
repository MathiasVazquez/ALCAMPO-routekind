<template>
    <q-dialog :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)"
        transition-show="rotate" transition-hide="rotate" persistent
    >
        <q-card>
            <q-card-section>
                <div class="row justify-between items-center">
                    <div class="text-body1 text-grey-9">
                        Agregar clientes a la zona <strong>{{selectedZone.name || `Zona ${selectedZone.id}`}}</strong>
                    </div>
                    <q-btn flat round icon="close" @click="$emit('update:modelValue', false)" />
                </div>
            </q-card-section>

            <q-separator />

            <q-card-section style="max-height:65vh;width:50vw;max-width:400px" class="scroll">
                <!-- SEARCH CUSTOMER -->
                <div class="rounded-borders overflow-hidden">
                    <q-input borderless
                        class="q-px-sm rounded-borders bg-grey-2"
                        v-model="search" label="Buscar cliente"
                    >
                        <template v-slot:prepend>
                            <q-icon name="search" class="q-ml-sm" />
                        </template>
                        <template v-slot:append>
                            <q-btn v-if="search"
                                flat round dense icon="close"
                                class="q-mr-xs" @click="search=''" />
                        </template>
                    </q-input>
                </div>
                <div class="q-mt-xs q-pa-xs text-subtitle2 text-weight-light text-grey-8">
                    {{filteredCustomers.length}} {{filteredCustomers.length===1?'cliente disponible':'clientes disponibles'}}
                </div>
                <!-- CUSTOMER LIST -->
                <q-list>
                    <CustomerItem v-for="direction of currentPageCustomers" :key="direction.id"
                        :direction="direction" :customer="direction.customer"
                    >
                        <!--<template v-slot:side>
                            <q-btn icon="add" round dense outline
                                color="primary" class="q-mr-xs"
                                @click="addCustomerDirectionToRoute(direction)"
                            />
                        </template>-->
                        <div class="row">
                            <q-btn flat no-caps dense class="q-mt-sm q-pa-xs text-caption text-grey-8"
                                style="border:1px solid #ccc"
                                @click="addCustomerDirectionToRoute(direction)"
                            >
                                <q-icon name="add" size="16px" style="margin-top:2px" class="q-mr-xs" />
                                <div>Agregar a la zona</div>
                            </q-btn>
                            <!--<div style="border:1px solid #ccc" class="rounded-borders text-grey-8 q-mt-sm bg-grey-2">
                                <ItemOptionsBtn icon="add"
                                :options="addToDayOptions"
                                :hide-tooltip="true"
                                label="Agregar a la zona"
                            />
                            </div>-->
                            <!--<div class="q-px-sm q-mt-sm bg-primary text-white rounded-borders text-caption">Extra</div>-->
                        </div>
                        <!--<div class="row">
                            <q-btn flat round
                                v-if="!directionIsInRoute(direction)"
                                @click="addCustomerDirectionToRoute(direction)"
                                color="primary" icon="add"
                            >
                                <q-tooltip>
                                    Agregar de la zona
                                </q-tooltip>
                            </q-btn>
                            <q-btn flat round v-else color="red" icon="o_delete"
                                @click="removeCustomerDirectionFromRoute(direction)"
                            >
                                <q-tooltip>
                                    Remover de la zona
                                </q-tooltip>
                            </q-btn>
                        </div>-->
                    </CustomerItem>
                </q-list>
            </q-card-section>

            <q-separator />

            <q-card-actions align="right">
                <q-btn round flat color="grey-8" icon="chevron_left" @click="page=page<=0?0:page-1" />
                <div class="q-px-sm text-caption">Página {{page+1}} de {{totalPages}}</div>
                <q-btn round flat color="grey-8" icon="chevron_right" @click="page=page>=totalPages-1?totalPages-1:page+1" />
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { ref, toRefs, computed, watch } from 'vue'
import { useZones, useCustomers } from 'src/context'
import CustomerItem from 'src/components/customer/CustomerItem'
import ItemOptionsBtn from 'src/components/includes/ItemOptionsBtn'

export default {
    name: 'AddCustomerToRouteModal',
    components: {CustomerItem, ItemOptionsBtn},
    props: ['modelValue'],
    emits: ['update:modelValue'],
    setup(props) {
        const { modelValue } = toRefs(props)
        const {
            selectedZone,
            selectedZoneDirections,
            addCustomerDirectionToRoute,
            removeCustomerDirectionFromRoute,
        } = useZones()
        const { customersDirections } = useCustomers()
        const search = ref('')
        const page = ref(0)
        const perPage = ref(10)

        const directionIsInRoute = dir => {
            const existIds = selectedZone.value.extraDirections.map(e => e.direction.id)
            return existIds.includes(dir.id)
        }

        const filteredCustomers = computed(() => {
            const catchSearch = d => {
                const c = d.customer
                return (`${c.firstName} ${c.lastName}` || '').toLowerCase().includes(search.value.toLowerCase()) ||
                    (c.ci || "").toLowerCase().includes(search.value.toLowerCase()) ||
                    (c.email || "").toLowerCase().includes(search.value.toLowerCase())
            }
            const alreadyIds = selectedZoneDirections.value.map(d => d.id)
            const notAdded = customersDirections.value.filter(c => !alreadyIds.includes(c.id) && !directionIsInRoute(c))
            /*const filter1 = customersDirections.value.filter(c => !alreadyIds.includes(c.id))
            const filter2 = filter1.slice(page.value, page.value + perPage.value)
            const filter3 = search.value ? filter2.filter(catchSearch) : filter2
            return filter3*/
            const searched = search.value ? notAdded.filter(catchSearch) : notAdded
            return searched
        })

        const currentPageCustomers = computed(() => {
            /*const catchSearch = c => {
                return (`${c.firstName} ${c.lastName}` || '').toLowerCase().includes(search.value.toLowerCase()) ||
                    (c.ci || "").toLowerCase().includes(search.value.toLowerCase()) ||
                    (c.email || "").toLowerCase().includes(search.value.toLowerCase())
            }*/

            const initIndex = page.value * perPage.value
            return filteredCustomers.value.slice(initIndex, Math.min(initIndex + perPage.value, filteredCustomers.value.length))
        })

        const addToDayOptions = computed(() => {
            return [{
                text: 'Lunes',
                // icon: direction.disabled ? 'o_visibility' : 'o_visibility_off',
                onClick: () => {},
            }]
        })

        watch(search, () => page.value = 0)

        const totalPages = computed(() => Math.ceil(filteredCustomers.value.length / perPage.value))

        return {
            removeCustomerDirectionFromRoute,
            addCustomerDirectionToRoute,
            directionIsInRoute,
            filteredCustomers,
            currentPageCustomers,
            selectedZone,
            modelValue,
            search,
            page,
            totalPages,
            addToDayOptions,
        }
    },
}
</script>
