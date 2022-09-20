from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Users
from rolepermissions.roles import assign_role

@receiver(post_save, sender = Users)
def designa_permissoes(sender , instance, created, **kwargs):
    if created:
        if instance.funcao == "CAN":
            assign_role(instance, 'candidato')
        elif instance.funcao == "EMP":
            assign_role(instance, 'empresa')
        elif instance.funcao == "ADM":
            assign_role(instance, 'admin')