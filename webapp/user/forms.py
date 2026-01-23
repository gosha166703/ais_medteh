from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from webapp.user.models import User
from webapp.db import db


#Форма авторизации
class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")

    submit = SubmitField("Отправить")

#Форма регистрации
class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    lastname = StringField("Фамилия пользователя", validators=[DataRequired()])
    email = StringField("Электронная почта", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo("password")])

    submit = SubmitField("Отправить")

# Валидация email
    def validate_email(self, email):
        user = db.session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError("Этот email уже зарегистрирован")