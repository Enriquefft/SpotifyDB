from flask import current_app

from flask_wtf import FlaskForm


from app.server.models import User
    
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import PasswordField, StringField


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired()], description="Nombre de usuario")
    password = PasswordField('Password', validators=[DataRequired()], description="Contraseña")


    def validate_username(self, field):
        with current_app.app_context():
            self._user = User.query.filter_by(username=field.data).first()

        if self._user:
            raise ValidationError("Nombre de usuario ya existe")

    def validate_password(self, field):
        from werkzeug.security import generate_password_hash
        self.passhash = generate_password_hash(field.data)
        with current_app.app_context():
            passw = User.query.filter_by(pass_hash=self.passhash).first()
        if passw:
            raise ValidationError("Contraseña ya existe")

def register():

    form = RegisterForm()

    if form.validate_on_submit(): # POST

        from flask_login import login_user
        from flask import url_for, redirect

        user = User(username=form.username.data, pass_hash=form.passhash)
        id, error = user.insert()
        user = User.query.get(id)

        login_user(user)

        return redirect(url_for('users.authorize'))

    # GET
    from flask import render_template
    return render_template("register.html", form=form)
