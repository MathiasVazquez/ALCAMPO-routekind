<template>
  <q-img class="full-height" src="https://cdn.quasar.dev/img/material.png">
    <div class="absolute-bottom bg-transparent">
      <q-avatar size="56px" class="q-mb-sm">
        <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
      </q-avatar>
      <div class="text-weight-bold">Nombre de la persona</div>
      <div>@username</div>
    </div>
  </q-img>
  <div class="absolute-top-right">
    <q-btn round flat icon="more_vert" color="white" class="q-ma-xs">
      <q-menu v-model="showMobileOptionsMenu" auto-close>
        <q-list bordered>
          <!-- EDIT USER -->
          <q-item v-ripple clickable>
            <q-item-section avatar>
              <q-icon name="o_manage_accounts" />
            </q-item-section>
            <q-item-section>
              <q-item-label> Modificar información </q-item-label>
            </q-item-section>
          </q-item>
          <!-- RESET PASSWORD OPTION -->
          <q-item v-ripple clickable>
            <q-item-section avatar>
              <q-icon name="lock_open" />
            </q-item-section>
            <q-item-section>
              <q-item-label> Cambiar contraseña </q-item-label>
            </q-item-section>
          </q-item>
          <!-- DISABLE USER -->
          <q-item v-ripple clickable>
            <q-item-section avatar>
              <q-icon name="o_person_off" />
            </q-item-section>
            <q-item-section>
              <q-item-label> Deshabilitar usuario </q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const showMobileOptionsMenu = ref(false);

    return {
      showMobileOptionsMenu,
    };
  },
};
</script>
