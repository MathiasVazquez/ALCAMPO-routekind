

const formatToDatePicker = (date, separator="/") => {
  if (!date) return ''
  if (typeof date === 'string') return date

  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const monthDay = date.getDate()
  const result = `${year}${separator}${(month + '').padStart(2, '0')}${separator}${(monthDay + '').padStart(2, '0')}`
  return result
}

const formatFromDatePicker = (date, separator="/") => {
  // "2022-01-13"
  if (!date) return null
  if (typeof date !== 'string') return date

  const [year, month, monthDay] = date.split(separator)
  return new Date(year, +month - 1, monthDay)
}

const formatDate = (d, includeHour = false, separator = '/') => {
  if (!d) return null
  if (typeof d === 'string') d = formatFromDatePicker(d)

  const year = d.getFullYear()
  const month = ((d.getMonth() + 1) + '').padStart(2, '0')
  const monthDay = (d.getDate() + '').padStart(2, '0')
  const hour = (d.getHours() + '').padStart(2, '0')
  const minute = (d.getMinutes() + '').padStart(2, '0')
  return `${monthDay}${separator}${month}${separator}${year}` + (includeHour ? ` ${hour}:${minute}` : '')
}

const isToday = date => {
  const today = new Date()
  return date.getDate() == today.getDate() &&
    date.getMonth() == today.getMonth() &&
    date.getFullYear() == today.getFullYear()
}

const isTomorrow = date => {
  const today = new Date()
  const isTomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1)
  return date.getDate() == isTomorrow.getDate() &&
    date.getMonth() == isTomorrow.getMonth() &&
    date.getFullYear() == isTomorrow.getFullYear()
}

const isOvermorrow = date => {
  const today = new Date()
  const isTomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 2)
  return date.getDate() == isTomorrow.getDate() &&
    date.getMonth() == isTomorrow.getMonth() &&
    date.getFullYear() == isTomorrow.getFullYear()
}

const isYesterday = date => {
  const today = new Date()
  const isTomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() - 1)
  return date.getDate() == isTomorrow.getDate() &&
    date.getMonth() == isTomorrow.getMonth() &&
    date.getFullYear() == isTomorrow.getFullYear()
}

const sameDate = (_d1, _d2) => {
  const d1 = new Date(_d1)
  const d2 = new Date(_d2)
  return d1.getDate() == d2.getDate() &&
    d1.getMonth() == d2.getMonth() &&
    d1.getFullYear() == d2.getFullYear()
}

export {
  formatFromDatePicker,
  formatToDatePicker,
  formatDate,
  isOvermorrow,
  isYesterday,
  isTomorrow,
  sameDate,
  isToday,
}