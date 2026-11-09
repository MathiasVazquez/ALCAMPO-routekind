import { store } from "src/store/local.store";
import { ref, computed, reactive, toRefs } from "vue";
import {
  formatToDatePicker,
  formatFromDatePicker,
  formatDate,
  isToday,
  isYesterday,
  isTomorrow,
  isOvermorrow,
  sameDate,
} from "src/helpers";

const defaultSettings = {
  polygonVisualization: {
    zones: "all",
    orders: "none",
    editmode: "zone",
    events: "none",
  }, // all, zone, figure, none
  addressesVisualization: {
    zones: "all",
    orders: "none",
    editmode: "none",
    events: "none",
  }, // all, zone, polygon, none
  orderVisualization: {
    zones: "none",
    orders: "all",
    editmode: "none",
    events: "none",
  }, // all, visible, none
  eventVisualization: {
    zones: "none",
    orders: "none",
    editmode: "none",
    events: "all",
  }, // all, visible, none
  selectedZoneListMainTab: "zones", // zones, orders, events
  viewScope: "zones", // zones, orders, events, editmode
  // orderDateFilter: formatToDatePicker(new Date()),
};
const orderDateFilter = ref(formatToDatePicker(new Date()));

const settings = reactive(store.get("settings", defaultSettings));
const showSettingsMenu = ref(false);
const showSearchAddress = ref(false);

export const useSettings = () => {
  const computeProp = (propName, { useViewScope } = {}) => {
    return {
      [propName]: computed({
        get: () => {
          const result = settings[propName] || defaultSettings[propName];
          return useViewScope
            ? result[settings.viewScope] ||
                defaultSettings[propName][settings.viewScope]
            : result;
        },
        set: (value) => {
          if (useViewScope)
            (settings[propName] = settings[propName] || {})[
              settings.viewScope
            ] = value;
          else settings[propName] = value;
          store.set("settings", { ...settings });
        },
      }),
    };
  };

  const viewScope = computeProp(
    "viewScope",
    defaultSettings.viewScope
  ).viewScope;

  return {
    viewScope,
    ...computeProp("polygonVisualization", { useViewScope: true }),
    ...computeProp("addressesVisualization", { useViewScope: true }),
    ...computeProp("orderVisualization", { useViewScope: true }),
    ...computeProp("eventVisualization", { useViewScope: true }),
    ...computeProp("selectedZoneListMainTab"),
    // ...computeProp("orderDateFilter"),
    orderDateFilter,
    orderDateFilterLabel: computed(() => {
      const date = formatFromDatePicker(orderDateFilter.value);
      return isToday(date)
        ? "Hoy"
        : isTomorrow(date)
        ? "Mañana"
        : isOvermorrow(date)
        ? "Pasado mañana"
        : isYesterday(date)
        ? "Ayer"
        : formatDate(date);
    }),
    showSettingsMenu,
    showSearchAddress,
  };
};
