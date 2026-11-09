<template>
  <div class="row">
    <q-item-label v-for="day of zoneDays || []" :key="day.id" caption
      class="row text-grey-8 q-pa-xs q-mr-sm q-mt-xs rounded-borders items-center"
      style="border:1px solid #ccc"
    >
      <div class="q-mr-xs">{{day.name}}</div>
      <q-btn v-if="canRemove && isSelectedRoute" flat dense round
        icon="close" size="6px" class="q-pa-none q-ma-none"
        @click="handleDeleteDayFromRoute(day.code)"
      >
        <q-tooltip>Remover día</q-tooltip>
      </q-btn>
    </q-item-label>
    <!-- EMPTY ROUTE DAY LIST MESSAGE -->
    <q-item-label v-if="zoneDays.length <= 0" caption class="row text-grey-8 q-pa-xs q-mt-xs rounded-borders items-center">
      <div class="q-mr-xs">Sin días</div>
    </q-item-label>
    <!-- ADD DAY TO ROUTE -->
    <q-item-label v-if="isSelectedRoute" caption
      class="row text-grey-8 q-pa-xs q-mr-sm q-mt-xs rounded-borders"
      style="border:1px solid #ccc"
    >
      <q-icon name="add" />
      <q-tooltip>Agregar día</q-tooltip>
      <q-menu auto-close>
        <q-list>
          <q-item v-for="day of unselectedWeekDays" :key="day.code"
            clickable @click="handleAddDayToRoute(day.code)"
          >
            <q-item-section>
              <q-item-label>
                {{day.name}}
              </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-item-label>
  </div>
</template>

<script>
import { ref, computed, toRefs } from 'vue'
import { weekDays } from 'src/utils/statics'
import { useZones, useConfirmModal } from 'src/context'

export default {
  props: ["zone", "canRemove"],
  emits: ["delete"],
  setup(props) {
    const { zone, canRemove } = toRefs(props)
    const { updateZone, selectedZone } = useZones()
    const { showConfirmModal } = useConfirmModal()

    const isSelectedRoute = computed(() => selectedZone.value && zone.value.id === selectedZone.value.id)
    const zoneDays = computed(() => {
      const dayCodes = zone.value.days
      const dayCodesArr = !dayCodes ? [] : typeof dayCodes === 'string' ? dayCodes.split(',') : dayCodes
      return dayCodesArr.map(c => weekDays.find(d => `${d.code}` === `${c}`)).sort((a, b) => a.code > b.code ? 1 : a.code < b.code ? -1 : 0)
    })

    const unselectedWeekDays = computed(() => {
      const zoneDaysCodes = zoneDays.value.map(d => d.code)
      return weekDays.filter(d => !zoneDaysCodes.includes(d.code))
    })
    const handleAddDayToRoute = async dayCode => {
      const days = selectedZone.value.days ? selectedZone.value.days + `,${dayCode}` : `${dayCode}`
      await updateZone({ id: zone.value.id, days })
    }
    const handleDeleteDayFromRoute = dayCode => {
      console.log('handleDeleteDayFromRoute')
      showConfirmModal({
        text: '¿Está seguro/a de que desea remover este día de la zona?',
        color: 'red',
        errorMessage: 'No fue posible remover el día, por favor vuelva a intentarlo',
        onConfirm: async () => {
          const days = zone.value.days.split(',').filter(d => `${d}` !== `${dayCode}`).join(',')
          await updateZone({ id: zone.value.id, days })
        }
      })
    }

    return {
      zone,
      weekDays,
      zoneDays,
      canRemove,
      isSelectedRoute,
      unselectedWeekDays,
      handleAddDayToRoute,
      handleDeleteDayFromRoute,
    }
  },
}
</script>
