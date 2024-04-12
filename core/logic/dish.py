from django.db import connection

def get_dish_all(query):
    dishes = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        for row in rows:
            data_col = dict(zip(columns, row))
            dishes.append(data_col)
    return dishes