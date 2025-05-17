from datetime import datetime

from flask import jsonify, Blueprint

from forms import TrainForm
from server.service_files.links import *
from utils import render_template_with_user
from ..database.use_DataBase import database_query

trains_blueprint = Blueprint('trains_blueprint', __name__)


@trains_blueprint.route('/<int:user_id>/trains', methods=['POST'])
def add_trains_to_user(user_id):
    form = TrainForm()
    train_id = form.train_id.data
    date = form.date.data
    time = form.time.data

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

    sql_query = f"INSERT INTO users_trains (user_id, train_id, date, time) VALUES ('{user_id}', '{train_id}', '{date}', '{time}')"

    database_query(sql_query)

    return jsonify({'message': 'Succsess'}), 201


@trains_blueprint.route('/<int:user_id>/trains', methods=['GET'])
def get_user_train(user_id):
    current_date = datetime().now().date()

    sql_query = f"""
        SELECT name, date, time, kpd 
        FROM users_trains us
        WHERE date = '{current_date}' AND user_id = {user_id};
        JOIN trains tr ON tr.id = train_id
    """
    sql = database_query(sql_query)

    if not sql:
        return jsonify({'error': 'Record not found'}), 200

    trainings = [
        {
            "name": row[0],
            "date": row[1],
            "time": row[2],
            "kpd": row[3]
        } for row in sql
    ]

    return render_template_with_user(
        "Trainings/training.html",
        header_links=choose_header_links("authorized"),
        title="Сегодняшняя тренировка",
        date=current_date,
        trainings=trainings
    )


def parse_tine(time: str):
    hours, mins = divmod(time, 60)
    if hours > 0 and mins > 0:
        return f"{hours} hours {mins} minutes"
    elif hours > 0:
        return f"{hours} hours"
    else:
        return f"{mins} minutes"
