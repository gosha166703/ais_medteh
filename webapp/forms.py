from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, IntegerField, SelectField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional, ValidationError

from datetime import datetime

#Форма авторизации
class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")

    submit = SubmitField("Отправить")

#Форма создания и редактирования оборудования 
class EquipmentForm(FlaskForm):
    name = StringField("Название", validators= [DataRequired(message="Обязательное поле"),
                                               Length(max=1000, message="Не более 1000 символов")])
    purpose = StringField("Назначение", validators=[Optional()])
    serial_number = StringField("Серийный номер", validators=[Optional()])
    inventory_number = StringField("Инвентарный номер", validators=[Optional()])
    date_entry = DateField("Дата ввода в эксплуатацию",format='%Y-%m-%d',
                           validators=[Optional()])
    status = SelectField("Статус", choices=[('active', 'Исправно'),
                                            ('inactive', 'В резерве'),
                                            ('repair', 'На ремонте'),
                                            ('not_active', 'Не исправно')
                                        ], validators=[DataRequired()])
    write_off = BooleanField("Оборудование списано?", default=False)
    model = StringField("Модель", validators=[Optional()])
    manufacturer = StringField("Производитель", validators=[Optional()])
    #time_work = IntegerField("Наработка(часы)", validators=[Optional()], default=0)
    #downtime =  IntegerField("Время простоя(часы)", validators=[Optional()],default=0)
    last_maintenance = DateField("Дата последнего ТО", format='%Y-%m-%d',
                                 validators=[Optional()])

    submit = SubmitField("Сохранить")