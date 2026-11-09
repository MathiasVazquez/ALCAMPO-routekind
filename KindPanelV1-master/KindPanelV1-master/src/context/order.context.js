import { ref, computed } from "vue"
import { store } from "src/store/local.store"
import { useGenericEntityList } from "./generics/listEntity.generic"
import { useSettings, useMobiles, useVisits } from "src/context"
import { sameDate, formatFromDatePicker } from "src/helpers"

const orders = ref(store.get("orders", []))
const selectedOrder = ref(null)

export const useOrders = () => {
  const { orderDateFilter } = useSettings()
  const { selectedMobileList } = useMobiles()
  const { visits, getLastOrderVisitById } = useVisits()

  const selectedDate = computed(() =>
    formatFromDatePicker(orderDateFilter.value)
  )

  const options = ref({
    entityName: "orders",
    entityNameSingular: "order",
    entityUrl: "order/",
    selectedEntity: selectedOrder,
    deselectOnSelfSelection: true,
    canDeselectEntity: true,
    formatter: (order) => {
      const lastVisit = computed(
        () => visits.value && getLastOrderVisitById(order.id)
      )
      const hasVisit = computed(() => !!lastVisit.value)
      const hasDelivered = computed(() => lastVisit.value?.visited)
      const visitLater = computed(
        () => !hasDelivered.value && lastVisit.value?.visitLater
      )
      const hasSkiped = computed(
        () => hasVisit.value && !hasDelivered.value && !visitLater.value
      )
      const assigned = computed(
        () => !!(order.mobile || order.autoAssignedToMobile)
      )
      return {
        ...order,
        hasVisit,
        hasDelivered,
        visitLater,
        hasSkiped,
        assigned,
        isDate: (d) => sameDate(new Date(order.expiryDate), new Date(d)),
      }
    },
    listFilter: (order) => {
      // Filter by date
      if (!sameDate(order.expiryDate, selectedDate.value)) return false
      // Filter by mobile
      const selectedMobileIncluded = selectedMobileList.value.some(
        (m) =>
          m.value === order.mobile || m.value === order.autoAssignedToMobile
      )
      if (!selectedMobileIncluded) return false
      // All filter pass
      return true
    },
  })

  const manager = useGenericEntityList(orders, options.value)

  const sortOrders = (unsortOrders) => {
    const firstOrder = unsortOrders.find((o) => o.isFirstOrder)
    if (firstOrder) {
      const sortedOrders = []
      let currentOrder = firstOrder
      while (currentOrder) {
        sortedOrders.push(currentOrder)
        currentOrder = unsortOrders.find((o) => o.id === currentOrder.nextOrder)
      }
      return Array.from(new Set(sortedOrders.concat(unsortOrders)))
    }
    return unsortOrders
  }

  const getOrdersByDate = (date) =>
    manager.allOrders.value.filter((order) =>
      sameDate(order.expiryDate, new Date(date))
    )

  const unassignedOrders = computed(() => {
    // Filter by date
    return manager.allOrders.value.filter((order) => {
      if (!sameDate(order.expiryDate, selectedDate.value)) return false
      return !order.mobile && !order.autoAssignedToMobile
    })
  })

  const ordersGroupByMobile = computed(() => {
    // Group orders
    const result = {}
    manager.orders.value.forEach((o) => {
      const mobile = o.mobile || o.autoAssignedToMobile
      if (!result[mobile]) result[mobile] = [o]
      else result[mobile].push(o)
    })
    // Sort order group elements
    const sortedResilt = {}
    for (const group in result) sortedResilt[group] = sortOrders(result[group])
    return sortedResilt
  })

  const insertOrderAtIndex = async (index, order) => {
    const _order = order || manager.selectedOrder.value
    if (!index)
      return await manager.updateOrder({
        id: _order.id,
        nextOrder: null,
        prevOrder: null,
      })

    const mobileOrders =
      ordersGroupByMobile.value[_order.mobile || _order.autoAssignedToMobile]
    const firstOrder = mobileOrders.find((o) => o.isFirstOrder)
    if (index === 1)
      return await manager.updateOrder({
        id: _order.id,
        nextOrder: firstOrder?.id || null,
      })

    let selectedOrderIndex = 1
    for (const mobileOrder of mobileOrders)
      if (_order.id === mobileOrder.id) break
      else selectedOrderIndex++

    await manager.updateOrder({
      id: _order.id,
      prevOrder: mobileOrders[index - (selectedOrderIndex < index ? 1 : 2)].id, // prevOrder.id,
      mobile: _order.mobile || _order.autoAssignedToMobile,
    })
  }

  return {
    ...manager,
    unassignedOrders,
    ordersGroupByMobile,
    ordersGroupByMobileWithUnassigned: computed(() => {
      return {
        ...ordersGroupByMobile.value,
        ...(unassignedOrders.value?.length > 0
          ? { [-1]: unassignedOrders.value }
          : {}),
      }
    }),
    insertOrderAtIndex,
    getOrdersByDate,
  }
}
