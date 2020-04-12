from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    FileField
)


class LoginForm(FlaskForm):
    astronaut_id = StringField("ID астронавта", validators=[DataRequired()])
    astronaut_pass = PasswordField("Пароль астронавта", validators=[DataRequired()])
    
    capitan_id = StringField("ID капитана", validators=[DataRequired()])
    capitan_pass = PasswordField("Пароль капитана", validators=[DataRequired()])

    submit = SubmitField('Войти')


class ImageForm(FlaskForm):
    image = FileField('Новое фото', validators=[DataRequired()])

    submit = SubmitField('Добавить')