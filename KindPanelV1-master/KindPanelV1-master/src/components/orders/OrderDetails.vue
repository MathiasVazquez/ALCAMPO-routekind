<template>
  <!-- ADDRESS -->
  <q-item>
    <q-item-section>
      <q-item-label overline>Detalles del pedido</q-item-label>
    </q-item-section>
  </q-item>
  <q-item v-if="selectedOrder">
    <!-- CUSTOMER -->
    <q-item-section v-if="selectedOrder.customerAddress?.customer">
      <q-item-label><strong>CLIENTE</strong></q-item-label>
      <q-item-label>{{
        selectedOrder.customerAddress.customer.fiscalName
      }}</q-item-label>
    </q-item-section>
    <!-- <div>{{selectedOrder}}</div> -->
  </q-item>
  <!-- ADDRESS -->
  <q-item v-if="selectedOrder.customerAddress?.description">
    <q-item-section>
      <q-item-label><strong>DIRECCIÓN DE ENVÍO</strong></q-item-label>
      <q-item-label>{{
        selectedOrder.customerAddress.description
      }}</q-item-label>
    </q-item-section>
  </q-item>
  <!-- DETAILS -->
  <q-item>
    <q-item-section>
      <q-item-label><strong>DETALLES</strong></q-item-label>
      <div class="row" v-if="selectedOrder.invoiceNumber">
        <q-item-label>Factura a entregar</q-item-label>
        <q-space />
        <q-item-label>{{ selectedOrder.invoiceNumber }}</q-item-label>
      </div>
      <div class="row">
        <q-item-label>Condición de venta</q-item-label>
        <q-space />
        <q-item-label>{{ selectedOrder.saleCondition }}</q-item-label>
      </div>
      <div class="row">
        <q-item-label>Método de pago</q-item-label>
        <q-space />
        <q-item-label>{{ selectedOrder.paymentType }}</q-item-label>
      </div>
      <div class="row">
        <q-item-label>Monto total</q-item-label>
        <q-space />
        <q-item-label>{{ formatMoney(totalToPay, currency) }}</q-item-label>
      </div>
      <div class="row" v-if="selectedOrder.totalPayed">
        <q-item-label>Monto pagado</q-item-label>
        <q-space />
        <q-item-label>{{
          formatMoney(selectedOrder.totalPayed, currency)
        }}</q-item-label>
      </div>
      <div class="row" v-if="selectedOrder.totalPayed">
        <q-item-label>Monto a pagar</q-item-label>
        <q-space />
        <q-item-label>{{
          formatMoney(totalToPay - selectedOrder.totalPayed, currency)
        }}</q-item-label>
      </div>
    </q-item-section>
  </q-item>
  <!-- PRODUCTS -->
  <q-item class="q-mb-sm">
    <q-item-section>
      <q-item-label><strong>ÍTEMS</strong></q-item-label>
      <div v-for="item of selectedOrderDetails" :key="item.id" class="row">
        <q-item-label
          >{{ item.quantity }}x {{ item.product.productName }}</q-item-label
        >
        <q-space />
        <q-item-label>{{
          formatMoney(item.quantity * item.unitPrice, currency)
        }}</q-item-label>
      </div>
    </q-item-section>
  </q-item>
</template>

<script>
import { computed } from "vue";
import { useOrders, useProducts, useSession } from "src/context";
import { formatMoney } from "src/helpers";

export default {
  setup() {
    const { getProductById } = useProducts();
    const { selectedOrder } = useOrders();
    const { user } = useSession();

    const currency = computed(() => user?.company?.currencyUnit || "Gs.");

    return {
      currency,
      selectedOrder,
      selectedOrderDetails: computed(() =>
        selectedOrder.value.details.map((d) => {
          return { ...d, product: getProductById(d.product) };
        })
      ),
      totalToPay: computed(() =>
        selectedOrder.value.details.reduce(
          (total, d) => total + d.quantity * d.unitPrice,
          0
        )
      ),
      formatMoney,
    };
  },
};
</script>
