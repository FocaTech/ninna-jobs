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


function s1() {
    var s1 = document.getElementById("sUm");
    var s2 = document.getElementById("sDois");

    if (s2.style.display === "none") {
    s1.style.display = "block";
    s1.style.display = "none";
    }
}