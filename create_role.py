import sys # модуль взаимодействия с системными функциями 

from webapp import create_app, db
from webapp.user.models import Role

app = create_app()

with app.app_context():#Позволяет работать с нашей БД
    name = input("Введите название роли: ")

    #Проверяем есть ли в БД роль с заданным именем
    enginner_role = db.session.query(Role).filter_by(name=name).first()
    #Если такой роли нет, то создаем ее
    if not enginner_role:
        enginner_role = Role(name = "Инженер")
        db.session.add(enginner_role)
        db.session.commit()
        print(f"Создана роль {enginner_role.name}")
    else:
        print(f"Роль '{enginner_role.name}' уже существует")
