import axios from "axios";
import { ref, computed } from "vue";
import { store } from "src/store/local.store";
import { BASE_URL } from ".";

const user = ref(store.get("user", null));

export const authHeader = computed(() => {
  const { token } = user?.value || {};
  const baseHeaders = {
    "kind-version": "1.0.2",
  };
  return {
    headers: token
      ? { Authorization: `token ${token}`, ...baseHeaders }
      : { ...baseHeaders },
  };
});

export const useSession = () => {
  const setUser = (data) => {
    user.value = data;
    store.set("user", data);
  };

  const validateToken = async () => {
    try {
      return await axios.get(`${BASE_URL}validate-token/`, authHeader.value);
    } catch (error) {
      return error.response &&
        error.response.data &&
        error.response.data.error === "No se han enviado las credenciales."
        ? { error }
        : {};
    }
  };

  const login = async ({ username, password }) => {
    try {
      const { data } = await axios.post(
        BASE_URL + "login/",
        { username, password },
        authHeader.value
      );
      setUser(data[0] || data);
      return { data: data[0] || data };
    } catch (error) {
      return { error };
    }
  };

  const logout = () => {
    setUser(null);
    store.set("users", null);
    store.set("planning", null);
    store.set("selectedZone", null);
    store.set("warehouses", null);
    store.set("mobiles", null);
    store.set("selectedPlanning", null);
    store.set("selectedMobile", null);
    store.set("zones", null);
    store.set("customers", null);
    store.set("polygonPins", null);
    store.set("polygons", null);
    store.set("selectedMobiles", null);
    store.set("invoiceConfigs", null);
    store.set("selectedMobileList", null);
    store.set("addresses", null);
    store.set("settings", null);
  };

  return {
    user: computed(() => user.value),
    isLogged: computed(() => !!user.value),
    token: computed(() => user.value.token),
    validateToken,
    logout,
    login,
  };
};
