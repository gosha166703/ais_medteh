from turtle import title
from flask import Blueprint

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from sqlalchemy import select

from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')

#Страница регистрации
@blueprint.route("/register")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    title = "Регистрация"
    form = RegistrationForm()
    return render_template("user/registration.html", page_title=title, form=form)

#Процесс регистрации
@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(name=form.username.data,
                         email=form.email.data,
                         lastname=form.lastname.data,
                         role_id=2)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    flash('Пожалуйста, исправьте ошибки в форме')
    return render_template('user/registration.html',page_title="Регистрация", form=form )

#Cтраница авторизации. 
@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title = title, form = login_form)

#Процесс авторизации
@blueprint.route("/process-login", methods=["POST"])
def process_login():
    form = LoginForm()
    
    
    if form.validate_on_submit():
        stmt = select(User).where(User.name == form.username.data)
        user = db.session.execute(stmt).scalar_one_or_none()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Авторизация прошла успешно")
            return redirect(url_for("home.index"))
        
        flash("Неправильное имя пользователя или пароль")
        return redirect(url_for("user.login"))

#Выход из системы(Разлогиниться)
@blueprint.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.index"))