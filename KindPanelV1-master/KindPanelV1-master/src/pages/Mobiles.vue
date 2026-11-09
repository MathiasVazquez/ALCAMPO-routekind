<template>
  <CreateUserModal v-model="showCreateUserModal" :mobile="selectedMobile" />
  <div v-if="selectedMobile" class="page-container">
    <!-- MOBILE -->
    <div class="text-overline text-weight-regular text-grey-6">MÓVIL</div>
    <div class="row items-center q-gutter-x-md">
      <div class="text-h4 text-weight-light">{{ selectedMobile.name }}</div>
      <q-badge color="green" v-if="selectedMobile.isActive">Activo</q-badge>
      <q-badge color="red" v-else>Inactivo</q-badge>
      <q-space />
      <!-- <q-btn no-caps unelevated color="grey-3" text-color="grey-8">
                <div class="row items-center q-gutter-x-sm">
                    <q-icon name="o_edit" size="20px" />
                    <div>Editar</div>
                </div>
            </q-btn> -->
      <q-btn
        no-caps
        unelevated
        color="grey-3"
        text-color="grey-8"
        icon="more_horiz"
      >
        <q-menu>
          <q-list style="min-width: 100px">
            <q-item clickable v-close-popup @click="confirmDeleteMobile">
              <q-item-section avatar>
                <q-avatar text-color="red" icon="o_delete" />
              </q-item-section>
              <q-item-section class="text-red">Eliminar</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </div>
    <!--

            USER

        -->
    <div
      v-if="user"
      class="page-section-item row justify-start items-center q-gutter-x-md full-width"
    >
      <q-avatar icon="o_person" size="4em" color="grey-3" text-color="grey-6" />
      <div class="row justify-between items-center grow-1">
        <div class="column">
          <div class="row items-center q-gutter-x-sm">
            <div class="text-body1 text-weight-light">
              {{ user.name }} {{ user.lastName }}
            </div>
          </div>
          <div class="row items-center">
            <div class="row items-center q-gutter-x-xs q-mr-sm">
              <q-icon
                v-if="user.username"
                name="o_person"
                color="grey-7"
                size="14px"
              />
              <div class="text-capion text-grey-8 q-mr-xs">
                {{ user.username }}
              </div>
            </div>
            <div class="row items-center q-gutter-x-xs">
              <q-icon
                v-if="user.email"
                name="o_mail"
                color="grey-8"
                size="14px"
              />
              <div v-if="user.email" class="text-capion text-grey-7">
                {{ user.email }}
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center">
          <q-btn-dropdown
            no-caps
            flat
            dense
            rounded
            auto-close
            class="q-pl-md"
            color="grey-7"
          >
            <template #label>
              <div class="text-weight-light">Cambiar usuario</div>
            </template>
            <UserSelector />
          </q-btn-dropdown>
          <q-btn flat round icon="more_vert" color="grey-8" size="11px">
            <q-menu class="text-grey-8">
              <q-list>
                <q-item clickable @click="handleRemoveUser">
                  <q-item-section avatar>
                    <q-avatar icon="o_person_off" />
                  </q-item-section>
                  <q-item-section>
                    Remover asignación de usuario
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
    </div>
    <!-- NOT ASSIGNED USER CASE -->
    <EmptyListFace v-else @click="showCreateUserModal = true">
      <div>
        Este móvil todavía no tiene un <strong>usuario</strong> asignado
      </div>
      <template v-slot:footer>
        <q-btn color="primary" class="q-mt-sm">
          <div>Asignar un usuario</div>
          <q-menu fit anchor="top middle" self="bottom middle" auto-close>
            <UserSelector />
          </q-menu>
        </q-btn>
      </template>
    </EmptyListFace>

    <!--

            WAREHOUSE

        -->
    <div
      v-if="warehouse"
      class="page-section-item row justify-start items-center q-gutter-x-md full-width"
    >
      <q-avatar icon="o_home" size="4em" color="grey-3" text-color="grey-6" />
      <div class="row justify-between items-center grow-1">
        <div class="column">
          <div class="row items-center q-gutter-x-sm">
            <div class="text-body1 text-weight-light">{{ warehouse.name }}</div>
          </div>
        </div>
        <div class="row items-center">
          <q-btn-dropdown
            no-caps
            flat
            dense
            rounded
            auto-close
            class="q-pl-md"
            color="grey-7"
          >
            <template #label>
              <div class="text-weight-light">Cambiar almacén</div>
            </template>
            <WarehouseSelector />
          </q-btn-dropdown>
          <q-btn flat round icon="more_vert" color="grey-8" size="11px">
            <q-menu class="text-grey-8">
              <q-list>
                <q-item clickable @click="handleRemoveWarehouse">
                  <q-item-section avatar>
                    <q-avatar icon="not_interested" />
                  </q-item-section>
                  <q-item-section>
                    Remover asignación de almacén
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
    </div>
    <!-- NOT ASSIGNED WAREHOUSE CASE -->
    <EmptyListFace v-else>
      <div>
        Este móvil todavía no tiene un <strong>almacén</strong> asignado
      </div>
      <template v-slot:footer>
        <q-btn color="primary" class="q-mt-sm">
          <div>Asignar un almacén</div>
          <q-menu fit anchor="top middle" self="bottom middle" auto-close>
            <WarehouseSelector />
          </q-menu>
        </q-btn>
      </template>
    </EmptyListFace>

    <!--

            INVOICE CONFIG

        -->
    <div
      v-if="invoiceConfig"
      class="page-section-item row justify-start items-center q-gutter-x-md full-width"
    >
      <q-avatar
        icon="o_description"
        size="4em"
        color="grey-3"
        text-color="grey-6"
      />
      <div class="row justify-between items-center grow-1">
        <div class="column">
          <div class="row items-center q-gutter-x-sm">
            <div class="text-body1 text-weight-light">
              {{ invoiceConfig.name }}
            </div>
          </div>
          <div class="row items-center">
            <div class="row items-center q-gutter-x-xs q-mr-sm">
              <q-icon name="bookmark_border" color="grey-7" size="14px" />
              <div class="text-capion text-grey-8 q-mr-xs">
                {{ invoiceConfig.stamped }}
              </div>
            </div>
            <div class="row items-center q-gutter-x-xs">
              <q-icon name="numbers" color="grey-8" size="14px" />
              <div class="text-capion text-grey-7">
                {{ invoiceConfig.serialNumber }}
              </div>
            </div>
          </div>
        </div>
        <div class="row items-center">
          <q-btn-dropdown
            no-caps
            flat
            dense
            rounded
            auto-close
            class="q-pl-md"
            color="grey-7"
          >
            <template #label>
              <div class="text-weight-light">Cambiar facturación</div>
            </template>
            <InvoiceConfigSelector />
          </q-btn-dropdown>
          <q-btn flat round icon="more_vert" color="grey-8" size="11px">
            <q-menu class="text-grey-8">
              <q-list>
                <q-item clickable @click="handleRemoveInvoiceConfig">
                  <q-item-section avatar>
                    <q-avatar icon="not_interested" />
                  </q-item-section>
                  <q-item-section>
                    Remover asignación de facturación
                  </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
    </div>
    <!-- NOT ASSIGNED INVOICE CONFIG CASE -->
    <EmptyListFace v-else>
      <div>
        Este móvil todavía no tiene una <strong>facturación</strong> asignada
      </div>
      <template v-slot:footer>
        <q-btn color="primary" class="q-mt-sm">
          <div>Asignar un facturación</div>
          <q-menu fit anchor="top middle" self="bottom middle" auto-close>
            <InvoiceConfigSelector />
          </q-menu>
        </q-btn>
      </template>
    </EmptyListFace>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import EmptyListFace from "src/components/includes/EmptyListFace";
