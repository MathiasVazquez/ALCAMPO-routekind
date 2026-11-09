import { ref } from "vue"

export const ESC_ALIGN_LEFT = "0" // equivalent 0x1B, 0x61, 0x00
export const ESC_ALIGN_CENTER = "1" // equivalent 0x1B, 0x61, 0x01
export const ESC_ALIGN_RIGHT = "2" // equivalent 0x1B, 0x61, 0x02
// export const PRINTERS_NAME = ['GL-33', 'RG-MDP58B'] //'RG-MDP58B'
// export const PRINTERS_NAME = ['HM-E300-FB7C']
export const PRINTERS_NAME = [
  "MDP58C",
  "MDP58C_00F4",
  "MDP58C_0164",
  "MDP58C_010B",
  "MDP58C_0100",
  "MDP58C_179F",
  "MDP58C_00CA",
  "GL-33",
  "MDP58C_1DC4",
  "MDP58C_19E1",
  "HM-A300-CECF",
  "HM-A300-69D3",
]
const connectedPrinter = ref("")

export const getSpaces = (spaces) =>
  new Array(Math.max(spaces, 1)).fill(" ").join("")

export const getBetween = (left, right, spaces = 30) => {
  const middleSpace = spaces - (left + "").length - (right + "").length
  return left + getSpaces(middleSpace) + right
}

export const getSeparator = (pattern = " -", spaces = 30) => {
  let result = ""
  for (let i = 0; i < spaces; i += pattern.length) result += pattern
  return result
}

export const getSpaceBetween = (left, right, spaces = 30) => {
  const middleSpace = spaces - (left + "").length - (right + "").length
  return left + getSpaces(middleSpace) + right
}

export const formatWords = (value, columns = 30) => {
  const words = `${value}`
    // .replaceAll("á", "a")
    // .replaceAll("é", "e")
    // .replaceAll("í", "i")
    // .replaceAll("ó", "o")
    // .replaceAll("ú", "u")
    .split(" ")
  // ['Direccion:', 'Basilero', 'Milecis', '1063', 'La', 'Empresa']
  const lines = []
  let result = "" // ''
  let lineText = ""

  const currentRow = () => Math.ceil((result.length || 1) / columns)
  const currentColumn = () => result.length - (currentRow() - 1) * columns
  // let currentColumn = result.length - (currentRow() * columns)

  let rightSpace = () => columns - currentColumn()

  for (let word of words) {
    const _currentColumn = currentColumn()
    if (_currentColumn > 0 && _currentColumn < columns) {
      result += " "
      lineText += " "
    }

    const _rightSpace = rightSpace()
    if (word.length > _rightSpace) {
      lines.push(lineText.slice(0, -1) + "\n")
      lineText = ""
      for (let i = 0; i < _rightSpace; i++) result += " "
    }

    result += word
    lineText += word
  }

  return lines.concat(lineText + "\n")
}

export const listPrinters = async () => {
  const BTPrinter = window.BTPrinter
  if (!BTPrinter) return

  return new Promise((resolve, reject) => {
    BTPrinter.list(
      (data) => resolve(data),
      (error) => reject(error),
    )
  })
}

export const printLine = async (text, align = "0", size = "0") => {
  const BTPrinter = window.BTPrinter
  if (!BTPrinter) return

  const formattedLine = (textLine) => {
    return new Promise((resolve, reject) => {
      BTPrinter.printTextSizeAlign(
        (data) => resolve(data),
        (error) => reject(error),
        textLine,
        size,
        align,
      )
    })
  }

  return Promise.all(formatWords(text).map((w) => formattedLine(w)))
}

export const printSingleRow = async (text, align = "0", size = "0") => {
  const BTPrinter = window.BTPrinter
  if (!BTPrinter) return

  return new Promise((resolve, reject) => {
    BTPrinter.printTextSizeAlign(
      (data) => resolve(data),
      (error) => reject(error),
      text.split("\n").join(""),
      size,
      align,
    )
  })
}

export const printSeparator = async (pattern = " -", spaces = 30) => {
  return await printLine(getSeparator(pattern, spaces))
}

export const printBetween = async (left, right, spaces = 30) => {
  return await printLine(printBetween(left, right, spaces))
}

function setEncoding() {
  BTPrinter.setEncoding(
    function (data) {},
    function (err) {
      throw "No fue posible establecer la codificación, es posible que ciertos carácteres no sean correctamente impresos."
    },
    "IBM850",
  )
}

const getStoredAdditionalPrinters = () => {
  return JSON.parse(localStorage.getItem("additionalPrintes") ?? "[]")
}

/**
 * @param {string} additionalPrinter
 */
const storeAdditionalPrinter = (additionalPrinter) => {
  localStorage.setItem(
    "additionalPrintes",
    JSON.stringify(getStoredAdditionalPrinters().concat(additionalPrinter)),
  )
}

/**
 * @param {string} additionalNames
 */
export const connectPrinter = async (additionalPrinterName) => {
  setEncoding()
  const BTPrinter = window.BTPrinter
  if (!BTPrinter)
    throw "No se pudo imprimir: Asegurese de tener el bluetooth encendido y los permisos necesarios"

  const printers = await listPrinters()
  const allPrinters = PRINTERS_NAME.concat(
    getStoredAdditionalPrinters() ?? [],
  ).concat(additionalPrinterName ?? [])

  return new Promise((resolve, reject) => {
    for (let printerName of allPrinters) {
      if (printers.indexOf(printerName) === -1) continue
      try {
        BTPrinter.connect(
          (data) => {
            connectedPrinter.value = printerName
            if (additionalPrinterName)
              storeAdditionalPrinter(additionalPrinterName)
            resolve({ ...data, printerName: printerName })
          },
          (error) => reject(error),
          printerName,
        )
        return
      } catch (error) {
        const printerName = prompt("Ingrese el nombre de la impresora.")
        if (printerName) connectPrinter(printerName).then(resolve).catch(reject)
      }
    }
    reject("No fue posible detectar ninguna impresora.")
  })
}

export const disconnectPrinter = async (
  { printerName } = { printerName: PRINTERS_NAME },
) => {
  const BTPrinter = window.BTPrinter
  if (!BTPrinter)
    throw "Asegurese de tener el bluetooth encendido y los permisos necesarios"

  return new Promise((resolve, reject) => {
    BTPrinter.disconnect(
      (data) => {
        resolve(data)
        connectedPrinter.value = ""
      },
      (error) => reject(error),
      connectedPrinter.value,
    )
  })
}
