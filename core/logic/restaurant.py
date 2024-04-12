from django.db import connection

def get_restaurant_with_id_title(query):
    restaurants = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        for row in rows:
            data_col = dict(zip(columns, row))
            restaurants.append(data_col)
    return restaurants