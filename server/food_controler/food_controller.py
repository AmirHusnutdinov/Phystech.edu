from flask import request, jsonify, Blueprint
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

    sql_query = f"INSERT INTO dish (name, owner, calories, proteins, carbohydrates, fats, category) VALUES ('{name}', '{owner}', '{calories}', '{proteins}', '{carbohydrates}', '{fats}', '{category}') RETURNING id;" 

    database_query(sql_query)

    return jsonify({'message': 'succsess'}), 201

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

    sql_query = f"INSERT INTO products (name, proteins, carbohydrates, fats, calories) VALUES ('{name}', '{proteins}', '{carbohydrates}', '{fats}', '{calories}')"

    database_query(sql_query)

    return jsonify({'message': 'Succsess'}), 201

def add_product_and_dish_dependence(products, dish_id):
    for product in products:
        sql_query = f"INSERT INTO dish_products_relate (id_product, id_dish, weight) VALUES ('{product['id']}', '{dish_id}', '{product['weight']}')"
        database_query(sql_query)


def is_json_correct(json, poles) -> bool:
    flag = True
    for pole in poles:
        flag = flag and pole in json
    return flag and json
