import axios from 'axios'
import { ref, computed } from 'vue'
import { store } from 'src/store/local.store'
import { BASE_URL, clearAllMemory } from '.'

const user = ref(store.get('user', null))

export const authHeader = computed(() => {
  const { token } = user?.value || {}
  const baseHeaders = {
    "kind-version": "1.0.2"
  }
  return {
    headers: token ?
      { 'Authorization': `token ${token}`, ...baseHeaders } :
      { ...baseHeaders }
  }
})

export const useSession = () => {

  const setUser = value => {
    user.value = value
    store.set('user', value)
  }

  const login = async ({username, password}) => {
    try {
      const { data } = await axios.post(BASE_URL + "login/", { username, password }, authHeader.value)
      setUser(data[0] || data)
      return { data: data[0] || data }
    }
    catch (error) { return { error } }
  }

  const logout = () => {
    setUser(null)
    clearAllMemory()
    store.clear()
  }

  const increaseInvoiceConfigActualNumber = () => {
    setUser({
      ...user.value,
      invoiceConfig: {
        ...user.value.invoiceConfig,
        actualNumber: user.value.invoiceConfig.actualNumber + 1
      }
    })
  }

  const loadProfile = async () => {
    try {
      const { data } = await axios.get(BASE_URL + "user/profile/", authHeader.value)
      const profile = data[0] || data
      const profileResult = { ...user.value, ...profile }
      setUser(profileResult)
      return { data: profileResult }
    }
    catch (error) { return { error } }
  }

  return {
    user: computed(() => user.value),
    mobile: computed(() => user.value?.mobile),
    warehouse: computed(() => user.value?.warehouse),
    company: computed(() => user.value?.company),
    invoiceConfig: computed(() => user.value?.invoiceConfig),
    isLogged: computed(() => !!user.value),
    token: computed(() => user.value.token),
    increaseInvoiceConfigActualNumber,
    loadProfile,
    logout,
    login,
  }
}
