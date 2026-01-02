from sqlalchemy import select

from db import db_session
from models_user import User

my_user = select(User).where(User.name=="Иванов Александр")
a_ivanov = db_session.execute(my_user).scalar()
a_ivanov.name = "Александров Иван"
db_session.commit()