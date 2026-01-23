from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from webapp.db import Base


#Пользователь
class User(Base, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(50),unique=True)
    lastname: Mapped[str] = mapped_column(String(120), nullable=True)
    password: Mapped[str] = mapped_column(String(1000))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    #Проверка, является ли пользователь аднминистратором
    @property
    def is_admin(self):
        return self.role_id == 1

    #Внешний ключ к таблице ролей
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    
    #Связь с таблицей ролей
    role: Mapped["Role"] = relationship(back_populates="users")

    def __repr__(self):
        return f"<User: {self.name}, {self.email}, Role: {self.role.name if self.role else 'None'}>"

#Роль Пользователя  
class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    #Связь один ко многим с таблицей пользователей
    users: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self):
        return f"<Role: {self.name}>"