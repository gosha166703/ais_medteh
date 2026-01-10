from flask import Blueprint

from datetime import timedelta
from flask import render_template, flash, redirect, url_for
from flask_login import login_required

from sqlalchemy import select

from webapp.db import db
from webapp.equipment.forms import EquipmentForm
from webapp.equipment.models import Equipment

blueprint = Blueprint("equipment", __name__, url_prefix="/equipment")

#Эндпоинт Реестр основных средств
@blueprint.route("/")
def equipment():
    #Получить все оборудование из БД 
    stmt = select(Equipment).order_by(Equipment.created_at.desc())
    equipment_list = db.session.execute(stmt).scalars().all()
    return render_template("equipment/equipment.html", page_title="Реестр основных средств",
                            equipment_list=equipment_list)

#Эндпоинт Создание оборудования
@blueprint.route("/create", methods=["GET","POST"])
@login_required
def create_equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        new_equipment = Equipment(name=form.name.data,
                                    purpose=form.purpose.data,
                                    serial_number=form.serial_number.data,
                                    inventory_number=form.inventory_number.data,
                                    date_entry=form.date_entry.data,
                                    status=form.status.data,
                                    write_off=form.write_off.data,
                                    model=form.model.data,
                                    manufacturer=form.manufacturer.data,
                                    #time_work=timedelta(hours=form.time_work.data or 0),
                                    #downtime=timedelta(hours=form.downtime.data or 0),
                                    last_maintenance=form.last_maintenance.data,
                                    )
        try:
            db.session.add(new_equipment)
            db.session.commit()
            flash("Оборудование добавлено в реестр", 'success')
            return redirect(url_for("equipment.equipment"))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при добавлении: {str(e)}", "error") 

    return render_template("equipment/equipment_form.html", form=form, page_title="Добавить оборудование")

#Эндпоинт Просмотр оборудования
@blueprint.route("/<int:id>", methods=["GET"])
@login_required
def equipment_detail(id):
    equipment = db.session.get(Equipment, id)
    if not equipment:
        flash("Оборудование не найдено", "error")
        return redirect(url_for("equipment.equipment"))
    return render_template("equipment/equipment_detail.html", equipment=equipment, page_title=equipment.name)

#Эндпоинт Редактирование оборудования
@blueprint.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def equipment_edit(id):
    #Обработка GET запроса
    equipment = db.session.get(Equipment, id)
    if not equipment:
        flash("Оборудование не найдено", "error")
        return redirect(url_for("equipment.equipment"))
    form = EquipmentForm(obj=equipment)
    
    #Обработка POST запроса
    if form.validate_on_submit():
        form.populate_obj(equipment)
        try:
            db.session.commit()
            flash("Изменения сохранены", "success")
            return redirect(url_for("equipment.equipment_detail", id=id))
        except Exception as e:
            db.session.rollback()
            flash(f"Ошибка при изменении: {str(e)}", "error")
    return render_template("equipment/equipment_form.html", form=form, 
                        page_title="Редактировать оборудование", equipment=equipment)


#Эндпоинт Удаление оборудования
@blueprint.route("<int:id>/delete", methods=["POST"])
@login_required
def delete_equipment(id):
    equipment = db.session.get(Equipment, id)
    try:
        db.session.delete(equipment)
        db.session.commit()
        flash ("Оборудование удалено", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {str(e)}', 'error')
        
    return redirect(url_for('equipment.equipment'))