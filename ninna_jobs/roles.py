from rolepermissions.roles import AbstractUserRole

class Empresa(AbstractUserRole):
    available_permissions = {
        'cadastrar_vagas': True,
        'alterar_status_vagas': True,
        'acessar_dash_can' :False
    }

class Candidato(AbstractUserRole):
    available_permissions ={
        'se_candadatar': True,
        'favoritar_vaga': True,
        'acessar_dash_can' : True

    }