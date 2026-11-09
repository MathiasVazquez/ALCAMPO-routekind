<template>
    <q-dialog v-model="showDate" persistent
        transition-show="rotate" transition-hide="rotate"
    >
        <q-date v-model="dateValue" minimal>
            <div class="row justify-between">
                <q-btn no-caps dense flat color="grey-8" @click="closeDateSelector">Cerrar</q-btn>
                <q-btn no-caps dense flat color="primary" @click="confirmDateSelector">Seleccionar</q-btn>
            </div>
        </q-date>
    </q-dialog>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useSelectDate } from 'src/context'

export default {
    setup() {
        const {
            selectDate,
            selectedDate,
            formatedDate,
            closeDateSelector,
            showSelectDateModal,
            confirmDateSelector,
        } = useSelectDate()

        const showDate = computed({
            get() { return !!selectedDate.value },
            set(value) { if (!value) selectedDate(null) }
        })

        const dateValue = computed({
            get() {
                const d = selectedDate.value || new Date()
                const month = d.getMonth() + 1
                const monthDay = d.getDate()
                return `${d.getFullYear()}/${month < 10 ? '0'+month : month}/${monthDay < 10 ? '0'+monthDay : monthDay}`
            },
            set(date) {selectDate(new Date(date))},
        })
        
        return {
            showDate,
            dateValue,
            selectDate,
            selectedDate,
            formatedDate,
            closeDateSelector,
            confirmDateSelector,
            showSelectDateModal,
        }
    },
}
</script>