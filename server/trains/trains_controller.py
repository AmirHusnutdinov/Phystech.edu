from datetime import timedelta, datetime

from flask import jsonify, Blueprint
from flask import request
from ..database.use_DataBase import database_query
from forms import TrainForm

trains_blueprint = Blueprint('trains_blueprint', __name__)

@trains_blueprint.route('/<int:user_id>/trains', methods=['PUT']) 
def add_trains_to_user(user_id):
    form = TrainForm()
    train_id = form.train_id.data
    date = form.date.data
    time = form.time.data

    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    time = parse_tine(time)

    check_sql_query = f"""
        SELECT COUNT(*) 
        FROM users_trains 
        WHERE user_id = '{user_id}' 
        AND train_id = '{train_id}' 
        AND date = '{date}'
        AND time = '{time}'
    """
    check_result = database_query(check_sql_query, fetch=True)

    if check_result and check_result[0][0] > 0:
        return jsonify({'error': 'Record already exists'}), 400

    sql_query = f"INSERT INTO users_diets (user_id, train_id, date, time) VALUES ('{user_id}', '{train_id}', '{date}', '{time}')"

    database_query(sql_query)

    return jsonify({'message': 'Succsess'}), 201

    
    
def parse_tine(time: str):
    hours, mins = divmod(time, 60)
    if hours > 0 and mins > 0:
        return f"{hours} hours {mins} minutes"
    elif hours > 0:
        return f"{hours} hours"
    else:
        return f"{mins} minutes"