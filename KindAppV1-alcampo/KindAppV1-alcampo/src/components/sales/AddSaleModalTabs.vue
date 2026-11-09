<template>
  <q-dialog
    v-model="showAddSaleModal"
    persistent
    maximized
    transition-show="slide-up"
    transition-hide="slide-down"
  >
    <q-card>
      <div class="column no-wrap" style="height: 100vh">
        <q-toolbar class="bg-white row items-center">
          <div class="row items-center q-gutter-x-sm">
            <q-btn
              flat
              round
              color="grey-8"
              icon="arrow_back"
              @click="showAddSaleModal = false"
            />
          </div>
          <q-space />
        </q-toolbar>

        <q-tab-panels v-model="tab" animated style="flex-grow: 1">
          <q-tab-panel name="customer">
            <AddSaleCustomer />
          </q-tab-panel>

          <q-tab-panel name="products" class="q-pa-none">
            <AddSaleProducts />
          </q-tab-panel>

          <q-tab-panel name="details" class="q-pa-none">
            <AddSaleDetails />
          </q-tab-panel>
        </q-tab-panels>

        <!-- style="box-shadow:0 0 20px 10px #2372"
      <q-separator />-->
        <q-tabs
          v-model="tab"
          switch-indicator
          indicator-color="transparent"
          class="text-grey-8 q-py-xs"
          align="justify"
        >
          <q-tab
            v-for="t of tabs"
            :key="t.name"
            no-caps
            round
            :name="t.name"
            :ripple="false"
          >
            <div
              v-if="false && tab === t.name"
              class="bg-primary text-white q-pa-sm shadow-6 relative-position"
              style="border-radius: 10px"
            >
              <q-icon
                size="28px"
                :name="tab === t.name ? t.selectedIcon : t.icon"
              ></q-icon>
            </div>
            <div v-else :class="{ 'text-primary': tab === t.name }">
              <q-icon
                size="28px"
                :name="tab === t.name ? t.selectedIcon : t.icon"
              ></q-icon>
              <div>{{ t.label }}</div>
            </div>
          </q-tab>
        </q-tabs>
      </div>
    </q-card>
  </q-dialog>
</template>

<script>
import { ref, watch, computed } from "vue"
import { useAddresses, useSales } from "src/context"
import AddressList from "src/components/addresses/AddressList"
import OrderList from "src/components/orders/OrderList"
import AddSaleCustomer from "src/components/sales/AddSaleCustomer"
import AddSaleProducts from "src/components/sales/AddSaleProducts"
import AddSaleDetails from "src/components/sales/AddSaleDetails"

const tabs = ref([
  {
    name: "customer",
    icon: "o_person",
    selectedIcon: "person",
    label: "Cliente",
  },
  {
    name: "products",
    icon: "o_inventory_2",
    selectedIcon: "inventory_2",
    label: "Productos",
  },
  {
    name: "details",
    icon: "o_summarize",
    selectedIcon: "summarize",
    label: "Detalles",
  },
])

export default {
  components: {
    AddressList,
    OrderList,
    AddSaleCustomer,
    AddSaleProducts,
    AddSaleDetails,
  },
  setup() {
    const { showAddSaleModal, currentSale } = useSales()
    const { selectedAddress } = useAddresses()
    const tab = ref("customer")

    // watch(currentSale, () => currentSale.value.order && (tab.value='details'))

    watch(showAddSaleModal, () => {
      if (!showAddSaleModal.value) return

      // if (!!currentSale.value._currentSale.invoiceNumber) currentSale.value.clear()
      if (!currentSale.value.order) currentSale.value.clear()

      currentSale.value = {
        ...currentSale.value,
        customer: selectedAddress.value?.customer?.id || "",
        customerFiscalName: selectedAddress.value?.customer?.fiscalName || "",
        customerDocument: selectedAddress.value?.customer?.document || "",
        customerPhone: selectedAddress.value?.customer?.mobilePrimary || "",
        customerAddress: selectedAddress.value?.description || "",
      }

      if (
        !currentSale.value.customerFiscalName ||
        !currentSale.value.customerDocument
      )
        tab.value = "customer"
      else if (currentSale.value.order) tab.value = "details"
      else tab.value = "products"
    })

    return {
      tab,
      tabs,
      showAddSaleModal,
    }
  },
}
</script>
