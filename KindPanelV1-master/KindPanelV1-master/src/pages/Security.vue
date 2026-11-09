<template>
  <CreateUserModal v-model="showCreateUserModal" :mobile="selectedMobile" />
  <!-- INFORMATION -->
  <q-item
    class="absolute-top-left"
    style="z-index: 20000; left: 320px; top: 3px"
  >
    <div class="flex flex-center" style="height: 45px">
      <q-btn
        flat
        dense
        rounded
        color="grey"
        icon="o_info"
        @mouseover="showUsersInfo = true"
        @mouseleave="showUsersInfo = false"
      />
    </div>
    <div
      class="row no-wrap bg-grey-2 rounded-borders items-center text-caption text-grey-8 q-pa-sm q-ml-sm"
      v-if="showUsersInfo"
    >
      <q-avatar size="30px" fontSize="22px" icon="o_admin_panel_settings" />
      <div class="column q-ml-xs">
        <div class="text-black text-weight-bold text-no-wrap">
          {{ panelUsersCount }}
          {{ panelUsersCount === 1 ? "gestor" : "gestores" }}
          {{ "en uso" }}
        </div>
        <div class="text-no-wrap">
          {{ leftPanelUsersCount }}
          {{
            leftPanelUsersCount === 1 ? "gestor restante" : "gestores restantes"
          }}
        </div>
      </div>
    </div>
    <div
      class="row no-wrap bg-grey-2 rounded-borders items-center text-caption text-grey-8 q-pa-sm q-ml-sm"
      v-if="showUsersInfo"
    >
      <q-avatar size="30px" fontSize="22px" icon="o_assignment_ind" />
      <div class="column q-ml-xs">
        <div class="text-black text-weight-bold text-no-wrap">
          {{ mobileUsersCount }}
          {{ mobileUsersCount === 1 ? "repartidor" : "repartidores" }}
          {{ "en uso" }}
        </div>
        <div class="text-no-wrap">
          {{ leftMobileUsersCount }}
          {{
            leftMobileUsersCount === 1
              ? "repartidor restante"
              : "repartidores restantes"
          }}
        </div>
      </div>
    </div>
  </q-item>

  <!-- PAGE -->
  <div v-if="selectedMobile" class="page-container">
    <!-- USER -->
    <div class="text-overline text-weight-regular text-grey-6">USUARIO</div>
    <div class="row items-center q-gutter-x-md">
      <div class="text-h4 text-weight-light">
        {{
          `${selectedUser.name || ""} ${selectedUser.lastName || ""}`.trim() ||
          selectedUser.username
        }}
      </div>
      <q-badge color="green" v-if="selectedUser.isActive">Activo</q-badge>
      <q-badge color="red" v-else>Inactivo</q-badge>
      <q-space />
      <q-btn no-caps unelevated color="grey-3" text-color="grey-8">
        <div class="row items-center q-gutter-x-sm">
          <q-icon name="o_edit" size="20px" />
          <div>Editar</div>
        </div>
        <q-menu v-model="showUpdateMenu">
          <q-list style="min-width: 100px">
            <q-item class="column q-gutter-y-sm">
              <q-input
                dense
                outlined
                v-model="userData.username"
                label="Nombre de usuario"
              />
              <q-input dense outlined v-model="userData.name" label="Nombre" />
              <q-input
                dense
                outlined
                v-model="userData.lastName"
                label="Apellido"
              />
              <q-input dense outlined v-model="userData.email" label="Email" />
            </q-item>
            <q-item class="column">
              <q-btn
                unelevated
                color="primary"
                label="Confirmar"
                @click="handleUpdateUserData"
              />
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
      <q-btn
        no-caps
        unelevated
        color="grey-3"
        text-color="grey-8"
        icon="more_horiz"
      >
        <q-menu>
          <q-list style="min-width: 100px">
            <q-item clickable v-close-popup @click="handleChangePassword">
              <q-item-section avatar>
                <q-avatar icon="password" />
              </q-item-section>
              <q-item-section> Cambiar contraseña </q-item-section>
            </q-item>
            <q-separator />
            <q-item clickable v-close-popup @click="toggleIsActive">
              <q-item-section avatar>
                <q-avatar
                  :icon="
                    selectedUser.isActive
                      ? 'o_do_not_disturb_on'
                      : 'o_check_circle'
                  "
                />
              </q-item-section>
              <q-item-section>
                {{ selectedUser.isActive ? "Inactivar" : "Activar" }}
              </q-item-section>
            </q-item>
            <!-- <q-separator />
            <q-item clickable v-close-popup @click="handleDeleteUser">
              <q-item-section avatar>
                <q-avatar text-color="red" icon="o_delete" />
              </q-item-section>
              <q-item-section class="text-red">Eliminar</q-item-section>
            </q-item> -->
          </q-list>
        </q-menu>
      </q-btn>
    </div>
    <div class="column">
      <div class="row items-center">
        <div
          v-if="selectedUser.username"
          class="row items-center q-gutter-x-xs q-mr-sm"
        >
          <q-icon name="o_person" color="grey-7" size="14px" />
          <div class="text-capion text-grey-8 q-mr-xs">
            {{ selectedUser.username }}
          </div>
        </div>
        <div
          v-if="selectedUser.email"
          class="row items-center q-gutter-x-xs q-mr-sm"
        >
          <q-icon name="o_mail" color="grey-8" size="14px" />
          <div class="text-capion text-grey-7">{{ selectedUser.email }}</div>
        </div>
        <div
          v-if="selectedUser.isPanelUser"
          class="row items-center q-gutter-x-xs q-mr-sm"
        >
          <q-icon name="o_admin_panel_settings" color="grey-8" size="14px" />
          <div class="text-capion text-grey-8 q-mr-xs">Gestor</div>
        </div>
        <div
          v-if="selectedUser.isMobileUser"
          class="row items-center q-gutter-x-xs"
        >
          <q-icon name="o_assignment_ind" color="grey-8" size="14px" />
          <div class="text-capion text-grey-8 q-mr-xs">Chofer</div>
        </div>
      </div>
    </div>
    <!--

        MOBILE

    -->
    <div
      v-if="mobile && selectedUser.isMobileUser"
      class="page-section-item row justify-start items-center q-gutter-x-md full-width"
    >
      <q-avatar
        icon="o_local_shipping"
        size="4em"
        color="grey-3"
        text-color="grey-6"
      />
      <div class="row justify-between items-center grow-1">
        <div class="column">
          <div class="row items-center q-gutter-x-sm">
            <div class="text-body1 text-weight-light">{{ mobile.name }}</div>
          </div>
          <!--<div class="row items-center">
            <div class="row items-center q-gutter-x-xs q-mr-sm">
              <q-icon v-if="user.email" name="fingerprint" color="grey-7" size="14px" />
              <div class="text-capion text-grey-8 q-mr-xs">{{user.username}}</div>
            </div>
            <div class="row items-center q-gutter-x-xs">
              <q-icon v-if="user.email" name="o_mail" color="grey-8" size="14px" />
              <div v-if="user.email" class="text-capion text-grey-7">{{user.email}}</div>
            </div>
          </div>-->
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
              <div class="text-weight-light">Cambiar móvil</div>
            </template>
            <MobileSelectorForUser @select="handleAssingMobileToUser" />
          </q-btn-dropdown>
          <q-btn flat round icon="more_vert" color="grey-8" size="11px">
            <q-menu class="text-grey-8">
              <q-list>
                <q-item clickable @click="handleRemoveMobile">
                  <q-item-section avatar>
                    <q-avatar icon="o_person_off" />
                  </q-item-section>
                  <q-item-section> Remover asignación de móvil </q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
        </div>
      </div>
    </div>
    <!-- NOT ASSIGNED MOBILE CASE -->
    <EmptyListFace v-else-if="!assigning && selectedUser.isMobileUser">
      <div>
        Este usuario todavía no tiene un <strong>móvil</strong> asignado
      </div>
      <template v-slot:footer>
        <q-btn color="primary" class="q-mt-sm">
          <div>Asignar un móvil</div>
          <q-menu fit anchor="top middle" self="bottom middle" auto-close>
            <MobileSelectorForUser @select="handleAssingMobileToUser" />
          </q-menu>
        </q-btn>
      </template>
    </EmptyListFace>
  </div>
