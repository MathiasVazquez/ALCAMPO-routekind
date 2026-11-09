import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { useGenericEntityList } from './generics/listEntity.generic'
import { formatPolygonsJson, useZones, useMobiles } from 'src/context'

const planning = ref(store.get('planning', []))
const selectedPlanning = ref(null)

export const usePlanning = () => {
  const selectedPlanningPolygonsJson = computed(() => {
    const { selectedMobileList } = useMobiles()
    const { zones } = useZones()

    const selectedMobilesId = selectedMobileList.value.map(m => m.value)

    const planningRoutes = zones.value.filter(r => r.isActive && selectedMobilesId.includes(r.mobile) && r.planning === (selectedPlanning.value?.id || planning.value[0]?.id))
    const polygons = planningRoutes.reduce((result, r) => { return [...result, ...r.polygons.value] }, [])
    return formatPolygonsJson(polygons)
  })

  const options = ref({
    entityName: 'planning',
    entityNameSingular: 'planning',
    entityUrl: 'zone/planning/',
    selectedEntity: selectedPlanning,
  })
  return {
    ...useGenericEntityList(planning, options.value),
    activatedPlanning: computed(() => planning.value.find(p => p.isActive)),
    selectedPlanningPolygonsJson,
  }
}


/*
import axios from 'axios'
import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { BASE_URL, authHeader, replaceArrElementByProp, removeArrElementByProp } from '.'

const planning = ref(store.get('planning', []))
const selectedPlanning = ref(store.get('selectedPlanning', null))
const activatedPlanning = ref(store.get('activatedPlanning', null))

const UPDATE_ERROR = "No fue posible actualizar la planifización"
const ADD_ERROR = "No fue posible agregar la planifización"
const LOAD_ERROR = "No fue posible obtener las planifizaciones"
const DELETE_ERROR = "No fue posible eliminar la planificación"

const defaultPlanning = {
    id: 'default',
    name: 'Default',
    default: true
}

export const usePlanning = () => {

    const setPlanning = value => {
        planning.value = value
        store.set('planning', value)
    }

    const replaceInPlanning = value => {
        planning.value = replaceArrElementByProp(planning.value, value)
        store.set('planning', planning.value)
    }

    const activatePlanning = (value, updatePlanning=true) => {
        activatedPlanning.value = value
        store.set('activatedPlanning', activatedPlanning.value)
        if (updatePlanning) replaceInPlanning(activatedPlanning.value)
    }

    const selectPlanning = (value, updatePlanning=true) => {
        selectedPlanning.value = value
        store.set('selectedPlanning', selectedPlanning.value)
        if (updatePlanning) replaceInPlanning(selectedPlanning.value)
    }

    const loadPlanning = async () => {
        try {
            const { data } = await axios.get(`${BASE_URL}zone/planning/`, authHeader.value)
            setPlanning(data)
            // Updates activated planning
            activatePlanning(data.find(p => p.activated), false)
            // Update selected planning
            selectPlanning(selectedPlanning.value && data.find(p => p.id === selectedPlanning.value.id), false)
            // Return
            return { data }
        }
        catch (errorInfo) { return { error: LOAD_ERROR, errorInfo } }
    }

    const addPlanning = async plan => {
        try {
            const { data } = await axios.post(`${BASE_URL}zone/planning/`, plan, authHeader.value)
            setPlanning([...planning.value, data])
            selectPlanning(data, false)
            return { data }
        }
        catch (errorInfo) { return { error: ADD_ERROR, errorInfo } }
    }

    const updatePlanning = async props => {
        const selectedToUpdate = planning.value.find(p => p.id === props.id)
        if (!selectedToUpdate) return { error: UPDATE_ERROR }
        const updated = { ...selectedToUpdate, ...props }
        try {
            // Update in server
            const { data } = await axios.put(`${BASE_URL}zone/planning/?id=${updated.id}`, updated, authHeader.value)

            // Update in local
            if (data.id === selectedPlanning.value.id) selectPlanning(data, false)
            if (data.id === activatedPlanning.value.id || data.activated) activatePlanning(data, false)
            replaceInPlanning(data)

            return { data }
        }
        catch (errorInfo) { return { error: UPDATE_ERROR, errorInfo } }
    }

    const removePlan = async plan => {
        try {
            plan = plan || selectedPlanning.value
            if (activatedPlanning.value.id === plan.id) throw "Can't delete activated plannning"
            const { data } = await axios.delete(`${BASE_URL}zone/planning/?id=${plan.id}`, authHeader.value)
            setPlanning(removeArrElementByProp(planning.value, plan))
            return { data }
        }
        catch (errorInfo) { return { error: DELETE_ERROR, errorInfo } }
    }

    return {
        updatePlanning,
        loadPlanning,
        addPlanning,
        removePlan,
        selectPlanning,
        planning: computed(() => planning.value),
        selectedPlanning: computed(() => selectedPlanning.value),
        activatedPlanning: computed(() => activatedPlanning.value),
    }
}*/
