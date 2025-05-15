import datetime
import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail

load_dotenv()


class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    ACC_ACCESS_KEY = os.getenv("ACC_ACCESS_KEY")
    ACC_SECRET_KEY = os.getenv("ACC_SECRET_KEY")
    ENDPOINT_URL = os.getenv("ENDPOINT_URL")
    REGION_NAME = os.getenv("REGION_NAME")
    BUCKET_MAIN_PATH = os.getenv("BUCKET_MAIN_PATH")


app = Flask(__name__)

# folder for containing temp files before uploading them to the cloud
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}

app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)
host = "127.0.0.1"
port = os.getenv("POSTGRES_PORT")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("DATABASE_NAME")
app.config.from_object(Config)

MAIL_SERVER = "smtp.yandex.ru"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

import os

from flask import *
from server.hendler.handler import Handler
from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.day_plan.day_plan import DayPlan
from server.login.authorization import Authorization
from server.login.cabinet import Cabinet

# from server.login.process_registration import ProcessRegistration
from server.login.registration import Registration

# from server.main_page.main_page import StartPage
from server.news.news import News
from server.selected_products.selectedProducts import SelectedProduct
from server.trainer.trainer_students import Students
from server.food_controler.food_controller import food_blueprint, delete_old_diets
from apscheduler.schedulers.background import BackgroundScheduler
from settings import app, host

app.secret_key = os.urandom(24)
app.register_blueprint(food_blueprint)

scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_diets, "cron", hour=0, minute=0)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)


@app.route("/")
def open_main_page():
    return show_the_main_page()


def show_the_main_page():
    return render_template("MainPage/main.html", title="Главная страница")
