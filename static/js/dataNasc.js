
    const dataNascimento = document.querySelector('#data')
    let msgDeErroD = document.getElementById('dataInvalida')
    let tdokD = document.getElementById('taOkD')



dataNascimento.addEventListener('blur',(event) =>{
    validaDataNascimento(event.target)
})
function validaDataNascimento(input){
    const dataRecebida = new Date(input.value)
    if(!maiorQue16(dataRecebida)){
        msgDeErroD.classList.remove('d-lg-none')
        tdokD.classList.add('d-lg-none')
    }else{
        msgDeErroD.classList.add('d-lg-none')
        tdokD.classList.remove('d-lg-none')
    }
}

function maiorQue16(data){
    const dataAtual = new Date()
    const dataMais16 = new Date(data.getUTCFullYear()+ 16, data.getUTCMonth(), data.getUTCDate())

    return dataMais16 <= dataAtual
}