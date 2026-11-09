<template>
  <q-toolbar class="bg-white q-px-lg column" style="align-items: start">
    <div class="items-baseline row q-gutter-x-sm no-wrap">
      <div class="text-h5 text-weight-light"></div>
      <div class="text-h4 text-weight-bold">{{ visits.length }}</div>
      <div class="text-h5 text-weight-light">
        {{ visits.length === 1 ? "visita realizada" : "visitas realizadas" }}
      </div>
    </div>
  </q-toolbar>

  <q-list>
    <q-scroll-area
      ref="scrollAreaRef"
      class="q-mt-md"
      style="height: calc(100vh - 182px)"
      @scroll="onListScroll"
    >
      <q-item class="q-px-lg q-pb-md q-pt-none q-ma-none">
        <q-item-section>
          <div class="row items-center q-gutter-x-sm no-wrap">
            <q-input
              v-if="visits.length > 0"
              outlined
              dense
              v-model="search"
              placeholder="Buscar visita"
              style="flex-grow: 1"
            >
              <template #prepend
                ><q-icon name="search" color="grey-7"
              /></template>
            </q-input>
            <!-- <q-btn flat style="height:40px;border:1px solid #bbb" icon="sync" />
            <q-btn flat style="height:40px;border:1px solid #bbb" icon="o_filter_alt" /> -->
          </div>
        </q-item-section>
      </q-item>

      <q-separator />
      <VisitItem v-for="visit of visits" :key="visit.id" :visit="visit" />

      <div style="padding-bottom: 60px" />

      <q-page-sticky
        v-if="showGoToTopBtn"
        position="bottom-right"
        style="z-index: 100"
        :offset="[18, -40]"
      >
        <q-btn
          round
          icon="keyboard_arrow_up"
          color="primary"
          @click="setScrollPosition(0)"
        />
      </q-page-sticky>
    </q-scroll-area>
  </q-list>
</template>

<script>
import { ref, computed } from "vue"
import { useVisits } from "src/context"
import VisitItem from "./VisitItem"

export default {
  components: { VisitItem },
  setup() {
    const search = ref("")
    const scrollAreaRef = ref(null)
    const showGoToTopBtn = ref(false)
    const { visits } = useVisits()

    const sortedVisits = computed(() =>
      visits.value.sort((v1, v2) =>
        new Date(v1.checkDate) < new Date(v2.checkDate)
          ? 1
          : new Date(v1.checkDate) > new Date(v2.checkDate)
          ? -1
          : 0
      )
    )

    const onListScroll = (event) =>
      (showGoToTopBtn.value = event.verticalPosition > 100)
    const setScrollPosition = (position) =>
      scrollAreaRef.value.setScrollPosition("vertical", position, 200)

    return {
      search,
      visits: sortedVisits,
      scrollAreaRef,
      showGoToTopBtn,
      setScrollPosition,
      onListScroll,
    }
  },
}
</script>
