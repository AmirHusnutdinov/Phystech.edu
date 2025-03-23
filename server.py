import os

from flask import request
from utils import render_template_with_user

from Admin.admin import Admin
from Calendar.calendar import Calendar
from DayPlan.day_plan import DayPlan
from Login.authorization import Authorization
from Login.cabinet import Cabinet
from Login.registration import Registration
from MainPage.main_page import StartPage
from News.news import News
from SelectedProducts.selectedProducts import SelectedProduct
from ServiceFiles.links import main_page, admin, calendar, day_plan, selected_products, registration, authorization, \
    cabinet, all_news, one_news, add_product, save_day_plan, process_registration, confirm_code, process_login, logout, \
    add_product, all_students, student, make_news, save_news
from Trainer.trainer_students import Students
from settings import app, host

app.secret_key = os.urandom(24)


@app.route(main_page)
def open_main_page():
    return StartPage.show_the_main_page()


@app.route(admin)
def open_admin_page():
    return Admin.show_admin_page()


@app.route(registration, methods=['GET', 'POST'])
def show_registration_page():
    return Registration.show_registration_page()


@app.route(process_registration, methods=['POST'])
def process_registration():
    return Registration.process_registration()


@app.route(confirm_code, methods=['GET', 'POST'])
def confirm_code():
    if request.method == 'POST':
        return Registration.process_confirmation()
    return Registration.show_confirmation_page()


@app.route(authorization, methods=['GET', 'POST'])
def open_authorization_page():
    return Authorization.show_authorization_page()


@app.route(process_login, methods=['POST'])
def process_login():
    return Authorization.process_login()


@app.route(logout)
def logout():
    return Authorization.logout()


@app.route(cabinet, methods=['GET', 'POST'])
def open_cabinet_page():
    return Cabinet.show_cabinet_page()


@app.route(calendar)
def open_calendar_page():
    return Calendar.show_calendar_page()


@app.route(day_plan)
def open_day_plan_page():
    return DayPlan.show_day_plan_page()


@app.route(save_day_plan, methods=['POST'])
def save_data():
    return DayPlan.save_day_plan()


@app.route(selected_products)
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()


@app.route(all_news)
def open_all_news_page():
    return News.show_all_news_page()


@app.route(one_news)
def open_one_news_page(news_id):
    return News.show_one_news_page(news_id)

@app.route(make_news, methods=['GET'])
def open_make_news_page():
    return News.show_make_news()

@app.route(save_news, methods=['POST'])
def handle_make_news():
    return News.handle_make_news()


@app.route(add_product)
def open_add_product():
    return DayPlan.show_add_product_page()


@app.route(all_students)
def open_all_students_page():
    return Students.show_students_page()


@app.route(student)
def open_students_page(student_id):
    return Students.show_one_student_page(student_id)


@app.errorhandler(400)
def page_bad_request(_):
    error_phrase = ["Запрос", "неправильный", "."]
    return render_template_with_user("ErrorCodes/errors.html",
                           error_code_name="Bad request",
                           error_code="400",
                           error_phrase=error_phrase,
                           main_page=main_page), 400


@app.errorhandler(404)
def page_not_found(_):
    error_phrase = ["Похоже такой", "страницы", "нет"]
    return render_template_with_user("ErrorCodes/errors.html",
                           error_code_name="Not Found",
                           error_code="404",
                           error_phrase=error_phrase,
                           main_page=main_page), 404


@app.errorhandler(500)
def page_internal_server_error(_):
    error_phrase = ["Похоже что-то", "не очень", "хорошо."]
    return render_template_with_user("ErrorCodes/errors.html",
                           error_code_name="Internal Server Error",
                           error_code="500",
                           error_phrase=error_phrase,
                           main_page=main_page), 500


@app.errorhandler(501)
def page_not_implemented(_):
    error_phrase = ["Не поддерживается функция,", "необходимая", "для выполнения запроса."]
    return render_template_with_user("ErrorCodes/errors.html",
                           error_code_name="Not Implemented",
                           error_code="501",
                           error_phrase=error_phrase,
                           main_page=main_page), 501

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host=host, port=port, debug=True)
