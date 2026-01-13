from getpass import getpass #очень похожа на input, но не печатает то что пользователь вводит
import sys # модуль взаимодействия с системными функциями 

from webapp import create_app, db
from webapp.user.models import User, Role
from sqlalchemy import select

app = create_app()

with app.app_context():#Позволяет работать с нашей БД
    username = input("Введите имя: ")
    lastname = input("Введите фамилию: ")
    email = input("Введите ваш email: ")

    stmt = select(User).where(User.name == username)
    if db.session.execute(stmt).scalar_one_or_none():
        print("Пользователь с таким именем уже существует")
        sys.exit(0)

    stmt = select(User).where(User.email == email)
    if db.session.execute(stmt).scalar_one_or_none():
        print("Пользователь с таким email уже существует")
        sys.exit(0)

    #Находим нужную роль в БД 
    stmt = select(Role).where(Role.name == "Инженер")
    admin_role = db.session.execute(stmt).scalar_one_or_none()

    if not admin_role:
        print(" Роль не найдена!")
        sys.exit(1)

    password1 = getpass("Введите пароль")
    password2 = getpass("Повторите пароль")

    if not password1 == password2:
        print("Пароли не совпадают")
        sys.exit(0)

    #Создаем пользователя
    new_user = User(
        name=username,
        lastname=lastname,
        email=email,           
        role_id=admin_role.id  
    )
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f"Создан пользователь с id={new_user.id}")