# Загрузчик основных средств в реестр основных средств
import csv, sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webapp.db import db
from webapp.models_equipment import Equipment
from webapp import create_app


#Чтение csv файла
def read_csv(filname): 
    with open(filname, "r") as f:
        fields = [
            "Основное средство",
            "Инвентарный номер",
            "Подразделение",
            "Дата принятия к учету"
        ]
        reader = csv.DictReader(f, fields, delimiter=";")
        for row in reader:
            save_equipment_data(row)

#Сохранение значений из файла в базу данных
def save_equipment_data(row):
    equipment=Equipment(
        name=row["Основное средство"],
        inventory_number=row["Инвентарный номер"],
        subdivision=row["Подразделение"],
        date_entry=row["Дата принятия к учету"]
    )
    db.session.add(equipment)
    db.session.commit()

if __name__ == "__main__":
    app = create_app()
    
    with app.app_context():
        read_csv("os_1.csv")
