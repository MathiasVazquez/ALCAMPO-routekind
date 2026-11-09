<template>
  <q-dialog v-model="showAddVisitModal" maximized persistent transition-show="slide-up" transition-hide="slide-down">
    <q-layout container class="bg-white">
      <!--<q-toolbar class="bg-white text-black">
        <div class="row items-center q-gutter-x-sm">
          <q-btn flat round color="grey-8" icon="arrow_back" @click="showAddVisitModal=false" />
          <div class="text-h6 text-weight-light">Registrar una nueva visita</div>
        </div>
      </q-toolbar>-->

      <!--<q-card-section>
        <div>1: Preguntar si se visitó o no al cliente</div>
        <div>2.1: Si se visitó, pedir que ingrese factura si se hizo una entrega manual</div>
        <div>2.2: Si no se visitó, pedir que ingrese la razón y preguntar si va a volver más tarde o ya no
          (Si elige que no, se quita del mapa)</div>
        <div>3. Adjuntar archivo o tomar foto opcionalmente</div>
      </q-card-section>-->

      <q-page-container>
        <q-page class="q-pa-md q-gutter-y-sm scroll" style="height:calc(100vh - 200px)">

          <div class="column">
            <div class="text-h6">¿Hiciste una entrega al cliente?</div>
            <div class="row justify-between full-width q-my-md">
              <q-btn flat class="opt-btn-long q-px-sm overflow-hidden"
                :style="`border:${visited?'3':'1'}px solid ${visited ? '#4caf50':'#ccc'}`"
                @click="visited=true"
              >
                <div class="full-width full-height row items-end text-h5">
                  <div :class="visited ? 'text-green' : 'text-grey-9 text-weight-light'">SÍ</div>
                  <q-avatar size="60px" round icon="check" style="transform:translate(10px, -10px)"
                    class="absolute-top-right text-white" :class="visited?'bg-green':'bg-grey-4'"
                  />
                </div>
              </q-btn>

              <q-btn flat class="opt-btn-long q-px-sm overflow-hidden"
                :style="`border:${visited===false?'3':'1'}px solid ${visited===false ? '#f44336':'#ccc'}`"
                @click="visited=false"
              >
                <div class="full-width full-height row items-end text-h5">
                  <div :class="visited===false?'text-red':'text-grey-9 text-weight-light'">NO</div>
                  <q-avatar size="60px" round icon="close" style="transform:translate(10px, -10px)"
                    class="absolute-top-right text-white" :class="visited===false?'bg-red':'bg-grey-4'"
                  />
                </div>
              </q-btn>
            </div>
          </div>

          <!-- VISITED -->
          <div v-if="visited" class="q-gutter-y-md">
            <!-- SELECT RELATED ORDER -->
            <div v-if="addressOrders.length > 0" class="q-gutter-y-sm">
              <div class="text-h6">Confirmar pedido relacionado</div>
              <div>El pedido seleccionado será marcado como entregado automáticamente.</div>
              <AddressOrderItem v-if="selectedOrder" :order="selectedOrder">
                <template #append>
                  <q-item-section side>
                    <OrderSelectorBtn :orders="addressOrders" :selected="selectedOrder" @click="selectedOrder=$event" />
                  </q-item-section>
                </template>
              </AddressOrderItem>
              <q-item v-else class="basic-item basic-item-outline">
                <q-item-section avatar>
                  <q-avatar round size="34px" color="red" text-color="white" icon="close"></q-avatar>
                </q-item-section>
                <q-item-section><strong>Ninguno</strong></q-item-section>
                <q-item-section side>
                  <OrderSelectorBtn :orders="addressOrders" :selected="selectedOrder" @click="selectedOrder=$event" />
                </q-item-section>
              </q-item>
            </div>

            <div class="column q-gutter-y-sm">
              <div class="text-h6">¿Dejaste factura?</div>
              <div>En caso de haberlo hecho, completa la numeración de la factura.</div>
              <q-input v-model="invoiceNumber" outlined label="Número de factura" placeholder="001-001-00005" />
            </div>

            <div class="column q-gutter-y-sm">
              <div class="text-h6">Deja una observación</div>
              <q-input v-model="visitMessage" outlined type="textarea" label="Nota" placeholder="Hice factura manual porque la impresora no funciona" />
            </div>
          </div>
          <!-- NOT VISITED -->
          <div v-else-if="visited===false" class="q-gutter-y-md">
            <div class="q-gutter-y-sm column">
              <div class="text-h6">¿Por qué no finalizaste la entrega?</div>
              <div>Seleccione una opción o ingrese un texto manualmente indicando la razón.</div>
              <q-input outlined v-model="notVisitMessage" type="textarea" placeholder="Escribe aquí">
                <template #append>
                    <q-btn flat round color="black" icon="arrow_drop_down">
                      <q-menu auto-close>
                        <q-list separator>
                          <q-item v-for="mess of notVisitMessages" :key="mess" clickable @click="notVisitMessage=mess">
                            <q-item-section>{{mess}}</q-item-section>
                          </q-item>
                        </q-list>
                      </q-menu>
                    </q-btn>
                </template>
              </q-input>
            </div>
            <!-- VISIT LATER -->
            <div class="q-gutter-y-sm column">
              <div class="text-h6">¿Volverás a visitar al cliente más tarde?</div>
              <div no-caps auto-close flat class="row no-wrap items-center full-width q-px-md q-py-sm"
                style="border:1px solid #ccc" @click="visitLater=!visitLater"
              >
                <div v-if="visitLater" class="text-weight-regular row"><strong>Sí</strong>, volveré más tarde</div>
                <div v-else class="row text-weight-regular"><strong class="q-mr-xs">No</strong>volveré por hoy</div>
                <q-space />
                <q-btn flat round color="grey-8" icon="sync" />
              </div>
              <div v-if="!visitLater" class="text-caption bg-grey-3 rounded-borders q-pa-xs">
                El cliente dejará de figurar en el mapa
              </div>
            </div>
          </div>

        </q-page>
      </q-page-container>

      <q-footer class="bg-white" style="border-top:1px solid #ccc">
        <q-toolbar>
          <q-btn flat v-if="!sending" color="grey-8" @click="showAddVisitModal=false" label="Cancelar" />
          <q-space />
          <q-btn v-if="isValidVisit" flat color="primary" @click="handleAddVisit">
            <span v-if="sending">Finalizando...</span>
            <span v-else>Finalizar</span>
          </q-btn>
        </q-toolbar>
      </q-footer>

    </q-layout>
  </q-dialog>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useVisits, useAddresses, useOrders } from 'src/context'
