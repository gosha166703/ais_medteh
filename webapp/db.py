from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

# Подключение к своей локальной базе данных okm_ais
engine = create_engine(
    'postgresql://ais_user:255655@localhost:5432/okm_ais'
)

db_session = scoped_session(sessionmaker(bind=engine))

class Base(DeclarativeBase):
    pass