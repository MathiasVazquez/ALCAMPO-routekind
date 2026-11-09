<template>
  <div
    class="flex flex-center column full-width q-px-lg"
    style="max-width: 400px"
  >
    <!-- USERNAME INPUT -->

    <q-input
      v-model="username"
      dense
      autofocus
      :disable="sendingLogin"
      :ref="(el) => (usernameInput = el)"
      label="Nombre de usuario"
      class="full-width q-mt-xl login-input"
      @keypress.enter="requestLogin"
      @focus="focusUsername"
      @blur="focusUsername(false)"
      :error="!!usernameError"
      :error-message="usernameError"
    >
      <template v-slot:append>
        <q-icon
          v-if="!usernameError"
          name="person"
          :color="usernameColorIcon"
        />
      </template>
    </q-input>

    <!-- PASSWORD INPUT -->

    <q-input
      v-model="password"
      dense
      :ref="(el) => (passwordInput = el)"
      :disable="sendingLogin"
      label="Contraseña"
      class="full-width q-mt-md login-input"
      :type="hidePassword ? 'password' : 'text'"
      @keypress.enter="requestLogin"
      @focus="focusPassword"
      @blur="focusPassword(false)"
      :error="!!passwordError"
      :error-message="passwordError"
    >
      <template v-slot:append>
        <q-icon
          v-if="!passwordError"
          name="password"
          :color="passwordColorIcon"
        />
      </template>
      <!--<template v-slot:append>
        <q-icon
          :name=" hidePassword ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="hidePassword=!hidePassword"
        />
      </template>-->
    </q-input>

    <!-- SERVER ERROR MESSAGE -->

    <div class="q-ma-sm full-width">
      <div
        v-if="genericError"
        class="q-pa-xs bg-red text-white full-width br-4"
      >
        <strong>{{ genericError }}</strong>
      </div>
      <div v-else class="q-pa-xs text-white">.</div>
    </div>

    <!-- SEND LOGIN BUTTON -->

    <q-btn class="bg-primary text-white q-px-xl q-py-sm" @click="requestLogin">
      <div v-if="!sendingLogin">Iniciar sesión</div>
      <q-spinner v-else color="white" size="1em" />
    </q-btn>

    <div class="text-grey-6 q-mt-md">v1.1.10</div>

    <!-- RESET PASSWORD -->

    <!--<q-btn flat no-caps class="mt-16 underline text-primary px-64 py-4" @click="gotoResetPassword">
      <div>¿Olvidaste tu contraseña?</div>
    </q-btn>-->
  </div>
</template>

<script>
import { defineComponent, ref, computed, watch } from "vue"
import { loadAllFromServer, useSession } from "src/context"
import { useRouter } from "vue-router"

export default defineComponent({
  setup() {
    const router = useRouter()
    const focusedInput = ref(null)
    const hidePassword = ref(true)

    const { isLogged, login } = useSession()

    //
    // USER NAME
    //
    const username = ref("")
    const usernameInput = ref(null)
    const focusUsername = (state = true) => {
      if (state) focusedInput.value = usernameInput.value
      else if (focusedInput.value === usernameInput.value)
        focusedInput.value = null
    }
    const isUsernameFocus = computed(
      () => focusedInput.value === usernameInput.value,
    )
    const usernameColorIcon = computed(() =>
      usernameError.value
        ? "negative"
        : isUsernameFocus.value
          ? "primary"
          : "grey-7",
    )
    watch(
      username,
      () => loginError.value && (loginError.value.username = undefined),
    )
    //
    // PASSWORD
    //
    const password = ref("")
    const passwordInput = ref(null)
    const focusPassword = (state = true) => {
      if (state) focusedInput.value = passwordInput.value
      else if (focusedInput.value === passwordInput.value)
        focusedInput.value = null
    }
    const gotoResetPassword = () =>
      router.push({ path: `/login/resetPassword/${username.value}` })
    const isPasswordFocus = computed(
      () => focusedInput.value === passwordInput.value,
    )
    const passwordColorIcon = computed(() =>
      passwordError.value
        ? "negative"
        : isPasswordFocus.value
          ? "primary"
          : "grey-7",
    )
    watch(
      password,
      () => loginError.value && (loginError.value.password = undefined),
    )
    //
    // ERROR
    //
    const loginError = ref("")
    const usernameError = computed(() =>
      loginError.value ? loginError.value.username : "",
    )
    const passwordError = computed(() =>
      loginError.value ? loginError.value.password : "",
    )
    const genericError = computed(() =>
      loginError.value ? loginError.value.error : "",
    )
    watch(loginError, () => {
      if (!loginError.value) return
      if (loginError.value.username) usernameInput.value.focus()
      else if (loginError.value.password) passwordInput.value.focus()
    })
    //
    // LOGIN
    //
    const sendingLogin = ref(false)
    const validateLogin = () => {
      loginError.value = null
      if (!username.value)
        loginError.value = { username: "El nombre de usuario es requerido" }
      else if (!password.value)
        loginError.value = { password: "La contraseña es requerida" }
      return !loginError.value
    }
    const requestLogin = async () => {
      if (sendingLogin.value) return

      if (validateLogin()) {
        sendingLogin.value = true

        const { data, error } = await login({
          username: username.value,
          password: password.value,
        })

        if (error) {
          console.log(
            "🚀 ~ file: Login.vue ~ line 137 ~ requestLogin ~ error",
            error.response,
          )
          loginError.value = {
            error:
              error?.response?.data?.error ||
              (error?.response?.data?.non_field_errors
                ? error?.response?.data?.non_field_errors[0]
                : "No fue posible iniciar sesión"),
          }
          sendingLogin.value = false
        } else if (data) {
          await loadAllFromServer(false)
          router.replace({ path: "/" })
        } else {
          loginError.value = {
            error: "Error de conexión al servidor, vuelva a intentarlo.",
          }
          sendingLogin.value = false
        }
      }
    }
    //
    // ON CREATE
    //
    if (isLogged.value) {
      // GO TO NEXT PAGE
      router.replace({ path: "/" })
    }

    return {
      error: loginError,
      username,
      password,
      requestLogin,
      sendingLogin,
      genericError,
      usernameError,
      passwordError,
      usernameInput,
      passwordInput,
      focusUsername,
      focusPassword,
      isUsernameFocus,
      isPasswordFocus,
      gotoResetPassword,
      hidePassword,
      usernameColorIcon,
      passwordColorIcon,
    }
  },
})
</script>
