from flask import current_app
from flask_mail import Message
from app import mail
import requests

def send_email(name):
    MAILGUN_DOMAIN = current_app.config['MAILGUN_DOMAIN']
    MAILGUN_API_KEY = current_app.config['MAILGUN_API_KEY']
    MAILGUN_RECIPIENTS = current_app.config['MAILGUN_RECIPIENTS'].replace(' ', '').split(',')

    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"

    data = {
        "from": f"Flask App <no-reply@{MAILGUN_DOMAIN}>",
        "to": MAILGUN_RECIPIENTS,
        "subject": "Novo usuário adicionado",
        "text": f"Um novo usuário foi adicionado: {name}"
    }

    response = requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data=data
    )

    if response.status_code == 200:
        print("Email enviado com sucesso!")
    else:
        print(f"Erro ao enviar email: {response.status_code}, {response.text}")
