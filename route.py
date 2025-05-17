from datetime import datetime, timedelta

from flask import request, Blueprint, jsonify
from flask import session, redirect, render_template

from server.admin.admin import Admin
from server.calendar.calendar import Calendar
from server.database.use_DataBase import database_query
from server.day_plan.day_plan import DayPlan
from server.food_controler.forms import AddDishForm, AddProductForm, AddDietForm, DTUForm
from server.login.authorization import Authorization
from server.login.cabinet import Cabinet
from server.login.process_registration import ProcessRegistration
from server.login.registration import Registration
from server.main_page.main_page import StartPage
from server.news.news import News
from server.selected_products.selectedProducts import SelectedProduct
from server.service_files.links import *;
from server.trainer.trainer_students import Students

server_blueprint = Blueprint('server_blueprint', __name__)
@server_blueprint.route("/admin")
def open_admin_page():
    return Admin.show_admin_page()


@server_blueprint.route("/calendar/<int:student_id>")
def calendar_page(student_id):
    return Calendar.show_calendar_page_with_id(student_id)


@server_blueprint.route("/calendar")
def open_calendar_page():
    return Calendar.show_calendar_page()


@server_blueprint.route("/add_product", methods=["GET", "POST"])
def open_add_product():
    if "user_id" in session:
        return DayPlan.show_add_product_page()
    return redirect("/main")


@server_blueprint.route("/add_recipes", methods=["GET", "POST"])
def open_add_recipes():
    if "user_id" in session:
        return DayPlan.show_add_recipes()
    return redirect("/main")


@server_blueprint.route("/day_plan")
def open_day_plan_page():
    return DayPlan.show_day_plan_page()


@server_blueprint.route("/save_day_plan", methods=["POST"])
def save_data():
    if "user_id" in session:
        return DayPlan.save_food_intake()
    return redirect("/main")


@server_blueprint.route("/physical_exercises")
def open_physical_exercises_page():
    if "user_id" in session:
        images = DayPlan.cloud.get_folder("exercises")
        return render_template(
            "DayPlan/physical_exercises.html",
            header_links=choose_header_links("authorized"),
            title="Трекер Физических Упражнений",
            day_plan=day_plan,
            images=images,
        )
    return redirect("/main")


@server_blueprint.route("/day_plan/get_new_messages", methods=["GET"])
def get_chat_messages_route():
    return DayPlan.get_new_messages()


@server_blueprint.route("/day_plan/send_message", methods=["POST"])
def send_message_route():
    return DayPlan.send_message()


@server_blueprint.route("/authorization", methods=["GET", "POST"])
def open_authorization_page():
    return Authorization.show_authorization_page()


@server_blueprint.route("/process_login", methods=["POST"])
def process_login():
    return Authorization.process_login()


@server_blueprint.route("/logout")
def logout():
    return Authorization.logout()


@server_blueprint.route("/cabinet", methods=["GET", "POST"])
def open_cabinet_page():
    return Cabinet.show_cabinet_page()


@server_blueprint.route("/cabinet/update_profile", methods=["POST"])
def update_profile():
    return Cabinet.update_profile()


@server_blueprint.route("/cabinet/update_nutrition", methods=["POST"])
def update_nutrition():
    return Cabinet.update_nutrition()


@server_blueprint.route(
    "/cabinet/submit_trainer_application", methods=["POST"]
)
def submit_trainer_application():
    return Cabinet.submit_trainer_application()


@server_blueprint.route("/cabinet/request_trainer", methods=["POST"])
def request_trainer():
    return Cabinet.request_trainer()


@server_blueprint.route(
    "/cabinet/approve_request/<int:request_id>", methods=["POST"]
)
def approve_request(request_id):
    return Cabinet.approve_request(request_id)


@server_blueprint.route(
    "/cabinet/reject_request/<int:request_id>", methods=["POST"]
)
def reject_request(request_id):
    return Cabinet.reject_request(request_id)


@server_blueprint.route("/process_registration", methods=["GET"])
def show_process_registration_page():
    return ProcessRegistration.show_process_registration_page()


@server_blueprint.route("/process_registration/submit", methods=["POST"])
def submit_registration():
    return ProcessRegistration.submit()


@server_blueprint.route("/registration", methods=["GET", "POST"])
def show_registration_page():
    return Registration.show_registration_page()


@server_blueprint.route("/process_registration", methods=["POST"])
def process_registration():
    return Registration.process_registration()


@server_blueprint.route("/confirm_code", methods=["GET", "POST"])
def confirm_code():
    if request.method == "POST":
        return Registration.process_confirmation()
    return Registration.show_confirmation_page()


@server_blueprint.route("/main")
def open_main_page():
    return StartPage.show_the_main_page()


@server_blueprint.route("/all_news")
def open_all_news_page():
    return News.show_all_news_page()


@server_blueprint.route("/one_news/<int:news_id>")
def open_one_news_page(news_id):
    return News.show_one_news_page(news_id)


@server_blueprint.route("/make_news", methods=["GET"])
def open_make_news_page():
    return News.show_make_news()


@server_blueprint.route("/save_news", methods=["POST"])
def handle_make_news():
    return News.handle_make_news()


@server_blueprint.route("/news/<int:news_id>/edit", methods=["GET"])
def edit_news_page(news_id):
    return News.show_make_news(news_id)


@server_blueprint.route("/news/<int:news_id>/delete", methods=["POST"])
def delete_news_page(news_id):
    return News.handle_delete_news(news_id)


@server_blueprint.route("/selected_products")
def open_selected_products_page():
    return SelectedProduct.show_selected_product_page()


@server_blueprint.route("/all_students")
def open_all_students_page():
    return Students.show_students_page()


