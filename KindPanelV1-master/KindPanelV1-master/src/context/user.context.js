import { ref } from "vue";
import { store } from "src/store/local.store";
import { useGenericEntityList } from "./generics/listEntity.generic";

const users = ref(store.get("users", []));
const selectedUser = ref(null);

export const useUsers = () => {
  const options = ref({
    entityName: "users",
    entityNameSingular: "user",
    entityUrl: "user/",
    selectedEntity: selectedUser,
    confirmDeleteMessage: "¿Está seguro/a de que desea eliminar el usuario?",
  });
  return useGenericEntityList(users, options.value);
};
