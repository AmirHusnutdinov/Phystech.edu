import os

from flask import render_template
from Admin.admin import Admin
from Calendar.calendar import Calendar
from Login.authorization import Authorization
from Login.registration import Registration
from MainPage.main_page import StartPage
from Mode1.mode1 import Mode1
from Mode2.mode2 import Mode2
from SelectedProducts.selectedProducts import SelectedProduct
from ServiceFiles.links import main_page, admin, authorization, registration, calendar, mode1, mode2, selected_products
from settings import app, host

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


@app.errorhandler(400)
def page_bad_request(_):
    error_phrase = ["Запрос", "неправильный", "."]
    return render_template("ErrorCodes/errors.html",
                           error_code_name="Bad request",
                           error_code="400",
                           error_phrase=error_phrase,
                           main_page=main_page), 400


@app.errorhandler(404)
def page_not_found(_):
    error_phrase = ["Похоже такой", "страницы", "нет"]
    return render_template("ErrorCodes/errors.html",
                           error_code_name="Not Found",
                           error_code="404",
                           error_phrase=error_phrase,
                           main_page=main_page), 404


@app.errorhandler(500)
def page_internal_server_error(_):
    error_phrase = ["Похоже что-то", "не очень", "хорошо."]
    return render_template("ErrorCodes/errors.html",
                           error_code_name="Internal Server Error",
                           error_code="500",
                           error_phrase=error_phrase,
                           main_page=main_page), 500


@app.errorhandler(501)
def page_internal_server_error(_):
    error_phrase = ["Не поддерживается функция,", "необходимая", "для выполнения запроса."]
    return render_template("ErrorCodes/errors.html",
                           error_code_name="Not Implemented",
                           error_code="501",
                           error_phrase=error_phrase,
                           main_page=main_page), 501


port = int(os.environ.get("PORT", 8080))
app.run(host=host, port=port, debug=True)
