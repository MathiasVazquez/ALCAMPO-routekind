import { computed, ref, nextTick } from "vue";
import { loadAllFromServer } from "./index";

const updatingMap = ref(false);
const forceReloadMap = ref(false);
const showSessionMenu = ref(false);
const showAppFrame = ref(false);

//
// TOP MESSAGE
//

const topMessage = ref(null);
const timeoutId = ref(0);
const centerMapCoords = ref(null);

export const useUI = () => {
  const showMessage = ({
    text,
    bgColor,
    bottom = 90,
    autoclose = 5000,
  } = {}) => {
    topMessage.value = {
      text,
      bgColor,
      bottom: bottom || 90,
      autoclose: autoclose || 5000,
    };

    if (autoclose < 1000) return;
    timeoutId.value = setTimeout(() => {
      topMessage.value = null;
      timeoutId.value = 0;
    }, autoclose);
  };
  const showWarningMessage = (text, { bottom, autoclose } = {}) => {
    showMessage({ text, bgColor: "bg-warning", bottom, autoclose });
  };
  const showErrorMessage = (text, { bottom, autoclose } = {}) => {
    showMessage({ text, bgColor: "bg-red", bottom, autoclose });
  };
  const showSuccessMessage = (text, { bottom, autoclose } = {}) => {
    showMessage({ text, bgColor: "bg-green", bottom, autoclose });
  };
  const closeMessage = () => {
    if (timeoutId.value) {
      clearTimeout(timeoutId.value);
      timeoutId.value = 0;
    }
    topMessage.value = null;
  };

  async function centerMap(coords) {
    if (coords?.lat && coords?.lng) {
      centerMapCoords.value = coords;
    } else {
      // await nextTick();
      forceReloadMap.value = true;
      // setTimeout(() => (centerMapCoords.value = { ...coords }), 1000);
      await nextTick();
      // centerMapCoords.value = null;
      forceReloadMap.value = false;
    }
  }

  return {
    topMessage: computed(() => topMessage.value),
    showWarningMessage,
    showErrorMessage,
    showSuccessMessage,
    closeMessage,
    updatingMap,
    forceReloadMap,
    centerMapCoords: computed(() => centerMapCoords.value),
    showSessionMenu,
    showAppFrame,
    centerMap,
    reloadMap: async (coords) => {
      await centerMap(coords);
      loadAllFromServer();
    },
  };
};