</template>

<script setup>
import { computed, ref, reactive, watch } from "vue"
import { useMobiles, useUsers, useSession, useUI } from "src/context"
import EmptyListFace from "src/components/includes/EmptyListFace"
import CreateUserModal from "src/components/mobileUser/CreateUserModal"
import MobileSelectorForUser from "src/components/mobile/MobileSelectorForUser"
import { useQuasar } from "quasar"

const showCreateUserModal = ref(false)
const assigning = ref(false)
const showUsersInfo = ref(false)
const { mobiles, selectedMobile, updateMobile } = useMobiles()
const { selectedUser, selectUser, users, deleteUser, updateUser } = useUsers()
const { user } = useSession()
const { showSuccessMessage, showErrorMessage } = useUI()

const $q = useQuasar()

const mobile = computed(() =>
  mobiles.value.find((m) => m.user == selectedUser.value.id)
)

const showUpdateMenu = ref(false)
const userData = reactive({
  username: user.value.username,
  name: user.value.name,
  lastName: user.value.lastName,
  email: user.value.email,
})

function setUserData() {
  if (!selectedUser.value) return
  const splicedUsername = selectedUser.value.username.split(".").splice(1)
  userData.username =
    splicedUsername.length > 0
      ? splicedUsername.join(".")
      : selectedUser.value.username
  userData.name = selectedUser.value.name
  userData.lastName = selectedUser.value.lastName
  userData.email = selectedUser.value.email
}
setUserData()
watch(selectedUser, () => setUserData())

