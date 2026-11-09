<template>
  <div class="row items-center full-width justify-between q-gutter-x-xs">
    <div class="q-pa-sm row items-center q-gutter-x-xs">
      <div v-for="option of options" :key="option.id">
        <q-btn
          v-if="option.onClick"
          rounded
          dense
          :disable="option.disable"
          :flat="!option.selected"
          :color="option.selected ? 'primary' : 'grey-7'"
          :icon="option.icon"
          @click="option.onClick"
        >
          {{ option.text }}
          <q-tooltip>{{ option.message }}</q-tooltip>
        </q-btn>
        <div v-else class="q-px-sm">{{ option.text }}</div>
      </div>
    </div>

    <q-space />
    <div
      style="border-left: 1px solid #ddd"
      class="q-pa-sm bg-grey-1 text-grey-8"
    >
      <q-btn
        rounded
        flat
        dense
        @click="showPolygonEditor = false"
        icon="close"
      ></q-btn>
    </div>

    <q-dialog v-model="showCode" persistent>
      <q-card style="width: 600px">
        <q-card-section class="text-body1"> Vértices </q-card-section>
        <!-- <q-card-section class="row items-center">
          <div class="row">
            <div>{{ selectedPolygon.listOfPoints }}</div>
            <q-btn  color="primary" icon="edit" />
          </div>
        </q-card-section> -->
        <q-card-section class="row items-center">
          <q-input
            v-model="editingVertices"
            outlined
            autogrow
            class="full-width"
          />
        </q-card-section>
        <q-card-actions align="between" class="items-center">
          <q-btn no-caps flat label="Cancelar" color="grey-7" v-close-popup />
          <q-btn
            v-if="isValidListOfVertices"
            no-caps
            flat
            label="Confirmar"
            color="primary"
            @click="handleReplaceVertices"
            :loading="savingVertices"
          />
          <div v-else class="row">
            <div
              class="q-mt-md q-pa-sm rounded-borders bg-red text-white text-weight-bold"
            >
              Código inválido.
            </div>
          </div>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { computed, watch, ref } from "vue"
import { usePolygons, usePolygonPins } from "src/context"

const showCode = ref(false)
const { showPolygonEditor, selectedPolygonEditorOption, selectedPolygon } =
  usePolygons()

const { deletePolygonPin, addPolygonPin } = usePolygonPins()

const selectedPolygonHasVertices = computed(
  () => selectedPolygon.value?.polygonPins.value.length > 0
)

const editingVertices = ref("")
const savingVertices = ref(false)

async function handleReplaceVertices() {
  if (!isValidListOfVertices.value) return
  if (
    editingVertices.value !==
    JSON.stringify(selectedPolygon.value.listOfPoints.value)
  ) {
    savingVertices.value = true
    // Delete old vertices
    await Promise.all(
      selectedPolygon.value.polygonPins.value.map((pin) =>
        deletePolygonPin(pin)
      )
    )
    // Add new vertices
    const vertices = JSON.parse(editingVertices.value)
    let prevCreatedVertexId = null
    for (const vertex of vertices) {
      const { data } = await addPolygonPin({
        lat: vertex[0],
        lng: vertex[1],
        polygon: selectedPolygon.value.id,
        prev: prevCreatedVertexId,
      })
      prevCreatedVertexId = data.id
    }
  }
  savingVertices.value = false
  showCode.value = false
}

const options = computed(() => [
  {
    id: 1,
    icon: "o_pin_drop",
    message: "Mover (W)",
    disable: !selectedPolygonHasVertices.value,
    selected: selectedPolygonEditorOption.value === "edit",
    onClick: () => (selectedPolygonEditorOption.value = "edit"),
  },
  {
    id: 2,
    message: "Agregar (E)",
    icon: "o_add_location_alt",
    selected: selectedPolygonEditorOption.value === "add",
    onClick: () => (selectedPolygonEditorOption.value = "add"),
  },
  {
    id: 3,
    icon: "o_wrong_location",
    message: "Eliminar (R)",
    disable: !selectedPolygonHasVertices.value,
    selected: selectedPolygonEditorOption.value === "delete",
    onClick: () => (selectedPolygonEditorOption.value = "delete"),
  },
  {
    id: 4,
    text: "|",
  },
  // {
  //   id: 5,
  //   icon: "o_local_library",
  //   onClick: () => {},
  // },
  {
    id: 6,
    icon: "code",
    message: "Código",
    onClick: () => {
      showCode.value = true
      editingVertices.value = JSON.stringify(
        selectedPolygon.value.listOfPoints.value
      )
    },
  },
])

watch(
  selectedPolygon,
  () =>
    !selectedPolygonHasVertices.value &&
    (selectedPolygonEditorOption.value = "add")
)

const onKeyPress = (e) => {
  switch (e.code) {
    case "KeyW":
      selectedPolygonEditorOption.value = "edit"
      break
    case "KeyE":
      selectedPolygonEditorOption.value = "add"
      break
    case "KeyR":
      selectedPolygonEditorOption.value = "delete"
      break
  }
}
watch(showPolygonEditor, () => {
  if (showPolygonEditor.value) document.addEventListener("keypress", onKeyPress)
  else document.removeEventListener("keypress", onKeyPress)
})

const isValidListOfVertices = computed(() => {
  try {
    const _json_vertices = JSON.parse(editingVertices.value)
    for (const vertex of _json_vertices) {
      if (vertex.length !== 2) return false
    }
    return true
  } catch {
    return false
  }
})
</script>
