<template>
    <q-dialog :modelValue="modelValue" @update:modelValue="$emit('update:modelValue', $event)" persistent>
        <q-card>
            <q-card-section>
                <div class="text-h6 text-grey-7">Crear nuevo usuario</div>
                <div class="row">
                    <div v-if="errorMessage" class="bg-red q-pa-sm rounded-borders text-white">{{errorMessage}}</div>
                </div>
            </q-card-section>

            <q-separator />

            <q-card-section style="max-height:80vh;width:420px" class="scroll">
                <div class="row no-wrap q-gutter-x-lg">
                    <q-input v-model="name" borderless label="Nombre" autofocus>
                        <template v-slot:append>
                            <q-icon name="o_account_circle" />
                        </template>
                    </q-input>
                    <q-input v-model="lastName" borderless label="Apellido">
                        <template v-slot:append>
                            <q-icon name="o_account_circle" />
                        </template>
                    </q-input>
                </div>
                <!-- INPUTS -->
                <q-input v-model="username" borderless label="Nombre de usuario" 
                    no-error-icon hide-bottom-space
                    :rules="[val => !hasSpaces(val) || 'No debe contener espacios', val => !usernameSimbols || 'No debe contener simbolos (#, $, /, ...)']"
                >
                    <template v-slot:append>
                        <q-icon name="o_badge" />
                    </template>
                </q-input>
                <q-input v-model="email" borderless label="Email"
                    autofocus no-error-icon hide-bottom-space
                    :rules="[val => !hasSpaces(val) || 'No debe contener espacios']"
                >
                    <template v-slot:append>
                        <q-icon name="o_email" />
                    </template>
                </q-input>
                <q-input v-model="password" borderless type="password" label="Contraseña">
                    <template v-slot:append>
                        <q-icon name="password" />
                    </template>
                </q-input>
                <q-input v-model="passwordConfirmation" borderless  type="password" label="Confirmar contraseña">
                    <template v-slot:append>
                        <q-icon name="password" />
                    </template>
                </q-input>

                <!-- SELECT MOBILE -->

                <q-btn-dropdown flat :label="selectedMobile ? selectedMobile.name || 'Móvil ' + selectedMobile.id : 'Seleccionar móvil'" 
                    class="full-width bg-grey-3 q-pa-md q-mt-sm" align="left"
                >
                    <q-list>
                        <q-item v-for="mobile of unuserMobiles" :key="mobile.id"
                            clickable v-close-popup @click="selectedMobile=mobile"
                            class="q-pt-md"
                        >
    	                    <q-item-label>
                                {{mobile.name || 'Móvil ' + mobile.id}}
                            </q-item-label>
                        </q-item>
                    </q-list>
                </q-btn-dropdown>

            </q-card-section>

            <q-separator />
            <!-- BUTTONS -->
            <q-card-actions align="right">
                <q-btn flat label="Cancelar" color="grey-8" v-close-popup />
                <q-btn flat
                    :color="isValidInfo?'primary':'grey-8'" 
                    @click="handleCreateNewUser"
                >
                    <q-spinner-pie v-if="loading" color="primary" size="1em" class="q-mr-sm" />
                    <div>{{loading?'Enviando':'Crear'}}</div>
                    <q-tooltip v-if="!isValidInfo">Todos los campos son requeridos</q-tooltip>
                </q-btn>
            </q-card-actions>
        </q-card>
    </q-dialog>
</template>

<script>
import { ref, toRefs, computed } from 'vue'
import { useMobiles, useUsers } from 'src/context'

export default {
    props: ['modelValue', 'mobile'],
    emits: ['update:modelValue'],
    setup(props) {
        const { modelValue, mobile } = toRefs(props)
        const username = ref('')
        const password = ref('')
        const email = ref('')
        const name = ref('')
        const lastName = ref('')
        const passwordConfirmation = ref('')
        const selectedMobile = ref(mobile.value || null)
        const usernameRegrex = /^[a-zA-Z0-9-_]+$/
        const loading = ref(false)
        const errorMessage = ref('')

        const { mobiles } = useMobiles()
        const { createUser } = useUsers()

        const isValidUsername = computed(_ => username.value && username.value.length >= 4 && username.value.split(" ").length === 1)
        const isValidPassword = computed(_ => password.value && password.value.length >= 4 && password.value === passwordConfirmation.value)
        const isValidEmail = computed(_ => email.value && email.value.length >= 4)
        const isValidName = computed(_ => name.value && name.value.length >= 4)
        const isValidLastName = computed(_ => lastName.value && lastName.value.length >= 4)
        const isValidInfo = computed(_ => 
            isValidUsername.value && 
            isValidPassword.value && 
            isValidName.value && 
            isValidLastName.value && 
            isValidEmail.value && 
            selectedMobile.value)

        const hasSpaces = val => val.split(" ").length > 1
        const hasSimbols = val => /^[a-zA-Z0-9-_]+$/.search(val)

        const usernameSimbols = computed(_ => username.value.length > 0 && username.value.search(usernameRegrex) === -1)
        const unuserMobiles = computed(_ => mobiles.value.filter(m => !m.user))

        const handleCreateNewUser = async () => {
            if (!isValidInfo.value || loading.value) return
            loading.value = true

            const newUser = {
                name: name.value,
                last_name: lastName.value,
                username: username.value,
                password: password.value,
                email: email.value,
                mobileId: selectedMobile.value.id,
            }
            const { data, error } = await createUser(newUser)
            if (error) {
                console.log('User creation error:', error)
                errorMessage.value = Object.values(error.response.data)[0][0]
                // TODO: Show error message
            }
            loading.value = false
        }

        return {
            modelValue,
            username,
            password,
            email,
            name,
            lastName,
            passwordConfirmation,
            isValidInfo,
            selectedMobile,
            mobiles,
            unuserMobiles,
            loading,
            errorMessage,

            handleCreateNewUser,

            hasSpaces,
            hasSimbols,

            usernameSimbols,
        }
    },
}
</script>