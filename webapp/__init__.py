from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from sqlalchemy import select

from webapp.config import Config
from webapp.db import db

from webapp.admin.views import blueprint as admin_blueprint

from webapp.home.views import blueprint as home_blueprint

from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

from webapp.equipment.forms import EquipmentForm
from webapp.equipment.models import Equipment
from webapp.equipment.views import blueprint as equipment_blueprint



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Инициализируем БД с приложением
    db.init_app(app)

    #Создаем экземпляр логин-менеджера
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(equipment_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        stmt = select(User).where(User.id == int(user_id))
        return db.session.execute(stmt).scalar_one_or_none()

    # Инициализируем миграции
    migrate = Migrate(app, db)
    
    # Создаем таблицы (если нужно)
    with app.app_context():
        db.create_all()
    
    return app

app = create_app()