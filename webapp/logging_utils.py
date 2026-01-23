import json
from datetime import datetime, timezone
from webapp.db import db

class ActionLog(db.Model):
    __tablename__ = "action_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_email = db.Column(db.String(100), nullable=True)
    action_type = db.Column(db.String(50), nullable=False)  #Просмотр, редактирование, удаление
    equipment_id = db.Column(db.Integer, nullable=True)
    equipment_name = db.Column(db.String(1000), nullable=True)
    details = db.Column(db.Text, nullable=True) 
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

def log_equipment_action(user_id, action_type, equipment_id=None, details=None, user_email=None, equipment_name=None):
    #Логирование действий с оборудованием
    try:
        log_entry = ActionLog(
            user_id=user_id,
            user_email=user_email,
            action_type=action_type,
            equipment_id=equipment_id,
            equipment_name=equipment_name,
            details=json.dumps(details, ensure_ascii=False, default=str) if details else None
        )
        db.session.add(log_entry)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при логировании действия: {str(e)}")
        return False