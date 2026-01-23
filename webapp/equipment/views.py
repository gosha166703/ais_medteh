from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import select, or_, and_
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from webapp.db import db
from webapp.equipment.forms import EquipmentForm
from webapp.equipment.models import Equipment
from webapp.user.decorators import admin_required

blueprint = Blueprint("equipment", __name__, url_prefix="/equipment")

# Константы для пагинации
ITEMS_PER_PAGE = 50

# Эндпоинт Реестр основных средств с пагинацией и фильтрацией
@blueprint.route("/")
def equipment():
    page = request.args.get('page', 1, type=int)
    
    # Получаем параметры фильтрации из запроса
    search_query = request.args.get('search', '').strip()
    model_filter = request.args.get('model', '').strip()
    manufacturer_filter = request.args.get('manufacturer', '').strip()
    status_filter = request.args.get('status', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    
    # Базовый запрос
    query = select(Equipment)
    
    # Применяем поиск по названию или инвентарному номеру
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.where(
            or_(
                Equipment.name.ilike(search_pattern),
                Equipment.inventory_number.ilike(search_pattern),
                Equipment.serial_number.ilike(search_pattern)
            )
        )
    
    # Применяем фильтр по модели
    if model_filter:
        model_pattern = f"%{model_filter}%"
        query = query.where(Equipment.model.ilike(model_pattern))
    
    # Применяем фильтр по производителю
    if manufacturer_filter:
        manufacturer_pattern = f"%{manufacturer_filter}%"
        query = query.where(Equipment.manufacturer.ilike(manufacturer_pattern))
    
    # Применяем фильтр по статусу
    if status_filter:
        query = query.where(Equipment.status == status_filter)
    
    # Применяем фильтр по дате поступления
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.where(Equipment.date_entry >= date_from_obj)
        except ValueError:
            flash("Некорректный формат даты 'с'", "warning")
    
    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d')
            # Добавляем 23:59:59 к дате "по"
            date_to_obj = date_to_obj.replace(hour=23, minute=59, second=59)
            query = query.where(Equipment.date_entry <= date_to_obj)
        except ValueError:
            flash("Некорректный формат даты 'по'", "warning")
    
    # Сортировка
    query = query.order_by(Equipment.created_at.desc())
    
    # Получаем общее количество с учетом фильтров
    total_count = db.session.scalar(select(db.func.count()).select_from(query.subquery()))
    
    # Пагинация
    offset = (page - 1) * ITEMS_PER_PAGE
    query = query.offset(offset).limit(ITEMS_PER_PAGE)
    
    # Выполняем запрос
    equipment_list = db.session.execute(query).scalars().all()
    
    # Рассчитываем общее количество страниц
    total_pages = (total_count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE if total_count > 0 else 1
    
    # Определяем диапазон страниц для отображения в пагинации
    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)
    
    # Получаем уникальные значения для выпадающих списков
    models = db.session.execute(
        select(Equipment.model).distinct().where(Equipment.model.is_not(None)).order_by(Equipment.model)
    ).scalars().all()
    
    manufacturers = db.session.execute(
        select(Equipment.manufacturer).distinct().where(Equipment.manufacturer.is_not(None)).order_by(Equipment.manufacturer)
    ).scalars().all()
    
    statuses = db.session.execute(
        select(Equipment.status).distinct().order_by(Equipment.status)
    ).scalars().all()
    
    # Статусы с русскими названиями для отображения
    status_names = {
        'active': 'В работе',
        'inactive': 'В резерве',
        'repair': 'На ремонте',
        'not_active': 'Не исправно'
    }
    
    return render_template(
        "equipment/equipment.html", 
        page_title="Реестр основных средств",
        equipment_list=equipment_list,
        current_page=page,
        total_pages=total_pages,
        total_count=total_count,
        start_page=start_page,
        end_page=end_page,
        items_per_page=ITEMS_PER_PAGE,
        # Параметры фильтров для сохранения в форме
        search_query=search_query,
        model_filter=model_filter,
        manufacturer_filter=manufacturer_filter,
        status_filter=status_filter,
        date_from=date_from,
        date_to=date_to,
        # Данные для выпадающих списков
        models=models,
        manufacturers=manufacturers,
        statuses=statuses,
        status_names=status_names
    )

#Эндпоинт Создание оборудования
@blueprint.route("/create", methods=["GET","POST"])
@login_required
def create_equipment():
    form = EquipmentForm()
    if form.validate_on_submit():
        new_equipment = Equipment(
            name=form.name.data,
            purpose=form.purpose.data,
            serial_number=form.serial_number.data,
            inventory_number=form.inventory_number.data,
            date_entry=form.date_entry.data,
            status=form.status.data,
            write_off=form.write_off.data,
            model=form.model.data,
            manufacturer=form.manufacturer.data,
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
    equipment = db.session.get(Equipment, id)
    if not equipment:
        flash("Оборудование не найдено", "error")
        return redirect(url_for("equipment.equipment"))
    
    form = EquipmentForm(obj=equipment)
    
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
@admin_required  # Добавляем проверку на администратора
def delete_equipment(id):
    equipment = db.session.get(Equipment, id)
    if not equipment:
        flash("Оборудование не найдено", "error")
        return redirect(url_for('equipment.equipment'))
    
    try:
        # Сохраняем информацию об удаляемом оборудовании для лога
        equipment_info = {
            'id': equipment.id,
            'name': equipment.name,
            'inventory_number': equipment.inventory_number,
            'serial_number': equipment.serial_number,
            'deleted_by': current_user.id,
            'deleted_by_email': current_user.email,
            'deleted_at': datetime.now(timezone.utc).isoformat()
        }
        
        db.session.delete(equipment)
        db.session.commit()
        
        # Логирование удаления
        try:
            from webapp.logging_utils import log_equipment_action
            log_equipment_action(
                user_id=current_user.id,
                action_type='delete',
                equipment_id=id,
                details=equipment_info,
                user_email=current_user.email,
                equipment_name=equipment.name
            )
        except ImportError:
            # Если модуль логирования не настроен, пропускаем
            pass
        
        flash("Оборудование удалено", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении: {str(e)}', 'error')
    
    return redirect(url_for('equipment.equipment'))