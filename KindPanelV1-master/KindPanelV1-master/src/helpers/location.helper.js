import { computed, ref } from 'vue'
import { BASE_URL, useSession, authHeader } from 'src/context'
import axios from 'axios'

const OPTIONS = {
  enableHighAccuracy: true,
  maximumAge: 5000,
  timeout: 10000,
  frequency: 500
}

const currentPosition = ref(null)
const watcherId = ref(null)
const watcherError = ref(null)

export const useLocation = () => {
  const { isLogged, mobile } = useSession()

  const askForPermissions = async() => {
    try {
      return await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          position => { resolve({ data: position }) },
          error => { reject({ error }) },
          OPTIONS
        )
      })
    }
    catch(error) { return { error } }
  }

  const startWatchLocation = () => {
    if (watcherId.value) return watcherId.value

    const onUpdatePosition = location => {
      const { coords } = location
      watcherError.value = null
      currentPosition.value = {
        lat: coords.latitude,
        lng: coords.longitude,
        date: new Date().toISOString()
      }
      console.log('location:', location)
      // if (isLogged.value && mobile.value) updateLocationInServer({ ...coords, lat: coords.latitude, lng: coords.longitude, id: mobile.value.id })
    }
    const onUpdateError = async error => {
      // Ask for permission
      const result = await askForPermissions()
      // Show error if not perimssion
      if (result.error) watcherError.value = error
    }
    const id = navigator.geolocation.watchPosition(
      onUpdatePosition,
      onUpdateError,
      OPTIONS
    )
    watcherId.value = id
    return id
  }
  const stopWatch = () => {
    if (watcherId.value) {
      navigator.geolocation.clearWatch(watcherId.value);
      watcherId.value = null
    }
  }

  return {
    askForPermissions,
    startWatchLocation,
    stopWatch,
    currentPosition: computed(() => currentPosition.value),
    positionError: computed(() => watcherError.value)
  }
}
