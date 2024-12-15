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
