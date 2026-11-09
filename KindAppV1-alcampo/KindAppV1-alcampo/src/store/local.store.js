export const store = {
  get(key, defaultValue = null, jsonParse = true) {
    const value = localStorage.getItem(key)
    if (value === null) return defaultValue
    if (!jsonParse) return value;
    try { return JSON.parse(value) }
    catch (_) { return value }
  },
  set(key, value, jsonParse = true) {
    if (value === undefined || value === null) localStorage.removeItem(key)
    else localStorage.setItem(key, jsonParse ? JSON.stringify(value) : value)
  },
  clear() {
    localStorage.clear()
  },
}
export const session = {
  get(key, defaultValue = null, jsonParse = true) {
    const value = sessionStorage.getItem(key)
    if (value === null) return defaultValue
    if (!jsonParse) return value
    try { return JSON.parse(value) }
    catch (_) { return value }
  },
  set(key, value, jsonParse = true) {
    if (value === undefined || value === null) sessionStorage.removeItem(key)
    else sessionStorage.setItem(key, jsonParse ? JSON.stringify(value) : value)
  },
}

export default { store, session }
