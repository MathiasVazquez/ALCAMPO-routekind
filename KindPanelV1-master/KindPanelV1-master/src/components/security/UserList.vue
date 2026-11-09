<template>
  <q-list class="text-black">
    <!-- HEADER -->
    <q-item class="q-pa-none column">
      <q-item-section>
        <q-item-label header overline>
          <div class="row justify-between items-center">
            <div>USUARIOS</div>
            <q-btn
              dense
              unelevated
              icon="add"
              label="Usuario"
              color="primary"
              class="q-pr-sm"
              :disable="!canCreateMobileUser && !canCreatePanelUser"
            >
              <!-- <q-tooltip>Agregar nuevo móvil</q-tooltip> -->
              <q-menu v-model="newUser.showMenu">
                <q-list bordered>
                  <q-item class="column q-gutter-sm">
                    <div class="text-caption text-grey-7 q-pa-xs">
                      Credenciales
                    </div>
                    <q-input
                      dense
                      outlined
                      autofocus
                      v-model="newUser.username"
                      label="Nombre del usuario"
                    />
                    <q-input
                      dense
                      outlined
                      v-model="newUser.password"
                      label="Contraseña"
                    />
                    <div class="row">
                      <q-btn-group outline>
                        <q-btn
                          :flat="newUser.role !== 'app'"
                          color="primary"
                          label="Repartidor"
                          @click="newUser.role = 'app'"
                          :disable="!canCreateMobileUser"
                        />
                        <q-btn
                          :flat="newUser.role !== 'panel'"
                          color="primary"
                          label="Gestor"
                          @click="newUser.role = 'panel'"
                          :disable="!canCreatePanelUser"
                        />
                      </q-btn-group>
                    </div>
                  </q-item>
                  <q-item class="column q-gutter-sm">
                    <div class="text-caption text-grey-7 q-pa-xs">
                      Información personal
                    </div>
                    <q-input
                      dense
                      outlined
                      autofocus
                      v-model="newUser.name"
                      label="Nombre"
                    />
                    <q-input
                      dense
                      outlined
                      v-model="newUser.lastName"
                      label="Apellido"
                    />
                    <q-input
                      dense
                      outlined
                      v-model="newUser.email"
                      label="Email"
                    />
                  </q-item>
                  <q-item class="column">
                    <q-btn
                      :disable="!newUser.username || !newUser.password"
                      :color="
                        !newUser.username || !newUser.password
                          ? 'grey-7'
                          : 'primary'
                      "
                      label="Crear"
                      @click="handleAddUser"
                    />
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </div>
        </q-item-label>
      </q-item-section>
    </q-item>

    <!-- USERS -->
    <GenericEntityItem
      v-for="user of users"
      :key="user.id"
      alias="Usuario"
      :entity="user"
      :readonly="user.username"
      :entityManager="usersManager"
      :shortNameFilter="shortNameFilter"
      unselectedClass="bg-grey-3"
      :slice="true"
    >
      <!--<template #after="{ entity }">
        <q-item-section v-if="entity.isMobileUser || entity.isPanelUser">
          <q-item-label v-if="entity.isMobileUser" caption class="row items-center">
            <q-icon class="q-mr-xs" color="primary" name="directions_run" />
            <span>Chofer</span>
          </q-item-label>
          <q-item-label v-if="entity.isPanelUser" caption class="row items-center">
            <q-icon class="q-mr-xs" color="primary" name="o_admin_panel_settings" />
            <span>Gestor</span>
          </q-item-label>
        </q-item-section>
      </template>-->
      <template #side>
        <q-badge color="green" v-if="user.isActive">Activo</q-badge>
        <q-badge color="red" v-else>Inactivo</q-badge>
      </template>
      <template #under>
        <q-item-label caption class="row q-gutter-x-xs">
          <div>{{ `${user.name || ""} ${user.lastName || ""}`.trim() }}</div>
          <!--<div v-if="entity.isPanelUser" class="row items-center">
            <q-icon class="q-mr-xs" name="o_lock" />
            <span>Gestor</span>
          </div>
          <div v-if="entity.isMobileUser" class="row items-center">
            <q-icon class="q-mr-xs" name="o_lock" />
            <span>Chofer</span>
          </div>-->
        </q-item-label>
      </template>
    </GenericEntityItem>
  </q-list>
</template>

<script setup>
import { reactive, computed } from "vue";
import { useUsers, useSession } from "src/context";
import GenericEntityItem from "src/components/includes/GenericEntityItem";

const newUser = reactive({
  showMenu: false,
  username: "",
  password: "",
  role: "",
  name: "",
  lastName: "",
  email: "",
});

const { user } = useSession();
const { users, usersManager, addUser, selectUser } = useUsers();
const shortNameFilter = (user) => {
  if (!user.name && !user.lastName)
    return `${user.username[0]}${user.username[1]}`;
  else if (!user.name) return `${user.lastName[0]}${user.lastName[1]}`;
  else if (!user.lastName) return `${user.name[0]}${user.name[1]}`;
  return `${user.name[0]}${user.lastName[0]}`;
};

async function handleAddUser() {
  if (!newUser.username || !newUser.password || !newUser.role) return;
  newUser.showMenu = false;
  const user = await addUser({
    ...newUser,
    email: newUser.email || null,
    isMobileUser: newUser.role === "app",
    isPanelUser: newUser.role === "panel",
  });
  newUser.username = "";
  newUser.password = "";
  newUser.role = "";
  newUser.name = "";
  newUser.lastName = "";
  newUser.email = "";
  selectUser(user);
}

const canCreatePanelUser = computed(
  () =>
    users.value?.filter((user) => user.isPanelUser && user.isActive).length <
    user.value?.company?.maxPanelUsers
);
const canCreateMobileUser = computed(
  () =>
    users.value?.filter((user) => user.isMobileUser && user.isActive).length <
    user.value?.company?.maxMobileUsers
);
</script>
