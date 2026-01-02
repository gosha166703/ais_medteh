from sqlalchemy import select

from db import db_session
from models import User

my_user = select(User)
my_user_res = db_session.execute(my_user)
first_user = my_user_res.scalars().first()

print(f"""
Имя:{first_user.name}
email:{first_user.email}
Роль: {first_user.role_id}

""")