from flask import Flask, render_template

app = Flask(__name__)

#Используем декоратор. URL "/" означает галвная страница. 
#Функция для подготовки данных для отображения
@app.route("/")
def index():
    text_title = 'АИС "Сервисный отдел"'
    text_body = 'Главная страница'
    return render_template("index.html",title=text_title, body=text_body )

#Запустить сервер 
if __name__ == "__main__":
    app.run()