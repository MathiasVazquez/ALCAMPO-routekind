export const formatMoney = money => {
  money = `${money}`;
  if (money.length <= 3) return money
  let result = []
  let count = 0
  for (let i = 0; i < money.length; i++) {
    let m = money[money.length - i - 1]
    if (count === 3) {
      result.unshift('.')
      count = 0
    }
    count++
    result = [m].concat(result)
  }
  return result.join('')
}
