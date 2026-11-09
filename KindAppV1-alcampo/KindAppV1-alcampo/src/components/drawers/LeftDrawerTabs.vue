<template>
  <div class="column no-wrap" style="height:100vh">

    <q-toolbar class="bg-white row items-center">
      <div class="row items-center q-gutter-x-sm">
        <q-btn flat round color="grey-8" icon="arrow_back" @click="showLeftDrawer=false" />
      </div>
      <q-space />
      <q-btn dense flat round class="bg-grey-4" color="grey-9">
        <q-icon name="o_person" />
        <q-menu>
          <q-list>
            <q-item clickable @click="handleLogout">
              <q-item-section avatar>
                <q-avatar icon="logout" />
              </q-item-section>
              <q-item-section>
                Cerrar sesión
              </q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </q-toolbar>

    <q-tab-panels v-model="tab" animated style="flex-grow:1">
      <q-tab-panel name="addresses" class="q-pa-none">
        <AddressList />
      </q-tab-panel>

      <q-tab-panel name="orders" class="q-pa-none">
        <OrderList />
      </q-tab-panel>

      <q-tab-panel name="visits" class="q-pa-none">
        <VisitList />
      </q-tab-panel>

      <q-tab-panel name="invoices" class="q-pa-none">
        <InvoiceList />
      </q-tab-panel>

    </q-tab-panels>

    <!-- style="box-shadow:0 0 20px 10px #2372"-->
    <q-separator />
    <q-tabs
      v-model="tab"
      switch-indicator
      indicator-color="transparent"
      class="text-grey-8 q-py-xs"
      align="justify"
    >
      <q-tab v-for="t of tabs" :key="t.name" no-caps round
        :name="t.name" :ripple="false"
      >
        <div v-if="false && tab===t.name" class="bg-primary text-white q-pa-sm shadow-6 relative-position" style="border-radius:10px">
          <q-icon size="28px" :name="tab===t.name ? t.selectedIcon : t.icon"></q-icon>
        </div>
        <div v-else :class="{'text-primary': tab===t.name}">
          <q-icon size="28px" :name="tab===t.name ? t.selectedIcon : t.icon"></q-icon>
          <div>{{t.label}}</div>
        </div>
      </q-tab>
    </q-tabs>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useUI, useSession } from 'src/context'
import { useRouter } from 'vue-router'
import AddressList from 'src/components/addresses/AddressList'
import OrderList from 'src/components/orders/OrderList'
import VisitList from 'src/components/visits/VisitList'
import InvoiceList from 'src/components/invoices/InvoiceList'

const tabs = ref([
  { name: "addresses", icon: "o_people", selectedIcon: "people", label: "Clientes" },
  { name: "orders", icon: "o_inventory", selectedIcon: "o_inventory", label: "Pedidos" },
  { name: "visits", icon: "rule", selectedIcon: "rule", label: "Visitas" },
  { name: "invoices", icon: "o_receipt_long", selectedIcon: "receipt_long", label: "Facturas" },
])

export default {
  components: {AddressList, OrderList, VisitList, InvoiceList},
  setup() {
    const { user, mobile, logout } = useSession()
    const { showLeftDrawer } = useUI()
    const tab = ref("addresses")
    const router = useRouter()

    const handleLogout = () => {
      logout()
      router.replace({ name: 'Login' })
    }

    return {
      tab,
      tabs,
      user,
      mobile,
      showLeftDrawer,
      handleLogout,
    }
  },
}
</script>