import CreateUserModal from "src/components/mobileUser/CreateUserModal";
import {
  useMobiles,
  useUsers,
  useWarehouses,
  useInvoiceConfigs,
} from "src/context";
import WarehouseSelector from "src/components/warehouse/WarehouseSelector";
import UserSelector from "src/components/security/UserSelector";
import InvoiceConfigSelector from "src/components/invoices/InvoiceConfigSelector";
import { useQuasar } from "quasar";

const showCreateUserModal = ref(false);
const { selectedMobile, updateMobile, deleteMobile, selectMobile, mobiles } =
  useMobiles();
const { warehouses, getWarehouseById } = useWarehouses();
const { invoiceConfigs, getInvoiceConfigById } = useInvoiceConfigs();
const { users, getUserById } = useUsers();
const $q = useQuasar();

const user = computed(() => getUserById(selectedMobile.value?.user));
const warehouse = computed(() =>
  getWarehouseById(selectedMobile.value?.warehouse)
);
const invoiceConfig = computed(() =>
  getInvoiceConfigById(selectedMobile.value?.invoiceConfig)
);

const handleRemoveUser = async () =>
  await updateMobile({ id: selectedMobile.value.id, user: null });
const handleRemoveWarehouse = async () =>
  await updateMobile({ id: selectedMobile.value.id, warehouse: null });
const handleRemoveInvoiceConfig = async () =>
  await updateMobile({ id: selectedMobile.value.id, invoiceConfig: null });

async function confirmDeleteMobile() {
  await deleteMobile(selectedMobile.value);
  selectMobile(mobiles.value[0]);
}
</script>
