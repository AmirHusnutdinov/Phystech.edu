from datetime import datetime, timedelta

from flask import jsonify, Blueprint
from flask import request

from .utils import is_json_correct
from ..database.use_DataBase import database_query

from .forms import AddDishForm, AddProductForm, AddDietForm, DTUForm

food_blueprint = Blueprint('food_blueprint', __name__)


@food_blueprint.route('/data/dish', methods=['POST'])
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


@food_blueprint.route('/data/products', methods=['POST'])
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


@food_blueprint.route('/diets', methods=['POST'])
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


@food_blueprint.route('/<int:user_id>/diets', methods=['PUT'])
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


@food_blueprint.route('/<int:user_id>/diets', methods=['GET'])
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


@food_blueprint.route('/<int:user_id>/diets', methods=['DELETE'])
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