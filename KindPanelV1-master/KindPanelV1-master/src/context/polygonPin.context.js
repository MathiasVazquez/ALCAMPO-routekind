import { ref, computed } from "vue";
import { store } from "src/store/local.store";
import { useGenericEntityList } from "./generics/listEntity.generic";

const polygonPins = ref(store.get("polygonPins", []));
const selectedPolygonPin = ref(null);

export const usePolygonPins = () => {
  const replaceAllPins = async (geoJson) => {};

  const options = ref({
    entityName: "polygonPins",
    entityNameSingular: "polygonPin",
    entityUrl: "zone/polygon-pin/",
    selectedEntity: selectedPolygonPin,
    // confirmDeleteMessage: '¿Está seguro/a de que desea eliminar este marcador?',
    formatter: (pin, list) => {
      if (!pin) return null;
      return {
        ...pin,
        next: computed(() => list.find((p) => p.prev === pin.id)?.id),
      };
    },
  });

  const manager = useGenericEntityList(polygonPins, options.value);

  const sortFromInitialPin = (initialPin) => {
    // console.log('--> sortFromInitialPin')
    if (initialPin?.prev) return [];
    const sortedPins = [];
    let currentPin = initialPin;
    while (currentPin) {
      sortedPins.push(currentPin);
      currentPin = manager.getPolygonPinById(currentPin.next.value);
    }
    return sortedPins;
  };

  return {
    ...manager,
    replaceAllPins,
    sortFromInitialPin,
  };
};
