from flask import Flask, render_template, flash, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from sqlalchemy import select

from webapp.config import Config
from webapp.db import db
from webapp.forms import LoginForm
from webapp.models_user import User, Role
from webapp.models_fixed_assed import FixedAssed



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализируем БД с приложением
    db.init_app(app)

    #Создаем экземпляр логин-менеджера
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        stmt = select(User).where(User.id == int(user_id))
        return db.session.execute(stmt).scalar_one_or_none()

    # Инициализируем миграции
    migrate = Migrate(app, db)
    
    #Главная страница 
    @app.route('/')
    def index():
        return render_template('index.html', page_title="Главная")
    
    #Cтраница авторизации. Аторизация, проверка есть ли такой пользователь в системе,
    #проверка авторизовывался ли уже пользователь
    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title = title, form = login_form)
    
    #Процесс авторизации
    @app.route("/process-login", methods=["POST"])
    def process_login():
        form = LoginForm()
        
        
        if form.validate_on_submit():
            stmt = select(User).where(User.name == form.username.data)
            user = db.session.execute(stmt).scalar_one_or_none()

            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Авторизация прошла успешно")
                return redirect(url_for("index"))
            
            flash("Неправильное имя пользователя или пароль")
            return redirect(url_for("login"))
    
    #Выход из системы(Разлогиниться)
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/admin")
    @login_required #Проверка авторизован ли пользователь
    def admin_index():
        if current_user.is_admin:
            return "Привет админ"
        else:
            return "Ты не админ"

    # Создаем таблицы (если нужно)
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()