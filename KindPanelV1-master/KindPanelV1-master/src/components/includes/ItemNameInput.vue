<template>
  <q-input
    borderless
    dense
    autogrow
    v-if="isSelected && !disabled"
    ref="nameInputRef"
    @blur="discardNewName"
    @focus="$emit('update:focus', true)"
    v-model="newName"
    :label="showLabelName ? label : undefined"
    :error="!!errorMessage"
    :error-message="errorMessage"
    :bottom-slots="false"
    :hide-bottom-space="true"
    :disable="updating"
    :loading="updating"
    no-error-icon
  >
    <template v-slot:append v-if="nameHasChange && !updating">
      <q-btn
        flat
        dense
        round
        icon="close"
        color="greey-9"
        size="10px"
        @click="discardNewName"
      >
        <q-tooltip>Descartar</q-tooltip>
      </q-btn>
      <q-btn
        flat
        dense
        round
        icon="save"
        color="primary"
        size="10px"
        @click="saveNewName"
      >
        <q-tooltip>Guardar</q-tooltip>
      </q-btn>
    </template>
  </q-input>
  <q-item-label v-else class="q-py-xs text-grey-9">
    {{ nameAlias }}
  </q-item-label>
</template>

<script>
import { computed, watch, ref, toRefs, nextTick } from "vue"

export default {
  props: [
    "focus",
    "disabled",
    "updateHandler",
    "currentItem",
    "selectedItem",
    "alias",
    "showLabelName",
  ],
  emits: ["update:focus", "save"],
  setup(props, { emit }) {
    const { focus, currentItem, selectedItem, alias, disabled, showLabelName } =
      toRefs(props)
    const { updateHandler } = props

    const nameInputRef = ref(null)

    const originalName = ref(currentItem.value.name)
    const newName = ref(currentItem.value.name)
    const errorMessage = ref("")
    const updating = ref(false)

    const requestFocus = () =>
      focus.value &&
      nameInputRef.value &&
      setTimeout(nameInputRef.value.focus, 10)

    const saveNewName = async () => {
      updating.value = true
      errorMessage.value = ""

      const { error } = await updateHandler({
        id: selectedItem.value.id,
        name: newName.value,
      })

      if (error)
        errorMessage.value = "Error al cambiar de nombre, vuelva a intentarlo"
      else {
        originalName.value = newName.value
        emit("update:focus", false)
        emit("save", newName.value)
      }
      updating.value = false
    }
    const discardNewName = () => {
      errorMessage.value = ""
      if (!updating.value) newName.value = originalName.value
      emit("update:focus", false)
    }

    watch(focus, requestFocus)
    watch(newName, (_) => (errorMessage.value = ""))
    watch(
      currentItem,
      () => (newName.value = originalName.value = currentItem.value.name)
    )

    const nameHasChange = computed((_) => newName.value !== originalName.value)
    const isSelected = computed(
      (_) =>
        selectedItem.value && currentItem.value.id === selectedItem.value.id
    )
    const nameAlias = computed(
      (_) => currentItem.value.name || `${alias.value} ${currentItem.value.id}`
    )
    const label = computed((_) =>
      currentItem.value.name ? "Nombre" : nameAlias.value
    )

    return {
      label,
      newName,
      nameHasChange,
      saveNewName,
      discardNewName,
      nameInputRef,
      errorMessage,
      isSelected,
      nameAlias,
      disabled,
      updating,
      showLabelName,
    }
  },
}
</script>

<style scoped></style>
