<template>
  <!-- LOGOUT BUTTON -->
  <q-btn v-if="tabIsTake" @click="closeSession()" rounded
    class="bg-red text-white q-ma-md q-px-sm row items-center go-back-btn"
  >
    <q-icon name="arrow_back" size="22px"/>
    <div v-if="isInitPhoto" class="ml-5 q-pr-sm">Cerrar sesión</div>
  </q-btn>
  <!-- GO BACK BUTTON -->
  <q-btn v-else @click="tab='take'" round
    class="bg-primary text-white q-ma-md q-px-sm row items-center go-back-btn"
  >
    <q-icon name="arrow_back" size="22px"/>
  </q-btn>

  <q-tab-panels v-model="tab" animated>

    <q-tab-panel name="take">
      <!-- TAKE PHOTO PICTURE INFO -->
      <div class="q-pa-md text-center" style="height:calc(100vh - 140px)">
        <q-img src="../assets/take_photo.jpg" spinner-color="white" class="q-mb-md info-img"
          :style="isInitPhoto?'transform:rotate(6deg)':'transform:rotate(-6deg)'" />
        <div class="text-primary q-mb-sm q-mt-md fs-25"><strong>Toma una foto</strong></div>
        <div class="text-grey-8 fs-16">
          <span v-if="isInitPhoto">Captura el medidor de kilometraje de tu vehículo antes de <strong>empezar</strong> el recorrido de hoy</span>
          <span v-else>Captura el medidor de kilometraje de tu vehículo para <strong>terminar</strong> el recorrido de hoy</span>
        </div>
      </div>
      <!-- TAKE PHOTO PICTURE BUTTON -->
      <div class="column items-center">
        <q-btn rounded color="primary" @click="takePhoto" class="row items-center fs-16" label="Tomar foto" />
      </div>
    </q-tab-panel>

    <q-tab-panel name="verify">
      <div style="height:calc(100vh - 140px)">
        <!-- CAPTURED PHOTO -->
        <q-img :src="`data:image/jpeg;base64,${photo}`" spinner-color="white" class="mt-5 photo" />

        <!-- INPUT -->
        <div class="full-width">
          <q-input v-model="verificationText" :disable="sendingVerification" 
            type="number" class="full-width" autofocus
            ref="num-input" placeholder="Ej.: 45820"
            label="Ingrese el valor del kilometraje (solo números)" />
        </div>
      </div>

      <!-- FINALIZE BUTTON -->
      <div class="column items-center">
        <q-btn rounded color="primary" @click="finalizeVerification">
          <div class="row items-center p-5" style="font-size:16px">
            <q-spinner v-if="sendingVerification" class="mr-5" color="white" />
            <span>{{sendingVerification?'Finalizando':'Finalizar'}}</span>
          </div>
        </q-btn>
      </div>
    </q-tab-panel>

  </q-tab-panels>  
  
  <!-- CURRENT STEP -->
  <div class="column items-center">
    <div class="q-mt-lg row justify-between" style="width:40px">
      <q-icon color="primary" name="radio_button_checked"/>
      <q-icon :color="tabIsTake ? 'black' : 'primary'" :name="tabIsTake ? 'radio_button_unchecked' : 'radio_button_checked'"/>
    </div>
  </div>
</template>

<script>
import { useRouter, useRoute } from 'vue-router'
import { defineComponent, computed, ref } from 'vue'
import { useSession, useUI } from 'src/context'
import { capturePhoto } from 'src/helpers'

export default defineComponent({
  setup() {
    const route = useRoute()
    const router = useRouter()
    const { logout } = useSession()
    const { showErrorMessage } = useUI()

    const tab = ref('take')
    const photo = ref(null)

    const closeSession = () => { logout(); router.replace('/login') }
    const goToDash = () => router.replace({ path: '/' })

    // STATUS
    const isInitPhoto = computed(_ => route.params.status === 'init')

    // PHOTO
    const takePhoto = async () => {
      
      // TODO: DELETE NEXT THREE LINES
      tab.value = 'verify'
      photo.value = '---'
      return
      
      
      const { data, error } = await capturePhoto()
      if (error) {
        // TODO: SHOW ERROR MESSAGE
        return
      }
      
      // UPDATE PHOTO STATUS

      // if (isInitPhoto.value) updateInitialPhoto({ file: data })
      // else updateFinalPhoto({ file: data })
      
      tab.value = 'verify'
    }

    // VERIFICATION
    const sendingVerification = ref(false)
    const verificationText = ref("")
    const finalizeVerification = async () => {
      if (!verificationText.value) {
        showErrorMessage("El kilometraje no puede quedar vacío")
        return
      }
      
      sendingVerification.value = true
      await new Promise(resolve => setTimeout(resolve, 1500))
      goToDash()
    }

    return {
      tabIsTake: computed(() => tab.value === 'take'),
      tab,
      photo,
      isInitPhoto,
      verificationText,
      sendingVerification,
      finalizeVerification,
      closeSession,
      takePhoto,
      goToDash,
    }
  },
})
</script>

<style scoped>
.go-back-btn {
  position:absolute;
  z-index:1000;
  left:0;
}
.info-img {
  height:240px;
  max-width:240px;
  border-radius:10px;
}
.photo {
  height:80vw;
  max-width:100%;
  border-radius:10px;
}
</style>