<template>
  <div
    class="column items-center full-width justify-between q-gutter-x-xs q-gutter-y-sm"
  >
    <div
      class="q-pa-sm row full-width items-center q-gutter-x-xs q-gutter-x-sm bg-white"
    >
      <q-btn
        v-if="!hideMapOptions"
        flat
        round
        dense
        no-caps
        :icon="showSearchAddress ? 'close' : 'o_pageview'"
        class="text-grey-8"
        :class="{ 'bg-grey-4': showSearchAddress }"
        @click="
          () => {
            showSettingsMenu = false;
            showSearchAddress = !showSearchAddress;
          }
        "
      >
        <q-tooltip> Buscar clientes </q-tooltip>
      </q-btn>
      <q-btn
        v-if="!hideMapOptions"
        flat
        round
        dense
        no-caps
        :icon="showSettingsMenu ? 'close' : 'o_map'"
        :class="{ 'bg-grey-4': showSettingsMenu }"
        class="text-grey-8"
        @click="
          () => {
            showSettingsMenu = !showSettingsMenu;
            showSearchAddress = false;
          }
        "
      >
        <q-tooltip>Configurar vista de mapa</q-tooltip>
      </q-btn>
      <div
        v-if="!hideMapOptions"
        class="row items-center rounded-borders bg-grey-3 overflow-hidden"
        style="border-radius: 15px"
      >
        <q-btn flat dense no-caps @click="centerMap" class="bg-grey-3 q-px-sm">
          Centrar mapa
        </q-btn>
        <q-separator vertical />
        <q-btn
          flat
          dense
          no-caps
          @click="reloadMap"
          icon="restart_alt"
          class="bg-grey-3 q-px-xs"
        />
      </div>
      <q-space />
      <!--<q-btn flat dense round icon="o_notifications" />-->
      <!-- <q-btn
        flat
        dense
        round
        color="grey-8"
        icon="o_smartphone"
        style="transform: rotate(20deg)"
        @click="handleShowApp"
      /> -->
      <q-btn
        flat
        dense
        round
        color="grey-8"
        :icon="showSessionMenu ? 'close' : 'o_person'"
        @click="showSessionMenu = !showSessionMenu"
      />
    </div>
    <div
      v-if="showSessionMenu"
      class="bg-white q-pa-sm row full-width items-center q-gutter-x-xs q-gutter-x-sm"
    >
      <UserMenu />
    </div>
    <div
      v-if="showSettingsMenu && !hideMapOptions"
      class="bg-white q-pa-sm row full-width items-center q-gutter-x-xs q-gutter-x-sm"
    >
      <EditableMapOptionsMenu />
    </div>
    <div
      v-if="showSearchAddress && !hideMapOptions"
      class="bg-white q-pa-sm row full-width items-center q-gutter-x-xs q-gutter-x-sm"
    >
      <AddressesSearcherMenu />
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import { useUI, useSession, useSettings } from "src/context";
import EditableMapOptionsMenu from "src/components/map/EditableMapOptionsMenu";
import AddressesSearcherMenu from "src/components/map/AddressesSearcherMenu";
import UserMenu from "src/components/security/UserMenu";

export default {
  props: ["hideMapOptions"],
  components: { EditableMapOptionsMenu, UserMenu, AddressesSearcherMenu },
  setup() {
    const { centerMap, reloadMap, showSessionMenu, showAppFrame } = useUI();
    const { showSettingsMenu, showSearchAddress } = useSettings();
    const { logout } = useSession();
    const router = useRouter();

    const handleLogout = () => {
      logout();
      router.push({ name: "Login" });
    };
    const handleShowApp = () => {
      console.log("1. handleShowApp");
      showAppFrame.value = true;
    };

    return {
      reloadMap,
      centerMap,
      handleLogout,
      handleShowApp,
      showSessionMenu,
      showSettingsMenu,
      showSearchAddress,
    };
  },
};
</script>
