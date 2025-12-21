from flask import Flask

app = Flask(__name__)

#Используем декоратор. URL "/" означает галвная страница
@app.route("/")
def index():
    return "Автоматическая информационная система сервисного отдела"

#Запустить сервер 
if __name__ == "__main__":
    app.run()