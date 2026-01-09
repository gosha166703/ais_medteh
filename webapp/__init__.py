from datetime import timedelta
from flask import Flask, render_template, flash, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from sqlalchemy import select

from webapp.config import Config
from webapp.db import db
from webapp.forms import LoginForm, EquipmentForm
from webapp.models_user import User
from webapp.models_equipment import Equipment



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
    
    #Главная страница (Аналитика)
    @app.route('/')
    def index():
        return render_template('index.html', page_title="Главная")
    
    #Эндпоинт Реестр основных средств
    @app.route("/equipment")
    def equipment():
        #Получить все оборудование из БД 
        stmt = select(Equipment).order_by(Equipment.created_at.desc())
        equipment_list = db.session.execute(stmt).scalars().all()
        return render_template("equipment.html", page_title="Реестр основных средств",
                               equipment_list=equipment_list)
    
    #Эндпоинт Создание оборудования
    @app.route("/equipment/create", methods=["GET","POST"])
    @login_required
    def create_equipment():
        form = EquipmentForm()
        if form.validate_on_submit():
            new_equipment = Equipment(name=form.name.data,
                                      purpose=form.purpose.data,
                                      serial_number=form.serial_number.data,
                                      inventory_number=form.inventory_number.data,
                                      date_entry=form.date_entry.data,
                                      status=form.status.data,
                                      write_off=form.write_off.data,
                                      model=form.model.data,
                                      manufacturer=form.manufacturer.data,
                                      #time_work=timedelta(hours=form.time_work.data or 0),
                                      #downtime=timedelta(hours=form.downtime.data or 0),
                                      last_maintenance=form.last_maintenance.data,
                                      )
            try:
                db.session.add(new_equipment)
                db.session.commit()
                flash("Оборудование добавлено в реестр", 'success')
                return redirect(url_for("equipment"))
            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка при добавлении: {str(e)}", "error") 

        return render_template("equipment_form.html", form=form, page_title="Добавить оборудование")
    
    #Эндпоинт Просмотр оборудования
    @app.route("/equipment/<int:id>", methods=["GET"])
    @login_required
    def equipment_detail(id):
        equipment = db.session.get(Equipment, id)
        if not equipment:
            flash("Оборудование не найдено", "error")
            return redirect(url_for("equipment"))
        return render_template("equipment_detail.html", equipment=equipment, page_title=equipment.name)
    
    #Эндпоинт Редактирование оборудования
    @app.route("/equipment/<int:id>/edit", methods=["GET", "POST"])
    @login_required
    def equipment_edit(id):
        #Обработка GET запроса
        equipment = db.session.get(Equipment, id)
        if not equipment:
            flash("Оборудование не найдено", "error")
            return redirect(url_for("equipment"))
        form = EquipmentForm(obj=equipment)
        
        #Обработка POST запроса
        if form.validate_on_submit():
            form.populate_obj(equipment)
            try:
                db.session.commit()
                flash("Изменения сохранены", "success")
                return redirect(url_for("equipment_detail", id=id))
            except Exception as e:
                db.session.rollback()
                flash(f"Ошибка при изменении: {str(e)}", "error")
        return render_template("equipment_form.html", form=form, 
                          page_title="Редактировать оборудование", equipment=equipment)

    
    #Эндпоинт Удаление оборудования
    @app.route("/equipment/<int:id>/delete", methods=["POST"])
    @login_required
    def delete_equipment(id):
        equipment = db.session.get(Equipment, id)
        try:
            db.session.delete(equipment)
            db.session.commit()
            flash ("Оборудование удалено", 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при удалении: {str(e)}', 'error')
            
        return redirect(url_for('equipment'))

        
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
                login_user(user, remember=form.remember_me.data)
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