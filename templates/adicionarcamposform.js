//##Jquery##
//Adicionar experiencia Profissional 
$( "#adicionar").click(function(){
    $( ".experienciaProfissional" ).append('\
        <div id="xpProfissional" class="row py-2">\
            <div class="text-center excluir">\
                <button type="button" id="excluirXP" class="btn btn-primary float-end" onclick="$(this).parent().parent().remove()">\
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">\
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />\
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />\
                    </svg>\
                    Excluir\
                </button>\
            </div>\
            <div class="col-md-6 py-2">\
                <label for="empresa" class="form-label">Empresa</label><input type="text" class="form-control" id="empresa" required />\
                <div class="valid-feedback">Tudo ok!</div>\
            </div>\
            <div class="col-md-6 py-2">\
                <label for="cargo" class="form-label">Cargo</label><input type="text" class="form-control" id="cargo" required />\
                <div class="valid-feedback">Tudo ok!</div>\
            </div>\
            <div>\
                <div class="form-floating py-2"><textarea class="form-control" placeholder="Fale um pouco sobre" id="floatingTextarea" style="height: 100px;"></textarea><label for="floatingTextarea">Fale um pouco sobre.</label></div>\
            </div>\
            <div\z class="row py-2">\
                <div class="col-md-3">\
                    <label for="entrada" class="form-label">Data de inicio</label>\
                    <select class="form-select" id="entrada" required>\
                        <option selected disabled value="">Mês</option>\
                        <option value="janeiro">Janeiro</option>\
                        <option value="fevereiro">Fevereiro</option>\
                        <option value="marco">Março</option>\
                    </select>\
                </div>\
                <div class="col-md-3 py-2">\
                    <label for="entrada" class="form-label"></label>\
                    <select class="form-select" id="entrada" required>\
                        <option selected disabled value="">Ano</option>\
                        <option value="2022">2022</option>\
                        <option value="2021">2021</option>\
                        <option value="2020">2020</option>\
                    </select>\
                </div>\
                <div class="col-md-3">\
                    <label for="messaida" class="form-label">Saida</label>\
                    <select class="form-select" id="mesconclusao" required>\
                        <option selected disabled value="">Mês</option>\
                        <option value="janeiro">Janeiro</option>\
                        <option value="fevereiro">Fevereiro</option>\
                        <option value="marco">Março</option>\
                    </select>\
                </div>\
                <div class="col-md-3 py-2">\
                    <label for="saida" class="form-label"></label>\
                    <select class="form-select" id="saida" required>\
                        <option selected disabled value="">Ano</option>\
                        <option value="2022">2022</option>\
                        <option value="2021">2021</option>\
                        <option value="2020">2020</option>\
                    </select>\
                </div>\
                <div class="form-check"><input class="form-check-input" type="checkbox" value="" /><label class="form-check-label" for="invalidCheck">É meu emprego atual</label></div>\
            </div>\
        </div>\
    ')
})

//Adicionar certificados e conquistas

$( "#adicionarcertificados").click(function(){
    $( ".certificados" ).append('\
        <div class="row">\
            <div>\
                <button type="button" class="btn btn-primary float-end" onclick="$(this).parent().parent().remove()">\
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">\
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>\
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>\
                    </svg> Excluir\
                </button>\
            </div>\
            <div class="col-md-6 py-2">\
                <label for="certificadotitulo" class="form-label">Titulo</label>\
                <input type="text" class="form-control" id="certificadotitulo" required>\
                <div class="invalid-feedback">\
                    Por favor, informe o titulo.\
                </div>\
            </div>\
            <div class="col-md-6 py-2">\
                <label for="certificadotipo" class="form-label">Tipo</label>\
                <select class="form-select" id="certificadotipo" required>\
                    <option selected disabled value="">Escolha</option>\
                    <option value="curso">Curso</option>\
                    <option value="reconhecimento">Reconhecimento</option>\
                    <option value="TV">Trabalho Voluntário</option>\
                </select>\
            </div>\
            <div class="form-floating py-2">\
                <textarea class="form-control" placeholder="Fale um pouco sobre" id="floatingTextarea" style="height: 100px"></textarea>\
                <label for="floatingTextarea">Fale um pouco sobre.</label>\
            </div>\
        </div>\
    ');
});

//Adicionar Idioma
$( "#adicionarIdioma").click(function(){
    $( ".idioma" ).append('\
        <div id="idioma">\
            <div class="text-center">\
                <button type="button" class="btn btn-primary float-end" onclick="$(this).parent().parent().remove()">\
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">\
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>\
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>\
                    </svg> Excluir\
                </button>\
            </div>\
            <div class="row">\
                <div class="col-md-8 py-2">\
                <label for="idioma" class="form-label">Idioma</label>\
                <input type="text" class="form-control" id="idioma" value="idioma" required>\
                <div class="valid-feedback">\
                    Tudo ok!\
                </div>\
            </div>\
            <div class="col-md-4 py-2">\
                <label for="nivelDeConhecimento" class="form-label">Nivel</label>\
                <select class="form-select" id="nivelConhecimento" required>\
                    <option selected disabled value="">Escolha...</option>\
                    <option value="basico">Básico</option>\
                    <option value="intermediario">Intermediário</option>\
                    <option value="avancado">avançado</option>\
                    <option value="nativoFluente">Nativo/Fluente</option>\
                </select>\
                <div class="invalid-feedback">\
                     Por favor, escolha uma opção valida\
                </div>\
            </div>  \
        </div>\
    ')
})         

