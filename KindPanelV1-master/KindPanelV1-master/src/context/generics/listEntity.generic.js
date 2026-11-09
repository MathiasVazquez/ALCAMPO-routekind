import { store } from "src/store/local.store"
import { ref, computed, toRefs } from "vue"
import { useUI, useConfirmModal, authHeader, BASE_URL } from ".."
import axios from "axios"

export const useGenericEntityList = (entityList, options) => {
  const { showSuccessMessage, showErrorMessage } = useUI()
  const { showConfirmModal } = useConfirmModal()
  const { entityName, entityNameSingular, entityUrl, selectedEntity } =
    toRefs(options)
  const formatter = options?.formatter || ((e) => e)

  const entityTitle = computed(
    () =>
      `${(entityName.value[0] + "").toUpperCase()}${entityName.value.slice(1)}`
  )
  const entitySingularTitle = computed(
    () =>
      `${(
        entityNameSingular.value[0] + ""
      ).toUpperCase()}${entityNameSingular.value.slice(1)}`
  )

  const setEntity = (value) => {
    // console.log('--> setEntity', entityName.value)
    entityList.value = value
    store.set(entityName.value, value)
  }
  const updateListEntity = (entityToUpdate) => {
    // console.log('--> updateListEntity', entityName.value)
    const entities = [].concat(entityToUpdate)
    for (let entity of entities) {
      setEntity(
        entityList.value.map((c) =>
          `${c.id}` === `${entity.id}` ? { ...c, ...entity } : c
        )
      )
      if (selectedEntity && `${entity.id}` === `${selectedEntity.value?.id}`)
        selectEntity({ ...selectedEntity.value, ...entity }, false)
    }
  }
  const createOrReplaceEntityList = (list) => {
    // console.log('--> createOrReplaceEntityList', entityName.value)
    if (!list || list.length === 0) return
    const resultAdded = []
    for (let entity of [].concat(list).concat(entityList.value))
      if (!resultAdded.some((e) => e.id === entity.id)) resultAdded.push(entity)
    setEntity(resultAdded)
  }
  const selectEntity = (value, updateList = true) => {
    if (selectedEntity) {
      if (
        options.deselectOnSelfSelection &&
        value &&
        selectedEntity.value?.id === value.id
      )
        selectedEntity.value = null
      else
        selectedEntity.value = value
          ? entityList.value.find((e) => e.id === value.id)
          : null
      // if (updateList && selectedEntity.value) updateListEntity(selectedEntity.value)
    }
  }

  const getEntityById = (id) => {
    // console.log('--> getEntityById', entityName.value)
    return formatter(
      entityList.value.find((c) => `${c.id}` === `${id}`),
      entityList.value
    )
  }

  const addEntity = async (request) => {
    try {
      const { data } = await axios.post(
        `${BASE_URL}${entityUrl.value}`,
        request,
        authHeader.value
      )
      createOrReplaceEntityList(data)
      if (options.onPost)
        options.onPost({ data, request, manager: entityManager })
      return { data }
    } catch (error) {
      showErrorMessage("No fue posible realizar la creación")
      if (options.onPost) options.onPost({ error, manager: entityManager })
      return { error }
    }
  }

  const updateEntity = async (request, updateList = true) => {
    const _update = async (_request, _updateList) => {
      try {
        const { data } = await axios.put(
          `${BASE_URL}${entityUrl.value}${_request.id}/`,
          _request,
          authHeader.value
        )
        if (_updateList) updateListEntity(data)
        return { data }
      } catch (error) {
        showErrorMessage("No fue posible realizar la modificación")
        return { error }
      }
    }

    if (Array.isArray(request)) {
      const results = []
      for (let _request of request)
        if (!!_request) results.push(await _update(_request, false))
      for (let result of results) updateListEntity(result.data)
      return results
    } else return await _update(request, updateList)
  }

  const deleteEntity = async (request, deleteOptions) => {
    const confirDeleteEntity = async () => {
      try {
        const { data } = await axios.delete(
          `${BASE_URL}${entityUrl.value}${request.id}/`,
          authHeader.value
        )
        setEntity(entityList.value.filter((c) => c.id !== request.id))
        createOrReplaceEntityList(data)
        if (options?.onDelete)
          options.onDelete({ request, data, manager: entityManager })
        return { data }
      } catch (error) {
        showErrorMessage("No fue posible realizar la eliminación")
        if (options?.onDelete)
          options.onDelete({ error, manager: entityManager })
        return { error }
      }
    }
    return await new Promise(async (resolve) => {
      if (options.confirmDeleteMessage) {
        showConfirmModal({
          text: options.confirmDeleteMessage,
          color: "primary",
          errorMessage: "No fue posible realizar la eliminación",
          onConfirm: async () => {
            if (deleteOptions?.onConfirm) deleteOptions?.onConfirm()
            resolve(await confirDeleteEntity())
          },
        })
      } else {
        if (deleteOptions?.onConfirm) deleteOptions?.onConfirm()
        resolve(await confirDeleteEntity())
      }
    })
  }

  const deleteEntityById = async (id) => {
    return await deleteEntity({ id })
  }

  const loadEntity = async () => {
    try {
      const { data } = await axios.get(
        `${BASE_URL}${entityUrl.value}`,
        authHeader.value
      )
      setEntity(data)
      return { data }
    } catch (error) {
      if (![401, 403].includes(error?.response?.status))
        showErrorMessage("No fue posible obtener la lista")
      return { error }
    }
  }

  const formattedEntityList = computed(() => {
    // console.log('--> formattedEntityList', entityName.value)
    let result = entityList.value
    result =
      options && options.listFilter ? result.filter(options.listFilter) : result
    result =
      options && options.formatter
        ? result.map((e) => options.formatter(e, entityList.value))
        : result
    result =
      options && options.listSort ? result.sort(options.listSort) : result
    return result
  })
  const formattedEntityListNotFilter = computed(() => {
    // console.log('--> formattedEntityList', entityName.value)
    let result = entityList.value
    result =
      options && options.formatter
        ? result.map((e) => options.formatter(e, entityList.value))
        : result
    // result = options && options.listSort ? result.sort(options.listSort) : result
    return result
  })
  const formattedSelectedEntity = computed(() => {
    // console.log('--> formattedSelectedEntity', entityName.value)
    const selected = selectedEntity.value
      ? getEntityById(selectedEntity.value.id)
      : null
    const entity = options.canDeselectEntity
      ? selected
      : selected || entityList.value[0]
    return entity && formatter(entity, entityList.value)
  })
  // selectedEntity.value ? (selectedEntity.value.__cancelSelection ? null : selectedEntity.value) : entityList.value[0])
  const entityManager = {
    entityList: formattedEntityList,
    selectedEntity: formattedSelectedEntity,
    selectEntity,
    setEntity,
    getEntityById,
    addEntity,
    updateEntity,
    deleteEntity,
    deleteEntityById,
    loadEntity,
  }

  return {
    manager: entityManager,
    [`${entityName.value}Manager`]: entityManager,
    [`${entityName.value}`]: formattedEntityList,
    [`all${entityTitle.value}`]: formattedEntityListNotFilter,
    [`selected${entitySingularTitle.value}`]: formattedSelectedEntity,
    [`select${entitySingularTitle.value}`]: selectEntity,
    [`set${entityTitle.value}`]: setEntity,
    [`get${entitySingularTitle.value}ById`]: getEntityById,
    [`add${entitySingularTitle.value}`]: addEntity,
    [`update${entitySingularTitle.value}`]: updateEntity,
    [`updateLocal${entitySingularTitle.value}`]: updateListEntity,
    [`delete${entitySingularTitle.value}`]: deleteEntity,
    [`delete${entitySingularTitle.value}ById`]: deleteEntityById,
    [`load${entityTitle.value}`]: loadEntity,
  }
}
