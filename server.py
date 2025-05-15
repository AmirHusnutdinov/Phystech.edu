import os

from server.hendler.handler import Handler
from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.day_plan.day_plan import DayPlan
from server.login.authorization import Authorization
from server.login.cabinet import Cabinet

# from server.login.process_registration import ProcessRegistration
from server.login.registration import Registration
from server.main_page.main_page import StartPage
from server.news.news import News
from server.selected_products.selectedProducts import SelectedProduct
from server.trainer.trainer_students import Students
from server.food_controler.food_controller import food_blueprint, delete_old_diets
from apscheduler.schedulers.background import BackgroundScheduler
from settings import app, host

__all__ = ["app"]

app.secret_key = os.urandom(24)
app.register_blueprint(food_blueprint)

scheduler = BackgroundScheduler()
scheduler.add_job(delete_old_diets, "cron", hour=0, minute=0)
scheduler.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
