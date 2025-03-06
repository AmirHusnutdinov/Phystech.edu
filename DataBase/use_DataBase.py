import psycopg2

from settings import host, user, password, db_name, port


def database_query(sql):
    connection = []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name, port=port
        )
        connection.autocommit = True
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as _ex:
        print("[INFO] Error while working with Postgres", _ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] Postgres connection closed")


def get_dishes():
    sql = "SELECT * FROM dish"
    dishes = database_query(sql)
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
    user_data = database_query(sql)[0]
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


def get_day_data(user, date):
    sql = f"SELECT * FROM user_daily_metrics WHERE id = {user.id} AND date = {date}"
    return database_query(sql)


def database_check():
    sql = "SELECT * FROM user_daily_metrics"
    return database_query(sql)


print(database_check())
