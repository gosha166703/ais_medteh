from flask import Blueprint, render_template

blueprint = Blueprint("home", __name__)

 #Главная страница (Аналитика)
@blueprint.route('/')
def index():
    return render_template('home/index.html', page_title="Главная")