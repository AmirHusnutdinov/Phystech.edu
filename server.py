import os
from settings import app, host
from ServiceFiles.links import main_page, admin, authorization, registration, calendar, mode1, mode2, selected_products
from MainPage.main_page import StartPage
from Admin.admin import Admin
from Login.registration import Registration
from Login.authorization import Authorization
from Calendar.calendar import Calendar
from Mode1.mode1 import Mode1
from Mode2.mode2 import Mode2
from SelectedProducts.selectedProducts import SelectedProduct


@app.route(main_page)
def open_main_page():
    return StartPage.show_the_main_page()


@app.route(admin)
def open_admin_page():
    return Admin.show_admin_page()


@app.route(authorization)
def open_authorization_page():
    return Authorization.show_authorization_page()


@app.route(registration)
def open_registration_page():
    return Registration.show_registration_page()


@app.route(calendar)
def open_calendar_page():
    return Calendar.show_calendar_page()


@app.route(mode1)
def open_mode1_page():
    return Mode1.show_mode1_page()


@app.route(mode2)
def open_mode2_page():
    return Mode2.show_mode2_page()


@app.route(selected_products)
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()


port = int(os.environ.get("PORT", 8181))
app.run(host=host, port=port)
