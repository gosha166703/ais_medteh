from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import engine, Base


#Пользователь
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(unique=True)
    
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
    
#Конструкция if __name__ == "__main__": - говорит нам: Если из терминала был запущен файл- выполни следующую процедуру

if __name__ == "__main__":
    Base.metadata.create_all(engine)