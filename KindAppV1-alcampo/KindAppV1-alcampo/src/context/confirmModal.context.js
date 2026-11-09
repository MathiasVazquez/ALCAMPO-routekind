import { computed, ref, reactive } from 'vue'

const confirmOptions = ref(null)
const loadingConfirmModal = ref(false)
const hasError = ref(false)
let onConfirmAction = null
let onSuccessAction = null
let onErrorAction = null

export const useConfirmModal = () => {

  const showConfirmModal = ({ text, icon, color, errorMessage, onConfirm, onSuccess, onError, confirmButtonMessange } = { }) => {
    onConfirmAction = onConfirm
    onSuccessAction = onSuccess
    onErrorAction = onError
    confirmOptions.value = {
      text,
      icon,
      color,
      errorMessage,
      confirmButtonMessange: confirmButtonMessange || 'Confirmar',
    }
  }
  const hideConfirModal = () => {
    loadingConfirmModal.value = false
    confirmOptions.value = null
    onConfirmAction = null
    onSuccessAction = null
    onErrorAction = null
  }
  const handleOnConfirm = async () => {
    loadingConfirmModal.value = true
    try {
      const response = await onConfirmAction()
      if (onSuccessAction) await onSuccessAction()
      hideConfirModal()
      return response
    }
    catch (error) {
      hasError.value = true
      if (onErrorAction) onErrorAction(error)
      return { error }
    }
    finally {
      loadingConfirmModal.value = false
    }
  }

  return {
    hasError,
    onConfirm: handleOnConfirm,
    hideConfirModal,
    showConfirmModal,
    confirmOptions: computed(() => confirmOptions.value),
    loadingConfirmModal: computed(() => loadingConfirmModal.value),
  }
}
