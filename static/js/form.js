 // JavaScript inicial para desativar envios de formulário, se houver campos inválidos.
(function() {
    'use strict';
    window.addEventListener('load', function() {
    // Pega todos os formulários que nós queremos aplicar estilos de validação Bootstrap personalizados.
    var forms = document.getElementsByClassName('needs-validation');
    // Faz um loop neles e evita o envio
    var validation = Array.prototype.filter.call(forms, function(form) {
    form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
            alert("Por favor preencha todos os campos corretamente para prosseguir")
        }
        form.classList.add('was-validated');
    }, false);
    });
}, false);
})();

//valida CPF
function validaCPF(strCPF) {
    function testaCPF(strCPF) {
        var Soma;
        var Resto;
        Soma = 0;
        if (strCPF == "00000000000") return false;

        for (i=1; i<=9; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (11 - i);
        Resto = (Soma * 10) % 11;

            if ((Resto == 10) || (Resto == 11))  Resto = 0;
            if (Resto != parseInt(strCPF.substring(9, 10)) ) return false;

        Soma = 0;
            for (i = 1; i <= 10; i++) Soma = Soma + parseInt(strCPF.substring(i-1, i)) * (12 - i);
            Resto = (Soma * 10) % 11;

            if ((Resto == 10) || (Resto == 11))  Resto = 0;
            if (Resto != parseInt(strCPF.substring(10, 11) ) ) return false;
            return true;
        }

    erroCPF = document.getElementById("cpfInvalido");
    let tdok = document.getElementById('naoOk')

    if (testaCPF(strCPF)=== false) {
        erroCPF.classList.remove('d-lg-none')
        tdok.classList.add('d-lg-none')
        console.log('cu')
    } else {
        erroCPF.classList.add('d-lg-none')
        tdok.classList.remove('d-lg-none')
    }
}
//Mascara CPF
function fMasc(objeto,mascara) {
    obj=objeto
    masc=mascara
    setTimeout("fMascEx()",1)
    }

    function fMascEx() {
    obj.value=masc(obj.value)
    }

    function mCPF(cpf){
    cpf=cpf.replace(/\D/g,"")
    return cpf
    }




function desabilitar() {
    const selecionado = document.querySelector("#empregoAtual");
    var saidaMes = document.getElementById('mesconclusao');
    var saidaAno = document.getElementById('anoconclusao');

    if (selecionado.checked) {
        console.log('cu')
        saidaMes.disabled = true
        saidaAno.disabled = true
    }else{
        console.log('cuzin')
        saidaMes.disabled = false
        saidaAno.disabled = false
    }
  }

