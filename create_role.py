import sys # модуль взаимодействия с системными функциями 

from webapp import create_app, db
from webapp.models_user import Role

app = create_app()

with app.app_context():#Позволяет работать с нашей БД
    name = input("Введите имя: ")

    #Проверяем есть ли в БД роль с заданным именем
    admin_role = db.session.query(Role).filter_by(name=name).first()
    #Если такой роли нет, то создаем ее
    if not admin_role:
        admin_role = Role(name = "Админ")
        db.session.add(admin_role)
        db.session.commit()
        print(f"Создана роль {admin_role.name}")
    else:
        print(f"Роль '{admin_role.name}' уже существует")
