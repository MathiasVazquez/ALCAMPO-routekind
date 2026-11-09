<template>
  <q-btn round flat icon="expand_more" class="bg-grey-3 text-grey-8">
    <q-menu auto-close>
      <q-list style="width:calc(100vw - 70px)">
        <q-item v-if="selected" clickable @click="$emit('click', null)" class="q-py-md">
          <q-item-section avatar>
            <q-avatar round size="34px" color="red" text-color="white" icon="close" />
          </q-item-section>
          <q-item-section>
            <strong>Ninguno</strong>
          </q-item-section>
        </q-item>
        <AddressOrderItem v-for="order of orders.filter(o => o.id !== selected?.id)" :key="order.id" :order="order"
          @click="$emit('click', $event)"
        />
      </q-list>
    </q-menu>
  </q-btn>
</template>

<script>
import AddressOrderItem from 'src/components/orders/AddressOrderItem'

export default {
  props: ['orders', 'selected'],
  emits: ['click'],
  components: {AddressOrderItem},
  setup() {

  },
}
</script>
