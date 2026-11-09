<template>
  <q-item clickable @click="selectVisit(visit)">
    <q-item-section avatar>
      <GenericEntityAvatar :alias="address?.customer?.fullName || 'CO'" size="28px" />
    </q-item-section>

    <q-item-section>
      <q-item-label class="text-subtitle2 column q-gutter-y-xs" style="margin-bottom:-2px">
        <!-- NUMBER -->
        <div>{{address?.customer?.fullName || 'CLIENTE OCASIONAL'}}</div>
      </q-item-label>
      <!-- CUSTOMER NAME -->
      <!--<q-item-label class="text-weight-light text-grey-8 text-body2">
        {{invoice.customerFiscalName || 'CLIENTE OCASIONAL'}}
      </q-item-label>-->
      <q-item-label v-if="visit.message">
        <div class="row">
          <div class="row bg-grey-3 rounded-borders q-pa-xs">
            <div class="text-caption">{{visit.message}}</div>
          </div>
        </div>
      </q-item-label>

      <q-item-label>
        <div class="row items-center q-gutter-x-sm">
          <!-- DATE -->
          <div class="flex items-center">
            <q-icon color="grey-9" name="schedule" />
            <div class="text-weight-light text-grey-8 text-caption q-ml-xs">
              <span v-if="showDate">
                {{moment(visit.checkDate).fromNow()}}
              </span>
              <span v-else>
                {{moment(visit.checkDate).fromNow()}}
              </span>
            </div>
          </div>
          <!-- INVOICE NUMBER -->
          <div v-if="visit.invoiceNumber" class="flex items-center">
            <q-icon color="grey-9" name="o_receipt_long" />
            <div class="text-weight-light text-grey-8 text-caption q-ml-xs">{{visit.invoiceNumber}}</div>
          </div>
        </div>
      </q-item-label>
    </q-item-section>

    <q-item-section side top>
      <div class="row items-center rounded-borders text-white text-caption q-px-sm"
        :class="visit.visited ? 'bg-green' : 'bg-red'"
      >
        <!--<q-icon size="22px" class="text-white" :color="visit.visited ? 'green' : 'red'" :name="visit.visited ? 'check' : 'close'" />-->
        <div v-if="visit.visited">Visitado</div>
        <div v-else>No visitado</div>
      </div>
    </q-item-section>
  </q-item>
  <q-separator />
</template>

<script>
import { ref, computed } from 'vue'
import { useVisits, useConfirmModal, useAddresses } from 'src/context'
import GenericEntityAvatar from 'src/components/includes/GenericEntityAvatar'

import moment from 'moment'
import 'moment/locale/es'
moment.locale('es')

export default {
  props: ['visit'],
  components: {GenericEntityAvatar},
  setup(props) {
    const { selectVisit, selectedVisit } = useVisits()
    const { getAddressById } = useAddresses()
    const { showConfirmModal } = useConfirmModal()

    const address = computed(() => getAddressById(props.visit.customerAddress))

    const showDate = ref(true)
    setInterval(() => { showDate.value = !showDate.value }, 60000)

    return {
      moment,
      showDate,

      address,
      selectVisit,
      selectedVisit,
    }
  },
}
</script>

<style scoped>
.bottom-union-line {
  position: absolute;
  width: 1px;
  z-index: 999;
  left: 51px;
  height: 36px;
  background-color: transparent;
  transform: translateY(48px);
  /*transform: translateY(47px);*/
}
</style>
