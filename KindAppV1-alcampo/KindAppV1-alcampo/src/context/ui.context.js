import { computed, ref, nextTick } from 'vue'

const updatingMap = ref(false)

//
// TOP MESSAGE
//

const topMessage = ref(null)
const timeoutId = ref(0)
const showCenterMapBtn = ref(false)
const showLeftDrawer = ref(false)
const canShowCenterMapButton = ref(false)

export const useUI = () => {
  const showMessage = ({ text, bgColor, bottom=90, autoclose=5000 }={}) => {
    topMessage.value = { text, bgColor, bottom: bottom || 90, autoclose: autoclose || 5000 }
    
    if (autoclose < 1000) return
    timeoutId.value = setTimeout(() => {
      topMessage.value = null
      timeoutId.value = 0
    }, autoclose)
  }
  const showWarningMessage = (text, { bottom, autoclose }={}) => {
    showMessage({ text, bgColor: 'bg-warning', bottom, autoclose })
  }
  const showErrorMessage = (text, { bottom, autoclose }={}) => {
    showMessage({ text, bgColor: 'bg-red', bottom, autoclose })
  }
  const showSuccessMessage = (text, { bottom, autoclose }={}) => {
    showMessage({ text, bgColor: 'bg-green', bottom, autoclose })
  }
  const closeMessage = () => {
    if (timeoutId.value) {
      clearTimeout(timeoutId.value)
      timeoutId.value = 0
    }
    topMessage.value = null
  }
  
  return {
    topMessage: computed(() => topMessage.value),
    showWarningMessage,
    showSuccessMessage,
    showErrorMessage,
    closeMessage,
    updatingMap,
    showCenterMapBtn,
    showLeftDrawer,
    canShowCenterMapButton,
    centerMap: async () => {
      updatingMap.value = true
      await nextTick()
      updatingMap.value = false
      setTimeout(() => {
        showCenterMapBtn.value = false
        canShowCenterMapButton.value = true
      }, 500)
    },
  }
}
