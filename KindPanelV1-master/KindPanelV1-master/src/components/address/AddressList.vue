<template>
  <div>
    <GenericEntityItem
      v-for="(address, index) of addresses.filter(Boolean)"
      :key="address?.id || index"
      :entity="address"
      :entityManager="customerAddressesManager"
      selectedClass="bg-grey-3"
      :unselectable="true"
      :dense="dense"
      @click="$emit('click', address)"
    >
      <template #label>
        <div class="column">
          <div class="q-pa-xs">
            {{ address.customer.fullName || "Sin nombre" }}
          </div>
          <slot name="bottom-label" :address="address" :index="index" />
        </div>
      </template>
      <template #final>
        <q-item-section side>
          <slot name="side" :address="address" :index="index" />
        </q-item-section>
      </template>
      <template #under>
        <!-- <div>{{ address.id }}</div> -->
        <q-list class="row">
          <q-item-label
            v-for="(day, index) of getAddressActiveDays(address) || []"
            :key="index"
            caption
            class="row text-grey-8 q-pa-xs q-mr-sm q-mt-xs rounded-borders items-center"
            style="border: 1px solid #ccc"
          >
            <div class="q-mr-xs">{{ day.name }}</div>
          </q-item-label>
        </q-list>
      </template>
    </GenericEntityItem>
    <!-- EMPTY LIST MESSAGE -->
    <EmptyListFace v-if="addresses.length === 0 && !hideEmptyFace">
      <slot name="empty"> No hay ningún cliente </slot>
    </EmptyListFace>
  </div>
</template>

<script>
import { useCustomerAddresses } from "src/context"
import GenericEntityItem from "src/components/includes/GenericEntityItem"
import EmptyListFace from "src/components/includes/EmptyListFace"
import { weekDays } from "src/utils/statics"

export default {
  components: { EmptyListFace, GenericEntityItem },
  props: ["addresses", "hideEmptyFace", "dense"],
  emits: ["click"],
  setup(props) {
    const { customerAddressesManager } = useCustomerAddresses()

    function getAddressActiveDays(address) {
      const dayCodes = address.activeDays
      // const dayCodes = ["0", "1"];
      const dayCodesArr = !dayCodes
        ? []
        : typeof dayCodes === "string"
        ? dayCodes.split(",")
        : dayCodes
      return dayCodesArr
        .map((c) => weekDays.find((d) => `${d.code}` === `${c}`))
        .sort((a, b) => (a.code > b.code ? 1 : a.code < b.code ? -1 : 0))
    }

    return {
      customerAddressesManager,
      getAddressActiveDays,
    }
  },
}
</script>
