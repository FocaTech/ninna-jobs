// var cnpj = '77.180.345/0001-07'
function validarCNPJ(cnpj) {
  let numeros = cnpj.split('-')[0].replace(/[./]/g, '')
  let digitos = cnpj.split('-')[1]
  if (cnpj.length != 18 || !cnpj.includes('-'))
    return false
  if (calcularCNPJ(numeros) != digitos[0])
    return false
  if (calcularCNPJ(numeros+''+digitos[0]) != digitos[1])
    return false
  return true
}
function calcularCNPJ(numeros) {
  let peso = 2
  let resultado = 0
  for (let i = numeros.length - 1; i >= 0; i--) {
    resultado += numeros[i] * peso
    peso = (peso == 9 ? 2 : peso + 1)
  }
  let modulo = resultado % 11
  resultado = (modulo < 2 ? 0 : 11 - modulo)
  return resultado
}

$.validator.addMethod('validar_cnpj', value => {
  validarCNPJ(value)
})
