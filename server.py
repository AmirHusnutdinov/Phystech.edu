import os

from flask import render_template, request

from Admin.admin import Admin
from Calendar.calendar import Calendar
from DayPlan.day_plan import DayPlan
from Login.authorization import Authorization
from Login.cabinet import Cabinet
from Login.registration import Registration
from MainPage.main_page import StartPage
from News.news import News
from SelectedProducts.selectedProducts import SelectedProduct
from Trainer.trainer_students import Students
from ServiceFiles.links import *
from settings import app, host

app.secret_key = os.urandom(24)





port = int(os.environ.get("PORT", 8080))
app.run(host=host, port=port, debug=True)
