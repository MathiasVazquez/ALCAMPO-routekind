<template>
  <slot
    name="pre"
    :entity="entity"
    :selected="isSelected"
    :color="entityColor"
    :hovered="hovered"
  />
  <!-- <q-btn flat dense class="q-pa-noen q-ma-none full-width" v-ripple="''">
  <slot name="menu" /> -->
  <q-item
    clickable
    :style="[
      outline ? 'border:1px solid #ccc' : '',
      dense ? 'margin:0;padding: 0 4px' : '',
    ]"
    @click="
      () => {
        selectEntity(entity)
        $emit('click', entity)
      }
    "
    class="basic-item"
    :class="[
      isSelected
        ? [
            'basic-item-selected',
            selectedClass,
            { 'basic-item-selected-slice': slice },
          ]
        : unselectedClass,
    ]"
  >
    <!-- @mouseover="hovered=true"
    @mouseleave="hovered=false" -->
    <slot
      name="in"
      :entity="entity"
      :selected="isSelected"
      :color="entityColor"
      :hovered="hovered"
    />
    <div
      v-if="isSelected"
      class="side-bar"
      :style="`background-color:${entityColor}`"
    ></div>
    <q-item-section avatar class="q-pa-none" style="min-width: 45px">
      <!--<div class="text-grey-1 flex flex-center rounded-borders" style="width:40px;height:40px"
        :style="`background-color:${getRandomColor()}`"
      >
        {{entityShortName}}
      </div>-->
      <slot name="avatar">
        <q-avatar
          size="35px"
          :style="`background-color:${entityColor}`"
          text-color="grey-1 text-weight-light"
        >
          {{ entityShortName }}
          <slot name="inavatar" />
        </q-avatar>
      </slot>
    </q-item-section>
    <q-item-section>
      <slot
        name="upper"
        :entity="entity"
        :selected="isSelected"
        :hovered="hovered"
      />
      <q-item-label title class="row q-gutter-x-sm items-center">
        <slot
          name="before"
          :entity="entity"
          :selected="isSelected"
          :hovered="hovered"
        />
        <slot name="label" :hovered="hovered">
          <div v-if="readonly" class="text-grey-9" style="flex-grow: 1">
            {{ readonly }}
          </div>
          <ItemNameInput
            v-else
            v-model:focus="nameInputFocused"
            :updateHandler="entityManager.updateEntity"
            :selectedItem="selectedEntity"
            :currentItem="entity"
            :alias="alias"
            :showLabelName="true"
          />
        </slot>
        <slot :entity="entity" :selected="isSelected" :hovered="hovered" />
      </q-item-label>
      <slot
        name="under"
        :entity="entity"
        :selected="isSelected"
        :hovered="hovered"
      />
    </q-item-section>
    <q-item-section side>
      <slot
        name="side"
        :entity="entity"
        :selected="isSelected"
        :color="entityColor"
        :hovered="hovered"
      />
    </q-item-section>
    <slot
      name="final"
      :entity="entity"
      :selected="isSelected"
      :hovered="hovered"
    />
  </q-item>
  <!-- </q-btn> -->
</template>

<script>
import { toRefs, ref, computed } from "vue"
import ItemNameInput from "src/components/includes/ItemNameInput"
import ItemOptionsBtn from "src/components/includes/ItemOptionsBtn"
import { getRandomColor } from "src/utils/statics"

export default {
  components: { ItemOptionsBtn, ItemOptionsBtn, ItemNameInput },
  props: [
    "entity",
    "index",
    "unselectable",
    "entityManager",
    "alias",
    "color",
    "shortNameFilter",
    "readonly",
    "showLabelName",
    "selectedClass",
    "unselectedClass",
    "outline",
    "slice",
    "cancelSelect",
    "dense",
  ],
  emits: ["mouseover", "mouseleave", "click"],
  setup(props) {
    const {
      entity,
      index,
      unselectable,
      entityManager,
      alias,
      color,
      showLabelName,
      cancelSelect,
    } = toRefs(props)
    const nameInputFocused = ref(false)

    const isSelected = computed(
      () => selectedEntity.value && entity.value.id === selectedEntity.value.id
    )
    const aliasedName = computed(
      () => `${alias.value}${entity.value?.id ? " " + entity.value.id : ""}`
    )
    const selectedEntity = computed(
      () => !unselectable.value && entityManager.value.selectedEntity.value
    )
    const entityShortName = computed(() =>
      (props.shortNameFilter
        ? props.shortNameFilter(entity.value)
        : `${(entity.value?.name || aliasedName.value)[0]}${
            ((entity.value?.name || aliasedName.value).split(" ")[1] ||
              "")[0] || (entity.value?.name || aliasedName.value)[1]
          }`
      ).toUpperCase()
    )
    const entityColor = computed(
      () =>
        color.value ||
        getRandomColor(
          (entity.value?.id || index.value) +
            (entity.value?.name ||
              entity.value?.clientId ||
              entityShortName.value)
        )
    )

    const hovered = ref(false)

    const selectEntity = () => {
      if (unselectable.value) return
      if (cancelSelect.value && selectedEntity.value?.id === entity.value.id)
        entityManager.value.selectEntity(null)
      else entityManager.value.selectEntity(entity.value)
    }

    return {
      alias,
      entity,
      hovered,
      isSelected,
      entityColor,
      selectEntity,
      showLabelName,
      entityManager,
      selectedEntity,
      entityShortName,
      nameInputFocused,
      getRandomColor,
    }
  },
}
</script>

<style scoped>
.side-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 5px;
  height: 100%;
  background-color: red;
  z-index: 10;
}
</style>
