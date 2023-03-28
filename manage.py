#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ninna_jobs.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


# AJUDA DO FRONT
# python manage.py runserver
# python manage.py createcachetable
# python manage.py loaddata TipoTrabalho
# python manage.py loaddata PerfilProfissional
# python manage.py loaddata TipoContratacao
# pip install -r requirements.txt
# .\venv\Scripts\activate


#<-MEMBROS DA FOCATEC->
#FRONTEND:
#°Alice Costa - https://github.com/AliceKowai
#°Gustavo Ícaro - https://github.com/gustavoicaro
#°Maria Geisa - https://github.com/mariageisa

#BACKEND:
#°Erick Patrick - https://github.com/ErickPTCosta
#°Hermeson Rocha - https://github.com/Hemerson-Rocha
#°Kauhê Victo - https://github.com/Kauhe-Victor
#°Danilo da Silva - https://github.com/Danilozzz

#<-Projeto - NINNA JOBS->
#repositorio - https://github.com/gustavoicaro/ninna-jobs























































































































































#FÉ DA EQUIPE
#°Diego Wesley - https://github.com/DiegoWesley25