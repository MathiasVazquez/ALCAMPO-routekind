<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="flex justify-center items-center bg-white items-center column">
        <!-- HEADER -->
        <LoginImg :scale="0.8"/>
        <div class="bg-primary q-ma-lg flex justify-center items-center assignment">
          <q-icon name="assignment" color="white" size="16px"/>
        </div>
        <div class="text-h5 text-grey-7">Autenticación</div>
        <!-- BODY -->
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent } from 'vue'
import LoginImg from 'src/components/login/LoginImg'

export default defineComponent({
  components: {LoginImg},
  setup() {
    return {

    }
  },
})
</script>

<style scoped>
.assignment {
  width:26px;
  height:26px;
  border-radius:100px;
}
</style>
