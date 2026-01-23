from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy

class Base(DeclarativeBase):
    
    def to_dict(self):
        """Сериализация в словарь"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

db = SQLAlchemy(model_class=Base)
