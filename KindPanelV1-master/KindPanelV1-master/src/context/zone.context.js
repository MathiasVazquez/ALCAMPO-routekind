import { store } from "src/store/local.store"
import { ref, computed, watch } from "vue"
import { useGenericEntityList } from "./generics/listEntity.generic"
import { authHeader, BASE_URL } from "."
import axios from "axios"
import {
  formatPolygonsJson,
  usePlanning,
  useMobiles,
  usePolygons,
} from "src/context"

const zones = ref(store.get("zones", []))
const selectedZoneAddresses = ref([])
const selectedZone = ref(null)

export const useZones = () => {
  const { selectedPlanning } = usePlanning()
  const { selectedMobileList } = useMobiles()
  const { polygons, getAddressesFromPolygonList } = usePolygons()

  const selectedZonePolygonsJson = computed(() =>
    formatPolygonsJson(selectedZone.value?.polygons.value)
  )

  const options = ref({
    entityName: "zones",
    entityNameSingular: "zone",
    entityUrl: "zone/",
    selectedEntity: selectedZone,
    canDeselectEntity: true,
    confirmDeleteMessage: "¿Está seguro/a de que desea eliminar esta zona?",
    formatter: (zone) => {
      const zonePolygons = computed(() =>
        polygons.value.filter((p) => p.zone === zone.id)
      )
      return {
        ...zone,
        alias: zone.name || `Zona ${zone.id}`,
        polygons: zonePolygons,
        getAddresses: () =>
          getAddressesFromPolygonList(
            zonePolygons.value.filter((p) => p.isActive)
          ),
      }
    },
    listFilter: (r) =>
      r.planning === selectedPlanning.value.id &&
      selectedMobileList.value.some((m) => m.value === r.mobile),
    listSort: (r1, r2) =>
      r1.isActive && !r2.isActive ? -1 : !r1.isActive && r2.isActive ? 1 : 0,
    onDelete: ({ request, manager, error }) => {
      if (error) return
      if (request.id === manager?.selectedEntity.value?.id)
        manager.selectEntity(null)
    },
  })

  const manager = useGenericEntityList(zones, options.value)

  const zonesGroupedByMobile = computed(() => {
    const result = {}
    manager.zones.value.forEach((r) => {
      if (!result[r.mobile]) result[r.mobile] = [r]
      else result[r.mobile].push(r)
    })
    return result
  })

  const updateSelectedZoneAddresses = async () =>
    (selectedZoneAddresses.value =
      manager.selectedZone.value &&
      (manager.selectedZone.value.includeInternalCustomers ?? true)
        ? await manager.selectedZone.value.getAddresses()
        : [])
  watch(selectedZone, updateSelectedZoneAddresses)

  async function setAddressIsActive(zoneId, addressId, { isActive, remove }) {
    const action = remove
      ? "remove_additional_address"
      : isActive
      ? "activate_address"
      : "deactivate_address"
    const result = await axios.patch(
      `${BASE_URL}zone/${zoneId}/${action}/`,
      { address_id: addressId },
      authHeader.value
    )
    await manager.updateZone({ id: zoneId })
    return result
  }

  return {
    ...manager,
    zonesGroupedByMobile,
    selectedZoneAddresses,
    selectedZonePolygonsJson,
    updateSelectedZoneAddresses,
    setAddressIsActive,
  }
}
