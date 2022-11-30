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

//metodo validar cnpj

$.validator.addMethod('validar_cnpj', value => {
  validarCNPJ(value)
})

//metodo regex

$.validator.addMethod( "pattern", function( value, element, param ) {
  if ( this.optional( element ) ) {
      return true;
  }
  if ( typeof param === "string" ) {
      param = new RegExp( "^(?:" + param + ")$" );
  }
  return param.test( value );
}, "Invalid format." );


//regras e mensagens de erro

$(document).ready(function(){
  $("#formEmp").validate({
    rules:{
      img_perfil_empresa: {
        required: true,
      },
      nome_fantasia:{
        required:true,
        maxlength: 60
      },
      razao_social: {
        required: true,
        maxlength: 100
      },
      cnpj: {
        required: true,
      },
      telefone: {
        required:true,
      },
      celular:{
        required: true,
      },
      estado:{
        required:true,
      },
      cidade: {
        required: true
      },
      cep:{
        required:true,
      },
      ramo_de_atividade:{
        required:true
      },
      descricao_empresa:{
        required: true,
        maxlength:1000
      }
    },
    messages:{
      img_perfil_empresa: {
        required: "Insira o logo da empresa",
      },
      nome_fantasia:{
        required:"Insira o nome fantasia da empresa",
        maxlength:"Deve ter no maximo 60 caracteres"

      },
      razao_social: {
        required: "Insira a razão social da empresa",
        minlength: "A razão social deve conter até 100 caracteres"
      },
      cnpj: {
        required: "Insira O CNPJ",
        minlength: "Deve conter até 14 números",
      },
      telefone: {
        required:"Insira o telefone",
      },
      celular:{
        required: "Insira o celular",
      },
      estado:{
        required:"Insira o estado",
      },
      cidade: {
        required: "Insira a cidade"
      },
      cep:{
        required:"Insira o CEP",
      },
      ramo_de_atividade:{
        required:"Insira o ramo de atividade",
        maxlength:"Deve ter no maximo 60 caracteres"
      },
      descricao_empresa:{
        required: "Escreva um pouco da historia da empresa",
        maxlength:"Deve ter no maximo 1000 caracteres"
      }
    },
  })
})
