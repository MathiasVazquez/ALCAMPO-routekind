<template>
  <div
    class="full-height column items-center bg-white"
    style="width: 50px; max-width: 50px"
  >
    <slot name="top" />
    <div class="column flex-center">
      <q-btn
        flat
        icon="route"
        class="options-btn"
        :to="{ name: 'Index' }"
        :replace="true"
        :class="pageNameIs('Index') ? 'text-primary' : 'text-grey-5'"
      >
        <q-tooltip>Zonas</q-tooltip>
      </q-btn>
      <q-btn
        flat
        icon="o_local_shipping"
        class="options-btn"
        :to="{ name: 'Mobiles' }"
        :replace="true"
        :class="pageNameIs('Mobiles') ? 'text-primary' : 'text-grey-5'"
      >
        <q-tooltip>Móviles</q-tooltip>
      </q-btn>
      <!-- <q-btn flat icon="alt_route"
        class="options-btn" :to="{name:'Planning'}" :replace="true"
        :class="pageNameIs('Planning')?'text-primary':'text-grey-5'"
      >
        <q-tooltip>Planificaciones</q-tooltip>
      </q-btn> -->
      <q-btn
        flat
        icon="o_admin_panel_settings"
        class="options-btn"
        :to="{ name: 'Security' }"
        :replace="true"
        :class="pageNameIs('Security') ? 'text-primary' : 'text-grey-5'"
      >
        <q-tooltip>Usuarios y seguridad</q-tooltip>
      </q-btn>
    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { computed } from "vue";
export default {
  setup() {
    const route = useRoute();

    const pageNameIs = (name) => route.name === name;
    const pageName = computed((_) => route.name);

    return {
      pageName,
      pageNameIs,
    };
  },
};
</script>

<style scoped>
.options-btn {
  width: 50px;
  height: 50px;
  border-radius: 0;
}
</style>
