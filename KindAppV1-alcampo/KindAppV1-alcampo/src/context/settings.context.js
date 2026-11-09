import { ref, computed, reactive, toRefs } from 'vue'
import { store } from 'src/store/local.store'

const defaultSettings = {
  fullMapVisualization: false, 
}

const settings = reactive(store.get('settings', defaultSettings))

export const useSettings = () => {

  const computeProp = (propName, {useViewScope} = {}) => {
    return {
      [propName]: computed({
        get: () => {
          const result = settings[propName] || defaultSettings[propName]
          return useViewScope ? result[settings.viewScope] : result
        },
        set: value => {
          if (useViewScope) (settings[propName] = settings[propName] || {})[settings.viewScope] = value
          else settings[propName] = value
          store.set('settings', { ...settings })
        }
      })
    }
  }

  return {
    ...computeProp("fullMapVisualization"),
  }
    
}