from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from webapp.db import Base

from datetime import datetime

class FixedAssed(Base):
    __tablename__ = "fixed_assed"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(1000))
    purpose: Mapped[str] = mapped_column(String(100)) #ToDo: Справочник видов мед оборудования
    serial_number: Mapped[int] = mapped_column(unique=True)
    inventory_number: Mapped[int] = mapped_column(unique=True)
    date_entry: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(50)) #ToDo: Справочник статусов создать
    write_off:Mapped[bool] = mapped_column(Boolean)
    model:Mapped[str] = mapped_column(String(1000)) #ToDo: Справочник моделей создать
    manufacturer:Mapped[str] = mapped_column(String(1000))
    time_work:Mapped[datetime] = mapped_column(DateTime) #ToDo: Указать модуль time
    downtime:Mapped[datetime] = mapped_column(DateTime) #ToDo: Указать модуль time
    last_maintenance:Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<FixedAssed: {self.name},{self.serial_number}, {self.inventory_number},{self.date_entry}, {self.status}>"
