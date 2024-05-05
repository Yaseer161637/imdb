from wtforms import PasswordField, EmailField, StringField
from wtforms.form import Form
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = EmailField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=4, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')
        ]
    )
