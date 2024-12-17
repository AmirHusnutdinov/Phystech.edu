import psycopg2

from settings import host, user, password, db_name


def database_query(sql):
    connection = []
    try:
        connection = psycopg2.connect(
            host=host, user=user, password=password, database=db_name
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
    return database_query(sql)

def get_user_data(id):
    sql = f"SELECT * FROM public.\"User\" WHERE id = {id}"
    return database_query(sql)[0]

def get_day_data(user, date):
    sql = f"SELECT * FROM user_daily_metrics WHERE id = {user.id} AND date = {date}"
    return database_query(sql)