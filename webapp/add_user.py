from db import db_session 
from models import User, Role

engineer_role = Role(name = "Инженер")
db_session.add(engineer_role) # Формируем запрос
db_session.commit() #commit - накатывает изменения на нашу базу 

first_user = User(name = "Иванов Александр", email= "gosha166703@gmail.com", role= engineer_role)
db_session.add(first_user) # Формируем запрос
db_session.commit() #commit - накатывает изменения на нашу базу 