@server_blueprint.route("/student/<int:student_id>", methods=["GET", "POST"])
def open_students_page(student_id):
    return Students.show_one_student_page(student_id)


@server_blueprint.route("/send_message", methods=["POST"])
def send_message():
    return Students.send_message()


@server_blueprint.route("/get_new_messages/<int:student_id>")
def get_new_messages(student_id):
    return Students.get_new_messages(student_id)

@server_blueprint.route('/data/dish', methods=['POST'])
def add_dish():
    form = AddDishForm()

    name = form.name.data
    owner = form.owner.data
    calories = form.calories.data
    proteins = form.proteins.data
    carbohydrates = form.carbohydrates.data
    fats = form.fats.data
    category = form.category.data
    products = form.products

    sql_query = (f"INSERT INTO "
                 f"dish (name, owner, calories, proteins, carbohydrates, fats, category)"
                 f"VALUES ('{name}', '{owner}', '{calories}', '{proteins}', '{carbohydrates}', '{fats}',"
                 f" '{category}') RETURNING id;")

    user_id = database_query(sql_query, True)
    if user_id is None:
        return jsonify({'error': 'Failed to insert diet'}), 500
    add_product_and_dish_dependence(products=products, dish_id=user_id[0][0])

    return jsonify({'message': 'succsess'}), 201


def add_product_and_dish_dependence(products, dish_id):
    for product in products:
        sql_query = (f"INSERT INTO dish_products_relate (id_product, id_dish, weight) VALUES ('{product.product_id.data}',"
                     f" '{dish_id}', '{product.weight.data}')")
        database_query(sql_query)


@server_blueprint.route('/data/products', methods=['POST'])
def add_product():
    form = AddProductForm()

    name = form.name.data
    calories = form.calories.data
    proteins = form.proteins.data
    carbohydrates = form.carbohydrates.data
    fats = form.fats.data

    sql_query = (f"INSERT INTO products (name, proteins, carbohydrates, fats, calories) VALUES ('{name}', '{proteins}',"
                 f" '{carbohydrates}', '{fats}', '{calories}')")

    database_query(sql_query)

    return jsonify({'message': 'Succsess'}), 201


@server_blueprint.route('/diets', methods=['POST'])
def add_diet():
    form = AddDietForm()

    name = form.name.data
    owner = form.owner.data
    description = form.owner.description
    dishes = form.dishes

    sql_query = (f"INSERT INTO diets (name, owner, description) VALUES ('{name}', '{owner}',"
                 f" '{description}') RETURNING id;")

    user_id = database_query(sql_query, True)
    if user_id is None:
        return jsonify({'error': 'Failed to insert diet'}), 500
    add_diet_and_dishes_dependence(dishes=dishes, diet_id=user_id[0][0])

    return jsonify({'message': 'Succsess'}), 201


def add_diet_and_dishes_dependence(dishes, diet_id):
    for dish in dishes:
        sql_query = (f"INSERT INTO diet_dish_relate (diet_id, dish_id, weight, time_of_day) VALUES ('{diet_id}',"
                     f" '{dish.dish_id.data}', '{dish.weight.data}', '{dish.time_of_day.data}') ")
        database_query(sql_query)


@server_blueprint.route('/<int:user_id>/diets', methods=['PUT'])
def set_diets_to_user(user_id):
    form = DTUForm()

    trainer_id = form.trainer_id.data

    is_trainer_have_access = database_query(f"SELECT 1 WHERE EXISTS ( SELECT 1 FROM users_trainers WHERE tainer_id = '{trainer_id}' AND user_id = '{user_id}'", Fetch=True)
    if not is_trainer_have_access:
         return jsonify({'error': 'Access denied'}), 403

    diet_id = form.diet_id.data
    date = form.date.data

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    now_date = datetime.now().date()
    end_next_week = (datetime.now() + timedelta(days=(13 - datetime.now().weekday()))).date()
    if not (now_date <= date <= end_next_week):
        return jsonify({'error': 'Invalid data'}), 400

    check_sql_query = f"""
        SELECT COUNT(*) 
        FROM users_diets 
        WHERE diet_id = '{diet_id}' 
        AND user_id = '{user_id}' 
        AND date = '{date}'
    """
    check_result = database_query(check_sql_query, fetch=True)

    if check_result and check_result[0][0] > 0:
        return jsonify({'error': 'Record already exists'}), 400

    sql_query = f"INSERT INTO users_diets (diet_id, user_id, date) VALUES ('{diet_id}', '{user_id}', '{date}')"

    database_query(sql_query)

    return jsonify({'message': 'Succsess'}), 201


def delete_old_diets():
    delta = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

    sql = f"DELETE FROM users_diets WHERE date < '{delta}';"

    database_query(sql)
    print("[INFO] Old diets was deleted for all users")


@server_blueprint.route('/<int:user_id>/diets', methods=['GET'])
def get_user_diet(user_id):
    date = request.args.get('date')
    if date:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        sql = f"SELECT * FROM users_diets WHERE user_id = '{user_id}' AND date ='{date}'"

    else:
        sql = f"SELECT * FROM users_diets WHERE user_id = {user_id}"

    return database_query(sql, True)


@server_blueprint.route('/<int:user_id>/diets', methods=['DELETE'])
def delete_user_diet(user_id):
    form = DTUForm()

    diet_id = form.diet_id.data
    date = form.date.data
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    sql = f"DELETE FROM users_diets WHERE user_id = '{user_id}' AND dish_id = '{diet_id}' AND date = '{date}';"

    database_query(sql)

    return jsonify({'message': 'Delete diet is success'}), 201


