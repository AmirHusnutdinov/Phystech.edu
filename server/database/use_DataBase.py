import psycopg2

from settings import host
from settings import user, password, db_name, port


def database_query(sql, Fetch=False):
    connection = []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name, port=port
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(sql)
            if Fetch:
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


def get_user_data(id):
    sql = f"SELECT * FROM public.\"User\" WHERE id = {id}"
    user_data = database_query(sql, True)[0]
    user = {
        "id": user_data[0],
        "name": user_data[1],
        "login": user_data[2],
        "password": user_data[3],
        "avatar": user_data[4],
        "email": user_data[5],
        "sex": user_data[6],
        "age": user_data[7],
        "language": user_data[8],
        "koef": user_data[9],
        "water": user_data[10],
        "physical_activities": user_data[11],
        "weight": user_data[12],
        "height": user_data[13],
        "calories": user_data[14],
        "proteins": user_data[15],
        "carbs": user_data[16],
        "fats": user_data[17],
        "eating_times": user_data[18],
    }
    return user


def get_day_data(id, date):
    sql = f"SELECT * FROM user_daily_metrics WHERE id = {id} AND date = {date}"
    return database_query(sql, True)


def get_all_day_data(id):
    sql = f"SELECT * FROM user_daily_metrics WHERE id = {id}"
    data = database_query(sql, True)
    print(data)
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
        f"""INSERT INTO news (title, picture, html, date) VALUES ('{title}', '{image_path}', '{content}', NOW())""")


def check_trainer(id):
    sql = f"SELECT role FROM roles WHERE id = {id}"
    print(id)
    print(database_query(sql, True))
    data = database_query(sql, True)[0][0]
    if data == 2 or data == 3:
        return True
    return False


def get_list_of_student(id):
    sql = f"SELECT student_id FROM student WHERE id = {id}"
    ans_list = []
    data = database_query(sql, True)
    for el in data:
        ans_list.append(el[0])
    return ans_list
