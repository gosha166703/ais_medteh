from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    @app.route("/")
    def index():
        text_title = 'АИС "Сервисный отдел"'
        text_body = 'Главная страница'
        return render_template("index.html",title=text_title, body=text_body ) 
    return app