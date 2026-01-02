from db import engine, Base
from models import User, Role

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
print("База пересоздана")