from flask import Blueprint

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from sqlalchemy import select

from webapp.db import db
from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')

#Cтраница авторизации. Аторизация, проверка есть ли такой пользователь в системе,
    #проверка авторизовывался ли уже пользователь
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