import os

from flask import request, render_template
from utils import render_template_with_user

from server.hendler.handler import handler
from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.day_plan.day_plan import DayPlan
from server.login.authorization import Authorization
from server.login.cabinet import Cabinet
from server.login.registration import Registration
from server.main_page.main_page import StartPage
from server.news.news import News
from server.selected_products.selectedProducts import SelectedProduct
from server.service_files.links import main_page, admin, calendar, day_plan, selected_products, registration, authorization, \
    cabinet, all_news, one_news, add_product, save_day_plan, process_registration, confirm_code, process_login, logout, \
    add_product, all_students, student, make_news, save_news
from server.trainer.trainer_students import Students
from server.food_controler.food_controller import food_blueprint, delete_old_diets
from apscheduler.schedulers.background import BackgroundScheduler
from flask import request, render_template
from settings import app, host
from server.service_files.links import *

app.secret_key = os.urandom(24)
app.register_blueprint(food_blueprint)

scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_diets, 'cron', hour=0, minute=0)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host=host, port=port, debug=True)