async function handleRemoveMobile() {
  await updateMobile({ id: mobile.value.id, user: null })
}
async function handleAssingMobileToUser() {
  assigning.value = true
  if (mobile.value) await updateMobile({ id: mobile.value.id, user: null })
  await updateMobile({ id: m.id, user: selectedUser.value.id })
  assigning.value = false
}

const mobileUsersCount = computed(
  () => users.value.filter((user) => user.isMobileUser && user.isActive).length
)
const leftMobileUsersCount = computed(() =>
  Math.max(0, user.value.company.maxMobileUsers - mobileUsersCount.value)
)
const panelUsersCount = computed(
  () => users.value.filter((user) => user.isPanelUser && user.isActive).length
)
const leftPanelUsersCount = computed(() =>
  Math.max(0, user.value.company.maxPanelUsers - panelUsersCount.value)
)

async function handleDeleteUser() {
  try {
    const { error } = await deleteUser(selectedUser.value)
    if (!error) selectUser(users.value[0])
  } catch (e) {}
}

async function toggleIsActive() {
  await updateUser({
    id: selectedUser.value.id,
    isActive: !selectedUser.value.isActive,
  })
}

async function handleUpdateUserData() {
  showUpdateMenu.value = false
  await updateUser({
    id: selectedUser.value.id,
    ...userData,
  })
  showSuccessMessage("Usuario modificado correctamente")
}

async function handleChangePassword() {
  $q.dialog({
    title: "Cambiar contraseña",
    message: "Ingrese la nueva contraseña del usuario",
    prompt: {
      model: "",
      label: "Contraseña",
      type: "text", // optional
    },
    cancel: true,
    persistent: true,
    ok: {
      label: "Confirmar",
    },
  }).onOk(async (data) => {
    const { error } = await updateUser({
      id: selectedUser.value.id,
      password: data,
    })
    if (error) showErrorMessage("No fue posible modificar la contraseña")
    else showSuccessMessage("Contraseña modificada")
  })
}
</script>