import AddressOrderItem from 'src/components/orders/AddressOrderItem'
import OrderSelectorBtn from 'src/components/orders/OrderSelectorBtn'

const notVisitMessages = ref([
  'Nadie en casa / local cerrado',
  'No tiene suficiente dinero',
  'Pasa para otro día',
])
const contactTypes = ref([
  'No contacté con el cliente',
  'En el lugar establecido',
  'Llamada recibida',
  'Llamada realizada',
  'Whatsapp recibido',
  'Whatsapp enviado',
  'Mensaje de texto recibido',
  'Mensaje de texto enviado',
])

export default {
  components: {AddressOrderItem, OrderSelectorBtn},
  setup() {
    const { showAddVisitModal, addVisit } = useVisits()
    const { getOrdersByAddressId } = useOrders()
    const { selectedAddress } = useAddresses()
    const sending = ref(null)

    const visited = ref(null)
    const visitLater = ref(false)
    const visitMessage = ref("")
    const invoiceNumber = ref("")
    const notVisitMessage = ref("")
    const contactMessage = ref(contactTypes.value[0])

    const isValidVisit = computed(() => visited.value !== null)

    const addressOrders = computed(() => getOrdersByAddressId(selectedAddress.value?.id).filter(p => !p.hasDelivered.value))
    const selectedOrder = ref(addressOrders.value[0])
    watch([addressOrders, showAddVisitModal], () => selectedOrder.value = addressOrders.value[0])
    watch([selectedOrder, visited], () => invoiceNumber.value = selectedOrder.value?.invoiceNumber || '')

    watch(showAddVisitModal, () => {
      if (!showAddVisitModal.value) return
      visited.value = null
      visitMessage.value = ""
      invoiceNumber.value = ""
      notVisitMessage.value = ""
    })

    const handleAddVisit = async () => {
      if (sending.value || !isValidVisit.value) return
      sending.value = true
      await addVisit({
        customerAddress: selectedAddress.value.id,
        invoiceNumber: visited.value ? invoiceNumber.value : null,
        message: visited.value ? visitMessage.value : notVisitMessage.value,
        // contactMessage: visited.value ? null : contactMessage.value,
        order: selectedOrder.value?.id,
        visitLater: visitLater.value,
        visited: visited.value
      })
      sending.value = false
      showAddVisitModal.value = false
    }

    return {
      sending,
      visited,
      visitLater,
      isValidVisit,
      contactTypes,
      visitMessage,
      selectedOrder,
      addressOrders,
      invoiceNumber,
      handleAddVisit,
      contactMessage,
      notVisitMessage,
      notVisitMessages,
      showAddVisitModal,
    }
  },
}
</script>

<style scoped>
.opt-btn-long {
  width: calc(50% - 5px);
  height: 70px;
}
</style>
