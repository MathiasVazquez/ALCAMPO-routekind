import { computed, ref, reactive } from 'vue'

// const showSelectDateModal = ref(null)
const selectedDate = ref(null)
const onConfirmAction = ref(async () => {})

export const useSelectDate = () => {

    const showDateSelector = (initDate, onConfirm) => {
        // showSelectDateModal.value = true
        selectedDate.value = initDate || new Date()
        onConfirmAction.value = onConfirm
    }

    const confirmDateSelector = async () => {
        if (onConfirmAction.value) {
            await onConfirmAction.value(selectedDate.value)
        }
        // showSelectDateModal.value = false
        selectedDate.value = null
    }

    const closeDateSelector = () => {
        selectedDate.value = null
    }

    const selectDate = date => {
        selectedDate.value = date
    }

    return {
        selectDate,
        showDateSelector,
        closeDateSelector,
        confirmDateSelector,
        selectedDate: computed(() => selectedDate.value),
        formatedDate: computed(() => (selectedDate.value || new Date()).toISOString())
    }
}