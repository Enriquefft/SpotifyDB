from flask import render_template, current_app, redirect, url_for
from flask_login import login_user

from flask_wtf import FlaskForm


from app.server.models import User

from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import PasswordField, StringField, BooleanField
from werkzeug.security import check_password_hash


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[
                           DataRequired()], description="Nombre de usuario")
    password = PasswordField('Password', validators=[
                             DataRequired()], description="Contraseña")
    remember_me = BooleanField(
        "Remember Me", description="¿desea guardar su sesión?")

    def valid_username(self, field):
        with current_app.app_context():
            self._user = User.query.filter_by(username=field.data).first()

        if not self._user:
            raise ValidationError("Nombre de usuario no encontrado")

    def valid_password(self, field):
        #user = User.query.filter_by(username=field.data).first()
        if not check_password_hash(self._user.password, field.data):
            raise ValidationError("Contraseña incorrecta")


def login():

    form = LoginForm()

    from flask_login import current_user
    if current_user.is_authenticated:
        if current_user.has_authorized:
            return redirect(url_for('home.index'))
        else:
            return redirect(url_for('users.authorize'))

    if form.validate_on_submit():  # POST

        user = form._user
        remember_me = form.remember_me.data
        login_user(user, remember=remember_me)

        if not user.has_authorized():
            return redirect(url_for('auth'))
        else:
            return redirect(url_for('home.index'))

    # GET

    return render_template("login.html", form=form)
