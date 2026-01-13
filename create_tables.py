#Создание всех новых объектов, которые наследуются от Base
from webapp import create_app
from webapp.db import db

app = create_app()

with app.app_context():
    print("Создание всех таблиц")
    
    # Создаем все таблицы на основе моделей
    db.create_all()
    
    print("Таблицы созданы успешно!")
    
    # Проверяем
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    
    print("\nСозданные таблицы")
    for table in tables:
        print(f"- {table}")
        
        # Выводим колонки каждой таблицы
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
