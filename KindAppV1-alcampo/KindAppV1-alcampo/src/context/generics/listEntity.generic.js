import { store } from 'src/store/local.store'
import { ref, computed, toRefs } from 'vue'
import { useUI, useConfirmModal, authHeader, BASE_URL, useSession } from 'src/context'
import axios from 'axios'

export const mustCloseSession = ref(false)

export const validateResponse = (error) => {
  if (!error) return true
  const { logout } = useSession()
  if ([401, 403].includes(error.response?.status)) {
    mustCloseSession.value = true
    logout()
  }
  return false
}

export const useGenericEntityList = (entityList, options) => {
  const { showSuccessMessage, showErrorMessage } = useUI()
  const { showConfirmModal } = useConfirmModal()
  const { entityName, entityNameSingular, entityUrl, selectedEntity } = toRefs(options)
  const formatter = options?.formatter || (e => e)
  const requestFormatter = options?.requestFormatter || (e => e)
  const localOnly = options?.localOnly || false

  const entityTitle = computed(() => `${(entityName.value[0] + "").toUpperCase()}${entityName.value.slice(1)}`)
  const entitySingularTitle = computed(() => `${(entityNameSingular.value[0] + "").toUpperCase()}${entityNameSingular.value.slice(1)}`)

  const getEntityById = (id, format = true) => {
    const _entity = entityList.value.find(c => `${c.id}` === `${id}`)
    return format ? formatter(_entity) : _entity
  }

  const setEntityList = value => {
    entityList.value = value
    store.set(entityName.value, value)
  }
  const updateListEntity = entity => {
    setEntityList(entityList.value.map(c => `${c.id}` === `${entity.id}` ? { ...c, ...entity } : c))
    if (selectedEntity && `${entity.id}` === `${selectedEntity.value?.id}`) selectEntity({ ...selectedEntity.value, ...entity }, false)
  }
  const selectEntity = (value, updateList = true) => {
    if (selectedEntity) {
      selectedEntity.value = value ? getEntityById(value.id, false) : null
      if (updateList && value) updateListEntity(selectedEntity.value)
    }
  }

  //
  // HTTP METHODS IMPLEMENTATION
  //

  const addEntity = async request => {
    try {
      const formattedRequest = requestFormatter(request)
      // console.log('formattedRequest:', formattedRequest)
      const { data } = localOnly ?
        { data: { id: entityList.value.length, ...formattedRequest } } :
        await axios.post(`${BASE_URL}${entityUrl.value}`, formattedRequest, authHeader.value)
      setEntityList([...entityList.value, data])
      if (options.onPost) options.onPost({ data, request: formattedRequest, manager: entityManager })
      return { data }
    }
    catch (error) {
      validateResponse(error)
      showErrorMessage("No fue posible realizar la creación")
      if (options.onPost) options.onPost({ error, manager: entityManager })
      return { error }
    }
  }

  const updateEntity = async (request, updateLocalList = true) => {
    const updateSingleEntity = async (singleRequest, _updateLocalList) => {
      try {
        const { data } = localOnly ?
          { data: {...getEntityById(singleRequest.id, false), ...singleRequest} } :
          await axios.put(`${BASE_URL}${entityUrl.value}${singleRequest.id}/`, singleRequest, authHeader.value)
        if (_updateLocalList) updateListEntity(data)
        return { data }
      }
      catch (error) {
        validateResponse(error)
        showErrorMessage("No fue posible realizar la modificación")
        return { error }
      }
    }

    if (Array.isArray(request)) {
      const results = []
      for (let singleRequest of request) if (!!singleRequest) results.push(await updateSingleEntity(singleRequest, false))
      for (let result of results) updateListEntity(result.data)
      return results
    }
    else return await updateSingleEntity(request, updateLocalList)
  }

  const deleteEntity = async request => {
    const confirDeleteEntity = async () => {
      try {
        const { data } = localOnly ? { data: request } : await axios.delete(`${BASE_URL}${entityUrl.value}${request.id}/`, authHeader.value)
        setEntityList(entityList.value.filter(c => c.id !== request.id))
        if (options.onDelete) options.onDelete({ request, data, manager: entityManager })
        return { data }
      }
      catch (error) {
        validateResponse(error)
        showErrorMessage("No fue posible realizar la eliminación")
        if (options.onDelete) options.onDelete({ error, manager: entityManager })
        return { error }
      }
    }
    if (options.confirmDeleteMessage) {
      showConfirmModal({
        text: options.confirmDeleteMessage,
        color: 'primary',
        errorMessage: 'No fue posible realizar la eliminación',
        onConfirm: () => confirDeleteEntity()
      })
    }
    else confirDeleteEntity()
  }

  const deleteEntityById = async id => {
    return await deleteEntity({ id })
  }

  const loadEntityById = async (entityId) => {
    try {
      const { data } = await axios.get(`${BASE_URL}${entityUrl.value}${entityId}/`, authHeader.value)
      const exists = entityList.value.some(e => e.id === data.id)
      if (exists) setEntityList(entityList.value.map(e => e.id === data.id ? data : e))
      else setEntityList(data, ...entityList.value)
      return { data }
    }
    catch (error) {
      validateResponse(error)
      if (!([401, 403].includes(error?.response?.status)))
        showErrorMessage("No fue posible obtener la lista")
      return { error }
    }
  }

  const loadEntity = async () => {
    try {
      if (localOnly) return { data: entityList.value }
      const { data } = await axios.get(`${BASE_URL}${entityUrl.value}`, authHeader.value)
      setEntityList(data)
      return { data }
    }
    catch (error) {
      validateResponse(error)
      if (!([401, 403].includes(error?.response?.status)))
        showErrorMessage("No fue posible obtener la lista")
      return { error }
    }
  }

  const formattedEntityList = computed(() => entityList.value.map(formatter))
  const formattedSelectedEntity = computed(() => {
    const entity = options.canDeselectEntity ? selectedEntity.value : selectedEntity.value || entityList.value[0]
    return entity && formatter(entity)
  })
    // selectedEntity.value ? (selectedEntity.value.__cancelSelection ? null : selectedEntity.value) : entityList.value[0])
  const entityManager = {
    entityList: formattedEntityList,
    selectedEntity: formattedSelectedEntity,
    selectEntity,
    setEntityList,
    getEntityById,
    addEntity,
    updateEntity,
    deleteEntity,
    deleteEntityById,
    loadEntity,
    loadEntityById,
  }

  return {
    manager: entityManager,
    [`${entityName.value}Manager`]: entityManager,
    [`${entityName.value}`]: formattedEntityList,
    [`unformat${entityTitle.value}`]: entityList,
    [`selected${entitySingularTitle.value}`]: formattedSelectedEntity,
    [`select${entitySingularTitle.value}`]: selectEntity,
    [`set${entityTitle.value}`]: setEntityList,
    [`get${entitySingularTitle.value}ById`]: getEntityById,
    [`add${entitySingularTitle.value}`]: addEntity,
    [`update${entitySingularTitle.value}`]: updateEntity,
    [`updateLocal${entitySingularTitle.value}`]: updateListEntity,
    [`delete${entitySingularTitle.value}`]: deleteEntity,
    [`delete${entitySingularTitle.value}ById`]: deleteEntityById,
    [`load${entityTitle.value}`]: loadEntity,
    [`load${entitySingularTitle.value}ById`]: loadEntityById,
  }
}
