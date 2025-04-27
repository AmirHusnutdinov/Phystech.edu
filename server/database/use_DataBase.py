import psycopg2

from settings import host
from settings import user, password, db_name, port

from datetime import datetime

def database_query(sql, fetch=False):
    connection = []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name, port=port
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if fetch:
                return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with Postgres", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] Postgres connection closed")


def get_dishes():
    sql = "SELECT * FROM dish"
    dishes = database_query(sql, True)
    formatted_dishes = [
        {
            "id": dish[0],
            "name": dish[1],
            "calories": dish[3],
            "protein": dish[4],
            "carbs": dish[5],
            "fats": dish[6],
            "category": dish[7],
        }
        for dish in dishes
    ]
    return formatted_dishes


def get_user_data(user_id):
    sql = f'SELECT * FROM users WHERE id = {user_id}'
    user_data = database_query(sql, True)[0]
    user_info = {
        "id": user_data[0],
        "email": user_data[1],
        "login": user_data[2],
        "password": user_data[3],
        "name": user_data[4],
        "sex": user_data[5],
        "age": user_data[6],
        "language": user_data[7],
        "activity": user_data[8],
        "water": user_data[9],
        "weight": user_data[10],
        "height": user_data[11],
        "calories": user_data[12],
        "proteins": user_data[13],
        "carbs": user_data[14],
        "fats": user_data[15],
        'is_admin': user_data[16],
        'is_trainer': user_data[17],
        'is_activated': user_data[18]
    }
    return user_info


def update_user_data(user_id, data):
    # Проверяем, что словарь данных не пустой
    if not data:
        return False
    # Формируем SET часть SQL запроса
    set_parts = []
    for key in data:
        if key in ['id', 'password', 'email', 'login']:
            print('Error while updating user data: unaccesible field')
            return False
        # Экранируем специальные символы и обрабатываем разные типы данных
        value = data[key]
        if isinstance(value, str):
            value = f"'{value.replace("'", "''")}'"
        elif value is None:
            value = 'NULL'
        else:
            value = str(value)
        set_parts.append(f'"{key}" = {value}')
    
    set_clause = ', '.join(set_parts)
    
    # Формируем полный SQL запрос
    sql = f'UPDATE users SET {set_clause} WHERE id = {user_id}'
    
    try:
        # Выполняем запрос
        database_query(sql)
        return True
    except Exception as e:
        print(f"Error updating user data: {e}")
        return False

def get_day_data(user_id, date):
    sql = f"SELECT * FROM user_daily_metrics WHERE id = {user_id} AND date = '{date}'"
    return database_query(sql, True)

def get_trainer_request(user_id):
    sql = f"SELECT * FROM trainer_requests WHERE id_from = {user_id} AND status = 'in process'"
    data = database_query(sql, True)
    
    result = []
    for req in data:
        result.append({
            'request_id': req[0],
            'id_from': req[1],
            'id_to': req[2],
            'description': req[3],
            'status': req[4],
            'time': req[5]
        })
    
    return result

def add_trainer_request(id_from, id_to, description):
    sql = f"""
        INSERT INTO trainer_requests (id_from, id_to, description, status)
        VALUES ({id_from}, {id_to}, '{description}', 'in process')
    """
    database_query(sql)

def update_trainer_request(request_id, status):
    sql = f"UPDATE trainer_requests SET status = '{status}' WHERE request_id = {request_id}"
    database_query(sql, True)

def get_all_day_data(user_id):
    sql = f"SELECT * FROM user_daily_metrics WHERE id = {user_id}"
    data = database_query(sql, True)
    ans = []
    for el in data:
        day_data = {
            "id": el[0],
            "weight": el[1],
            "height": el[2],
            "water": el[3],
            "date": [el[4].year, el[4].month, el[4].day],
            "calories": el[5],
            "planCalories": el[6],
            "proteins": el[7],
            "planProteins": el[8],
            "fats": el[9],
            "planFats": el[10],
            "carbs": el[11],
            "planCarbs": el[12],
        }
        ans.append(day_data)
    return ans


def database_check():
    sql = "SELECT * FROM user_daily_metrics"
    return database_query(sql, True)


def save_news(title, content, image_path):
    database_query(
        f"""INSERT INTO news (title, picture, html, date) VALUES ('{title}', '{image_path}', '{content}', NOW())"""
    )


def check_trainer(user_id):
    sql = f'SELECT is_trainer FROM "users" WHERE id = {user_id}'
    query = database_query(sql, True)
    if query == []:
        return False
    data = database_query(sql, True)[0][0]
    if data:
        return True
    return False


def get_trainer_id(user_id):
    sql = f"SELECT id FROM student WHERE student_id = {user_id}"
    query = database_query(sql, True)
    if query == []:
        return 0
    return int(query[0][0])


def get_list_of_student(user_id):
    sql = f"SELECT student_id FROM student WHERE id = {user_id}"
    ans_list = []
    data = database_query(sql, True)
    for el in data:
        ans_list.append(int(el[0]))
    return ans_list


def get_message_history(first_id, second_id, since=None):
    
    if since:
        sql = f"""
        SELECT id_from, id_to, content, message_time
        FROM messages
        WHERE ((id_from = {first_id} AND id_to = {second_id}) 
               OR (id_from = {second_id} AND id_to = {first_id}))
        AND message_time AT TIME ZONE 'UTC' > '{since}'
        ORDER BY message_time
        """
    else:
        sql = f"""
        SELECT id_from, id_to, content, message_time
        FROM messages
        WHERE (id_from = {first_id} AND id_to = {second_id}) 
               OR (id_from = {second_id} AND id_to = {first_id})
        ORDER BY message_time
        """

    data = database_query(sql, True)
    message_history = []
    for el in data:
        message = {"id_from": el[0], "id_to": el[1], "content": el[2], "time": el[3]}
        message_history.append(message)
    return message_history


def add_message(id_from, id_to, content):
    sql = f"""
    INSERT INTO messages (id_from, id_to, content, message_time)
    VALUES ({id_from}, {id_to}, '{content}', NOW())
    """
    return database_query(sql)
