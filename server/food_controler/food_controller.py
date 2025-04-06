from datetime import datetime, timedelta

from flask import jsonify, Blueprint
from flask import request

from .utils import is_json_correct
from ..database.use_DataBase import database_query

food_blueprint = Blueprint('food_blueprint', __name__)


@food_blueprint.route('/data/dish', methods=['POST'])
def add_dish():
    new_dish = request.json

    dish_poles = {'name', 'owner', 'calories', 'proteins', 'carbohydrates', 'fats', 'category', 'products'}

    if not is_json_correct(json=new_dish, poles=dish_poles):
        return jsonify({'error': 'Invalid data'}), 400

    name = new_dish['name']
    owner = new_dish['owner']
    calories = new_dish['calories']
    proteins = new_dish['proteins']
    carbohydrates = new_dish['carbohydrates']
    fats = new_dish['fats']
    category = new_dish['category']
    products = new_dish['products']

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
        sql_query = (f"INSERT INTO dish_products_relate (id_product, id_dish, weight) VALUES ('{product['id']}',"
                     f" '{dish_id}', '{product['weight']}')")
        database_query(sql_query)


@food_blueprint.route('/data/products', methods=['POST'])
def add_product():
    new_product = request.json

    product_poles = {'name', 'proteins', 'carbohydrates', 'fats', 'calories'}

    if not is_json_correct(json=new_product, poles=product_poles):
        return jsonify({'error': 'Invalid data'}), 400

    name = new_product['name']
    proteins = new_product['proteins']
    carbohydrates = new_product['carbohydrates']
    fats = new_product['fats']
    calories = new_product['calories']

    sql_query = (f"INSERT INTO products (name, proteins, carbohydrates, fats, calories) VALUES ('{name}', '{proteins}',"
                 f" '{carbohydrates}', '{fats}', '{calories}')")

    database_query(sql_query)

    return jsonify({'message': 'Succsess'}), 201


@food_blueprint.route('/diets', methods=['POST'])
def add_diet():
    new_diet = request.json

    diet_poles = {'name', 'owner', 'description', 'dishes'}

    if not is_json_correct(json=new_diet, poles=diet_poles):
        return jsonify({'error': 'Invalid data'}), 400

    name = new_diet['name']
    owner = new_diet['owner']
    description = new_diet['description']
    dishes = new_diet['dishes']

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
                     f" '{dish['id']}', '{dish['weight']}', '{dish['time_of_day']}') ")
        database_query(sql_query)


@food_blueprint.route('/<int:user_id>/diets', methods=['PUT'])
def set_diets_to_user(user_id):
    diets_to_user = request.json

    dtu_poles = {'diet_id', 'date'}

    if not is_json_correct(diets_to_user, dtu_poles):
        return jsonify({'error': 'Invalid data'}), 400

    diet_id = diets_to_user['diet_id']
    try:
        date = datetime.strptime(diets_to_user['date'], '%Y-%m-%d').date()
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
    user_diet = request.json
    json_poles = {'dish_id', 'date'}
    if not is_json_correct(json=user_diet, poles=json_poles):
        return jsonify({'error': 'Invalid data'}), 400

    dish_id = user_diet['dish_id']
    date = user_diet['date']

    sql = f"DELETE FROM users_diets WHERE user_id = '{user_id}' AND dish_id = '{dish_id}' AND date = '{date}';"

    database_query(sql)

    return jsonify({'message': 'Delete diet is success'}), 201
