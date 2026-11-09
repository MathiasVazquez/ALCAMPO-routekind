import { ref, computed } from "vue";
import { store } from "src/store/local.store";
import { useGenericEntityList } from "./generics/listEntity.generic";

const mobiles = ref(store.get("mobiles", []));
const selectedMobile = ref(null);
const selectedMobileList = ref(
  store.get(
    "selectedMobileList",
    mobiles.value[0]
      ? [{ label: mobiles.value[0].name, value: mobiles.value[0].id }]
      : []
  )
);

export const useMobiles = () => {
  const options = ref({
    entityName: "mobiles",
    entityNameSingular: "mobile",
    entityUrl: "mobile/",
    selectedEntity: selectedMobile,
    confirmDeleteMessage: "¿Está seguro/a de que desea eliminar el móvil?",
    formatter: (mobile) => {
      return {
        ...mobile,
        visible: computed(
          () =>
            mobile.lat &&
            mobile.lng &&
            selectedMobileList.value.some((m) => m.value === mobile.id)
        ),
      };
    },
  });

  return {
    ...useGenericEntityList(mobiles, options.value),
    selectedMobileList: computed({
      get: () => selectedMobileList.value,
      set: (value) => {
        selectedMobileList.value = value;
        store.set("selectedMobileList", value);
      },
    }),
  };
};
