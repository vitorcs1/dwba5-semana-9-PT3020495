from flask import render_template, redirect, url_for, flash
from app.main.forms import NameForm
from app.models import User, Role, db
from app.email import send_email
from app.main import bp as main

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    name = None

    if form.validate_on_submit():
        name = form.name.data
        existing_user = User.query.filter_by(username=name).first()
        if existing_user is None:
            new_user = User(username=name)
            user_role = Role.query.filter_by(name='user').first()
            new_user.role = user_role

            db.session.add(new_user)
            db.session.commit()
            send_email(name)
            flash('E-mail enviado para os destinatários!', 'success')
            return redirect(url_for('main.index', name=name))
        else:
            flash('O usuário já existe! E-mail não enviado.', 'warning')
            return redirect(url_for('main.index', name=name))

    users = User.query.all()

    return render_template('index.html', form=form, users=users, name=name)
