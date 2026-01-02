from db import db_session

from models_fixed_assed import Fixed_assed

from datetime import datetime

enginner_fixed_assed = Fixed_assed(name = "OMS 3000",
                                    purpose = "Стоматологическое оборудование",
                                    serial_number = 73823820,
                                    inventory_number = 8973720,
                                    date_entry = datetime(2026, 12, 26),
                                    status = "Исправно",
                                    write_off = False,
                                    model = "3000", 
                                    manufacturer = "OMS",
                                    time_work = datetime(2026, 6, 12), 
                                    downtime = datetime(2026, 8, 19),
                                    last_maintenance = datetime(2026, 12, 5))

db_session.add(enginner_fixed_assed)
db_session.commit()