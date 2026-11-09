import { ref, computed } from "vue";
import { store } from "src/store/local.store";
import { useGenericEntityList } from "./generics/listEntity.generic";
import {
  formatPolygonsJson,
  usePolygonPins,
  useCustomerAddresses,
} from "src/context";

const polygons = ref(store.get("polygons", []));
const selectedPolygon = ref(null);
const showPolygonEditor = ref(false);
const selectedPolygonEditorOption = ref("edit");

/**
 * Verify if point of coordinates (longitude, latitude) is polygon of coordinates
 * https://github.com/substack/point-in-polygon/blob/master/index.js
 * @param {number} latitude Latitude
 * @param {number} longitude Longitude
 * @param {array<[number,number]>} polygon Polygon contains arrays of points. One array have the following format: [latitude,longitude]
 */
export function isPointInPolygon(latitude, longitude, polygon) {
  if (typeof latitude !== "number" || typeof longitude !== "number") {
    throw new TypeError("Invalid latitude or longitude. Numbers are expected");
  } else if (!polygon || !Array.isArray(polygon)) {
    throw new TypeError("Invalid polygon. Array with locations expected");
  } else if (polygon.length === 0) {
    throw new TypeError("Invalid polygon. Non-empty Array expected");
  }

  const x = latitude;
  const y = longitude;

  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i][0],
      yi = polygon[i][1];
    const xj = polygon[j][0],
      yj = polygon[j][1];

    const intersect =
      yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
    if (intersect) inside = !inside;
  }
  return inside;
}

export const usePolygons = () => {
  const { polygonPins, sortFromInitialPin } = usePolygonPins();
  const { customerAddresses } = useCustomerAddresses();

  const getAddressesFromPolygonList = async (polygonList) => {
    // console.log('--> getAddressesFromPolygonList')
    if (!polygonList || polygonList.length === 0) return [];
    const polygonAddresses = [];
    await Promise.all(
      [].concat(polygonList).map(async (polygon) => {
        const listOfPoints = polygon.listOfPoints.value;
        if (listOfPoints && listOfPoints.length > 0) {
          await Promise.all(
            customerAddresses.value.map(async (address) => {
              if (
                address.lat &&
                address.lng &&
                isPointInPolygon(
                  parseFloat(address.lat),
                  parseFloat(address.lng),
                  listOfPoints
                )
              )
                polygonAddresses.push(address);
            })
          );
        }
      })
    );
    return polygonAddresses;
  };

  const formatter = (polygon) => {
    if (!polygon) return null;
    const pins = computed(() =>
      sortFromInitialPin(
        polygonPins.value.find((pin) => pin.polygon === polygon.id && !pin.prev)
      )
    );
    const semiFormatted = {
      ...polygon,
      polygonPins: pins,
      listOfPoints: computed(() => pins.value.map((pin) => [pin.lat, pin.lng])),
    };
    return {
      ...semiFormatted,
      getAddresses: () => getAddressesFromPolygonList(semiFormatted),
    };
  };

  const options = ref({
    entityName: "polygons",
    entityNameSingular: "polygon",
    entityUrl: "zone/polygon/",
    selectedEntity: selectedPolygon,
    canDeselectEntity: true,
    confirmDeleteMessage: "¿Está seguro/a de que desea eliminar esta figura?",
    formatter,
  });

  const manager = useGenericEntityList(polygons, options.value);

  const getPolygonJson = (polygon) =>
    formatPolygonsJson(polygon ? [polygon.id] : []);

  return {
    ...manager,
    selectedPolygonEditorOption,
    getAddressesFromPolygonList,
    showPolygonEditor,
    getPolygonJson,
  };
};
