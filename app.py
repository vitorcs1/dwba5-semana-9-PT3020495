import os
import requests
from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'hard_key'

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
MAILGUN_RECIPIENTS = os.getenv('MAILGUN_RECIPIENTS').replace(' ', '').split(',')

class NameForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():

    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        send_email(name)
        flash('E-mail enviado para os destinatários.', 'success')
        return redirect(url_for('index'))

    return render_template('index.html', form=form)

def send_email(name):
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

    if response.status_code != 200:
        error_message = f"Falha ao enviar o e-mail. Status code: {response.status_code}, Resposta: {response.text}"
        print(error_message)
        raise Exception(error_message)

if __name__ == '__main__':
    app.run(debug=True)
