<template>
  <q-toolbar class="q-px-lg column" style="align-items: start">
    <div class="items-baseline row q-gutter-x-sm no-wrap">
      <!-- <div class="text-h5 text-weight-light">Tienes</div> -->
      <div class="text-h4 text-weight-bold">{{ addresses.length }}</div>
      <div class="text-h5 text-weight-light">clientes asignados</div>
    </div>
    <div v-if="addresses.length > 0" class="full-width q-mt-sm">
      <div class="row items-center">
        <div class="text-caption text-grey-8">
          {{ finishedAddress.length }} de {{ addresses.length }} clientes
          visitados
        </div>
        <q-space />
        <div class="text-caption text-grey-8">
          {{ Math.round(listProgress * 100) }}%
        </div>
      </div>
      <q-linear-progress
        rounded
        size="10px"
        :value="listProgress"
        color="primary"
      />
    </div>
  </q-toolbar>

  <q-list>
    <q-scroll-area
      ref="scrollAreaRef"
      class="q-mt-md"
      style="height: calc(100vh - 210px)"
      @scroll="onListScroll"
    >
      <q-item class="q-px-lg q-pb-md q-pt-none q-ma-none">
        <q-item-section>
          <div class="row items-center q-gutter-x-sm no-wrap">
            <q-input
              v-if="addresses.length > 0"
              outlined
              dense
              v-model="search"
              placeholder="Buscar cliente"
              style="flex-grow: 1"
            >
              <template #prepend>
                <q-icon name="search" color="grey-7" />
              </template>
              <template v-if="search" #append>
                <q-btn
                  round
                  flat
                  icon="close"
                  color="grey-7"
                  @click="search = ''"
                />
              </template>
            </q-input>
            <!-- <q-btn
              flat
              style="height: 40px; border: 1px solid #bbb"
              icon="sync"
            /> -->
            <!-- <q-btn
              flat
              style="height: 40px; border: 1px solid #bbb"
              icon="o_filter_alt"
            /> -->
          </div>
        </q-item-section>
      </q-item>

      <q-separator />
      <q-infinite-scroll @load="onLoad" :offset="250">
        <AddressItem
          v-for="address in filteredAddresses"
          :key="address.id"
          :address="address"
        />
        <template v-slot:loading>
          <div class="row justify-center q-my-md">
            <q-spinner-dots color="primary" size="40px" />
          </div>
        </template>
      </q-infinite-scroll>
      <!-- <q-virtual-scroll :items="filteredAddresses" v-slot="{ item: address }">
        <AddressItem :key="address.id" :address="address" />
      </q-virtual-scroll> -->

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

<script setup>
import { ref, computed, nextTick } from "vue"
import { useAddresses, useVisits } from "src/context"
import AddressItem from "./AddressItem"

const search = ref("")
const showElementsCount = ref(12)
const scrollAreaRef = ref(null)
const showGoToTopBtn = ref(false)
const { getVisitsByAddressId } = useVisits()
const { addresses } = useAddresses()

const finishedAddress = computed(() =>
  addresses.value.filter((a) => getVisitsByAddressId(a.id).length > 0)
)
const listProgress = computed(
  () => finishedAddress.value.length / addresses.value.length
)

const onListScroll = (event) =>
  (showGoToTopBtn.value = event.verticalPosition > 100)
const setScrollPosition = (position) =>
  scrollAreaRef.value.setScrollPosition("vertical", position, 200)

const filteredAddresses = computed(() => {
  const result = !search.value
    ? addresses.value
    : addresses.value?.filter((a) =>
        a.customer.fullName.toLowerCase().includes(search.value.toLowerCase())
      )
  return result.slice(0, showElementsCount.value) || []
})

async function onLoad(index, done) {
  showElementsCount.value += 12
  await nextTick()
  done()
}
</script>
