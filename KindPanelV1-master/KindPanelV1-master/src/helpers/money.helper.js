export const formatMoney = (number, suffix) => {
  if (!number) return `0 ${suffix || ''}`
  const [money, decimal] = `${parseFloat(number)}`.split(".")
  let result = ""
  if (money.length <= 3) result = money
  else {
    let results = []
    let count = 0
    for (let i = 0; i < money.length; i++) {
      let m = money[money.length - i - 1]
      if (count === 3) {
        results.unshift('.')
        count = 0
      }
      count++
      results = [m].concat(results)
    }
    result = results.join('')
  }
  return result + (decimal ? `,${decimal}` : '') + ` ${suffix || ''}`
}
