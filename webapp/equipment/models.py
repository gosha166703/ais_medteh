from sqlalchemy import Interval, String, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from webapp.db import Base

from datetime import datetime, timezone, timedelta
from typing import Optional

class Equipment(Base):
    __tablename__ = "equipment"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(1000), nullable=False)
    purpose: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) #ToDo: Справочник видов мед оборудования
    serial_number: Mapped[Optional[str]] = mapped_column(String(200),nullable=True)
    inventory_number: Mapped[Optional[str]] = mapped_column(String(200),nullable=True)
    subdivision: Mapped[str] = mapped_column(String(1000), nullable=True)
    date_entry: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default='active') #ToDo: Справочник статусов создать
    write_off:Mapped[bool] = mapped_column(Boolean, default=False)
    model:Mapped[Optional[str]] = mapped_column(String(1000), nullable=True) #ToDo: Справочник моделей создать
    manufacturer:Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    time_work:Mapped[timedelta] = mapped_column(Interval, default=lambda: timedelta(0)) 
    downtime:Mapped[timedelta] = mapped_column(Interval, default=lambda: timedelta(0))
    last_maintenance:Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                               default=lambda: datetime.now(timezone.utc))
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True), 
                                               default=lambda: datetime.now(timezone.utc), 
                                               onupdate=lambda: datetime.now(timezone.utc))



    def __repr__(self):
        return f"<Equipment: {self.name},{self.serial_number}, {self.inventory_number},{self.date_entry}, {self.status}>"