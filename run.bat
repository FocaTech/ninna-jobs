@echo off
if not exist .venv (
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    pause
) else (
    .venv\Scripts\activate
    python manage.py runserver
)
