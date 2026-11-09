<template>
  <q-list class="text-black" style="background-color: transparent">
    <!-- HEADER -->
    <q-item class="q-pa-none column">
      <q-item-section>
        <q-item-label header overline>
          <div class="row justify-between items-center">
            <div>MÓVILES</div>
            <q-btn
              dense
              unelevated
              icon="add"
              label="Móvil"
              color="primary"
              class="q-pr-sm"
            >
              <!-- <q-tooltip>Agregar nuevo móvil</q-tooltip> -->
              <q-menu v-model="newMobile.showMenu">
                <q-list bordered>
                  <q-item class="column q-gutter-sm">
                    <q-input
                      dense
                      outlined
                      autofocus
                      v-model="newMobile.name"
                      label="Nombre del móvil"
                    />
                    <q-btn
                      no-caps
                      :disable="!newMobile.name"
                      :color="newMobile.name ? 'primary' : 'grey-7'"
                      label="Crear"
                      @click="handleAddMobile"
                    />
                  </q-item>
                </q-list>
              </q-menu>
            </q-btn>
          </div>
        </q-item-label>
      </q-item-section>
    </q-item>

    <!-- MOBILES -->
    <GenericEntityItem
      v-for="mobile of mobiles"
      :key="mobile.id"
      alias="Móvil"
      :entity="mobile"
      :entityManager="mobilesManager"
      unselectedClass="bg-grey-3"
      :slice="true"
    >
      <template #under="{ entity }">
        <q-item-section>
          <q-item-label caption>
            {{
              entity.user
                ? `${(() => {
                    const user = getUserById(entity.user)
                    return user?.fullName || user?.username
                  })()} `
                : "- Sin usuario asignado -"
            }}
          </q-item-label>
          <!--<q-item-label v-if="entity.warehouse" caption class="row">
            <div class="q-pa-xs rounded-borders text-grey-8 q-mt-xs" style="border:1px solid #999">
              {{getWarehouseById(entity.warehouse).name}}
            </div>
          </q-item-label>-->
        </q-item-section>
      </template>
    </GenericEntityItem>
  </q-list>
</template>

<script setup>
import { reactive } from "vue"
import { useMobiles, useUsers, useWarehouses } from "src/context"
import GenericEntityItem from "src/components/includes/GenericEntityItem"

const { mobiles, mobilesManager, addMobile, selectMobile } = useMobiles()
const { getUserById } = useUsers()

const newMobile = reactive({
  showMenu: false,
  name: "",
})

async function handleAddMobile() {
  if (!newMobile.name) return
  newMobile.showMenu = false
  const mobile = await addMobile({ name: newMobile.name })
  newMobile.name = ""
  selectMobile(mobile)
}
// const { getWarehouseById } = useWarehouses();
// const user = computed(() => getUserById(mobile.value?.user))
// const warehouse = computed(() => getWarehouseById(mobile.value?.warehouse))
</script>
